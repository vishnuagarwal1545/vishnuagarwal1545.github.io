---
layout: post
title: Autoscaling on Request Rate with KEDA and Datadog - What the Docs Don't Tell You
date: 2026-10-24
description: Hands-on notes from replacing per-app Datadog external-metric HPAs with KEDA on EKS. How a Datadog trigger really turns into a replica count, a unit bug that made every service scale to max, and what the tests showed.
tags: kubernetes, keda, datadog, autoscaling, hpa, eks, devops
categories: devops, kubernetes
_styles: |
  #markdown-content table {
    border-collapse: collapse;
    width: 100%;
    margin: 2rem 0;
  }
  #markdown-content table th {
    background-color: var(--global-theme-color);
    color: var(--global-bg-color);
    padding: 0.75rem;
    text-align: left;
  }
  #markdown-content table td {
    padding: 0.6rem 0.75rem;
    border-bottom: 1px solid var(--global-divider-color);
  }
---

Most teams that scale Kubernetes workloads on Datadog metrics start with the Datadog Cluster Agent's external metrics provider. You create a `DatadogMetric` resource per app, then point an HPA at it. It works, but every app ends up carrying terraform for its scaling query, and the query lives far from the service it scales.

I recently evaluated [KEDA](https://keda.sh) as the replacement. The scaling query lives in a `ScaledObject` that ships with the service, in the same Helm chart or repo as its Deployment, and KEDA talks to the Datadog API directly. This post covers how a KEDA Datadog trigger actually computes replicas, a **unit bug that made our test service scale straight to its maximum**, and what the load tests showed.

The setup: EKS, KEDA 2.18 installed with its Helm chart, a `ScaledObject` per service, Karpenter for nodes, and Envoy Gateway in front of the services.

## Why move off `DatadogMetric` + HPA?

| | Datadog external metrics (HPA) | KEDA `datadog` trigger |
|---|---|---|
| Where the query lives | A `DatadogMetric` resource, applied by per-app terraform | A `ScaledObject` in the app's own chart, next to its Deployment |
| Changing a target | terraform apply, then an app config change | One deploy of the app chart |
| Link between metric and HPA | Name passed through env vars; a mismatch fails silently | The query is in the ScaledObject itself; KEDA creates the HPA |
| Other signals | Datadog only | 60+ scalers (SQS, CloudWatch, Kafka, Prometheus, cron, cpu, memory) |
| Metric unavailable | HPA freezes | `fallback` sets a safe replica count |
| Scale to zero | No | Yes |

**The catch: only one external metrics provider per cluster.** Kubernetes routes every `external.metrics.k8s.io` request to whoever owns the `v1beta1.external.metrics.k8s.io` APIService. The Datadog Cluster Agent and KEDA both register it. To install KEDA you hand the APIService over by setting `clusterAgent.metricsProvider.registerAPIService: false` in the Datadog chart. From then on, any HPA still pointing at `datadogmetric@...` silently stops scaling. So the switch is **per cluster**, and every app using Datadog-metric scaling has to migrate in the same window.

## What you actually deploy

KEDA scaling isn't a field on the Deployment. It takes three kinds of resources.

**1. Datadog credentials, once per cluster.** A Secret plus a `ClusterTriggerAuthentication`. For a cluster-scoped auth, the Secret must be in KEDA's own namespace:

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: datadog-keda-credentials
  namespace: keda
stringData:
  apiKey: <DD_API_KEY>
  appKey: <DD_APP_KEY>      # needs the timeseries_query scope
  datadogSite: datadoghq.com
---
apiVersion: keda.sh/v1alpha1
kind: ClusterTriggerAuthentication
metadata:
  name: datadog-keda-auth
spec:
  secretTargetRef:
    - parameter: apiKey
      name: datadog-keda-credentials
      key: apiKey
    - parameter: appKey
      name: datadog-keda-credentials
      key: appKey
    - parameter: datadogSite
      name: datadog-keda-credentials
      key: datadogSite
```

**2. The Deployment, unchanged except for one thing: leave out `replicas`.** Once KEDA's HPA owns the replica count, a `replicas:` value in the manifest resets the count on every `kubectl apply` or `helm upgrade`. GitOps tools then show the HPA's changes as drift. Either drop the field, or tell Argo CD to ignore it (`ignoreDifferences` on `/spec/replicas`).

**3. A `ScaledObject` per service**, shipped in the same chart as the Deployment:

```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: web
  namespace: my-app
spec:
  scaleTargetRef:
    name: web                  # the Deployment to scale
  minReplicaCount: 2
  maxReplicaCount: 12
  fallback:
    failureThreshold: 3
    replicas: 2
  advanced:
    horizontalPodAutoscalerConfig:
      behavior:
        scaleDown:
          stabilizationWindowSeconds: 300
          policies:
            - type: Percent
              value: 50
              periodSeconds: 60
  triggers:
    - type: datadog
      metricType: AverageValue
      metadata:
        query: "sum:envoy.cluster.upstream_rq_completed.count{kube_namespace:my-app,envoy_cluster:httproute/my-app/*}.as_count().rollup(sum, 60)"
        queryValue: "20"
        age: "180"
        lastAvailablePointOffset: "1"
      authenticationRef:
        name: datadog-keda-auth
        kind: ClusterTriggerAuthentication
```

KEDA then creates and owns an HPA named `keda-hpa-web`. **Don't create your own HPA for the same Deployment;** two HPAs fighting over one target is undefined behaviour. When you delete the ScaledObject, its HPA goes with it. The Deployment then keeps its last replica count, unless `advanced.restoreToOriginalReplicaCount: true` is set.

If you run a PaaS or platform layer that renders ScaledObjects from its own app manifest, it does steps 2 and 3 for you. The objects underneath are the same, so everything below still applies.

## How a Datadog trigger becomes a replica count

This took more digging than it should have. KEDA doesn't scale anything itself. It exposes your query as an external metric and creates an HPA (`keda-hpa-<name>`), which makes the decisions. Each decision has five steps:

1. **Query a window.** On every HPA sync (every 15s), Datadog is queried for `[now − age, now]`. KEDA's default `age` is 90s.
2. **Pick one point, without averaging.** KEDA takes the newest point, or the Nth-from-last with `lastAvailablePointOffset`. Offset `1` skips the newest bucket, which is often still being filled.
3. **Compute replicas.** With `metricType: AverageValue`, "average" means **per pod**:
   `desired = ceil(value ÷ queryValue)`, clamped to min and max. Changes within 10% of the target are ignored.
4. **Limit the rate of change.** `scaleUp` policies apply, e.g. at most +100% every 15s.
5. **Stabilize the scale-down.** During the scale-down window, the HPA keeps the **highest** recommendation it computed.

Two things surprised me:

- **`pollingInterval` usually doesn't drive scaling.** With `minReplicaCount ≥ 1` and no `useCachedMetrics`, KEDA's own polling loop doesn't query the trigger at all. The HPA's 15s sync does. So each ScaledObject makes about **240 Datadog API calls per hour**. With many services, use `useCachedMetrics: true` and watch the rate limit.
- **It's one point, not an average.** Spiky traffic means jumpy scaling unless you smooth it in the query or in the stabilization window.

## The bug: `.as_rate()` wasn't a rate

The first version of the trigger looked reasonable:

```yaml
query: "sum:envoy.cluster.upstream_rq_completed.count{...}.as_rate()"
queryValue: "1"      # 1 request/sec per pod
age: "120"
lastAvailablePointOffset: "1"
```

Under load, the service went straight to its maximum (12 replicas). The HPA reported about 2.1 req/s per pod across 12 pods, roughly 25 req/s in total. **The Datadog UI showed the actual load peaking at about 3.4 req/s.**

Querying Datadog with the same short window KEDA uses showed the cause:

```text
.as_rate()  → 48, 51, 51, 51, 51, 49, 52, 53   (interval 15s)
.as_count() → 48, 51, 51, 51, 51, 49, 52, 53   (interval 15s)
```

**At this granularity, `.as_rate()` returned exactly what `.as_count()` did: the raw count per 15-second bucket.** KEDA got about 51 and compared it with a target of 1. In effect the target was "one request per 15 seconds per pod", so any traffic at all maxed the service out.

The fix was to stop relying on `.as_rate()` and make the unit explicit:

```yaml
query: "sum:envoy.cluster.upstream_rq_completed.count{...}.as_count().rollup(sum, 60)"
queryValue: "20"     # requests per MINUTE per pod
age: "180"           # >= 2 full 60s buckets
lastAvailablePointOffset: "1"   # skip the minute still filling
```

**Takeaway:** before you trust a Datadog query in a scaler, run it with the **same `age` window** KEDA will use and look at the raw points. What a dashboard shows over an hour isn't what a 2-minute API query returns.

## Load test results

With `queryValue: 20` (20 requests per minute per pod), I generated stepped load with a deliberate one-minute pause. Requests per minute come from Datadog, replicas from the HPA events.

| Load (req/min) | Expected `ceil(÷20)` | HPA did |
|---|---|---|
| 203 | 11 | 1 → **11** ✅ |
| 154 | 8 | → **8** ✅ |
| 76 | 4 | → **4** ✅ |
| 0 | 1 (min) | → **1** ✅ |
| 7 (the pause) | 1 | **11 → 1** ⚠️ |

- **The math matched at every step.**
- **Reaction time** was about 1–2 minutes to scale up and 1–1.5 minutes to scale down. That's expected with one-minute buckets and skipping the newest point.
- **Karpenter** launched nodes within seconds for pods that didn't fit, and removed them 1.5–5 minutes after the pods left.
- **A transient Datadog API timeout** raised a `KEDAScalerFailed` event, and KEDA recovered 8 seconds later. Fallback didn't trigger, because it needs N failures in a row.

### The pause: an aggressive scale-down plus node consolidation

The test used fast settings so it would finish quickly: a 30s scale-down window and −100% every 15s. A one-minute pause in traffic dropped the service from **11 pods to 1**. At the same moment, Karpenter consolidated the node holding that last pod. The disruption budget allowed the eviction, so **zero pods were available** for a moment.

Two lessons:

1. **The scale-down window has to be longer than the metric's granularity.** With one-minute buckets, a 30s window means one quiet minute can remove almost everything. Use ≥180s, and keep the 300s default in production. Also cap the rate, e.g. −50% per 60s.
2. **The HPA and node disruption interact.** Our default PDB for single-replica services was `maxUnavailable: 1`, which allows the last pod to be evicted. A PodDisruptionBudget doesn't stop the HPA from scaling down, because removing replicas isn't an eviction. It does stop the node autoscaler from evicting your last pod. With a single replica, though, `minAvailable: 1` blocks **every** voluntary drain of that node, including consolidation, drift and AMI updates. The robust setup is **minimum 2 replicas plus `minAvailable: 1`**. (A follow-up PDB test is in progress.)

## CPU and memory as a safety net

KEDA has built-in `cpu` and `memory` scalers, so they can sit next to the Datadog trigger in the same ScaledObject's `spec.triggers`:

```yaml
# ScaledObject spec.triggers
triggers:
  - type: datadog
    metricType: AverageValue
    metadata:
      query: "sum:...as_count().rollup(sum, 60)"
      queryValue: "20"
      age: "180"
      lastAvailablePointOffset: "1"
  - type: cpu
    metricType: Utilization
    metadata:
      value: "70"
  - type: memory
    metricType: Utilization
    metadata:
      value: "80"
```

- **The HPA uses the highest** of the replica counts the three triggers ask for.
- **If Datadog is unreachable,** CPU and memory keep working, since they come from metrics-server inside the cluster. Kubernetes also **refuses to scale down** while any metric is missing, so a Datadog outage can't shrink the service. `fallback` covers the Datadog trigger itself.
- **Caveats:**
  - Utilization is relative to the pod's **requests**, so set them.
  - Skip the memory trigger for apps that hold on to memory (caches, JVM heaps). Otherwise they never scale back down.

## Monitoring KEDA itself

The KEDA Helm chart ships with the operator's Prometheus metrics **disabled** (`prometheus.operator.enabled: false`). Our first install ran with `--enable-prometheus-metrics=false`, and nothing listened on the operator's metrics port. Without that, the useful metrics (`keda_scaler_errors`, `keda_scaler_metrics_value`, scale-loop latency) don't exist, and the Datadog KEDA integration has nothing to scrape.

What worked even without operator metrics:

- **Kubernetes events:** `KEDAScalerFailed`, `SuccessfulRescale`.
- **HPA state** from kube-state-metrics.
- **Operator logs.**
- **The metrics-apiserver's `:8080/metrics`,** which covers the adapter's request latency and its gRPC calls to the operator.

Set `prometheus.operator.enabled: true` in the chart values from day one, then point the Datadog KEDA integration (openmetrics on `:8080/metrics`) at the operator.

## Summary

- KEDA is a cleaner home for Datadog-driven scaling than per-app `DatadogMetric` + HPA, but the switch is cluster-wide. Plan a coordinated cutover.
- Enable the operator's Prometheus metrics in the Helm chart; they're off by default.
- **Verify the units of your query** with the same short window KEDA uses. `.as_rate()` on a count over a 2-minute window gave me raw per-15s counts.
- `AverageValue` means per pod. It's one data point, not an average over time, and expect about 1–2 minutes of delay.
- Make scale-down slower than your metric's granularity, run at least 2 replicas with a PDB, and add CPU and memory triggers as a backstop.
- Make sure you can see KEDA's own errors before you depend on it.

**Helm values we ended up with** (relevant parts):

```yaml
prometheus:
  operator:
    enabled: true          # keda_scaler_* and keda_scaled_object_* metrics on :8080
nodeSelector:
  node-role/system: "true" # keep KEDA on the fixed system nodes
tolerations:
  - key: node-role/system
    operator: Equal
    value: "true"
    effect: NoSchedule
```

**References:** [KEDA Datadog scaler](https://keda.sh/docs/latest/scalers/datadog/), [KEDA ScaledObject spec](https://keda.sh/docs/latest/reference/scaledobject-spec/), [KEDA authentication (TriggerAuthentication / ClusterTriggerAuthentication)](https://keda.sh/docs/latest/concepts/authentication/), [Kubernetes HPA algorithm](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#algorithm-details), [HPA scaling behavior](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/#configurable-scaling-behavior), [Datadog rollup](https://docs.datadoghq.com/dashboards/functions/rollup/), [Datadog API rate limits](https://docs.datadoghq.com/api/latest/rate-limits/), [KEDA Helm chart values](https://github.com/kedacore/charts/blob/main/keda/values.yaml).
