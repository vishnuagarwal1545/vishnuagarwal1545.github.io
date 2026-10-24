---
layout: post
title: Moving from Cluster Autoscaler to Karpenter on EKS - Field Notes from a Dev Cluster Migration
date: 2026-10-24
description: A step-by-step test of replacing Cluster Autoscaler with Karpenter on an EKS cluster. What changed at each step, what broke (DaemonSets), and what consolidation, pool limits and disruption controls actually did.
tags: kubernetes, karpenter, eks, aws, autoscaling, cost-optimization, devops
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

[Karpenter](https://karpenter.sh) replaces the Cluster Autoscaler (CAS) model of "grow a node group of one instance type" with "launch the cheapest instance that fits the pods that are waiting". I tested the migration end to end on a development EKS cluster: Karpenter 1.13 installed with Helm, next to the existing EKS managed node groups and Cluster Autoscaler.

Before every step I took read-only snapshots of Helm values, EKS access entries, subnet and security group tags, IAM, SQS, EventBridge, nodes, pods, DaemonSets and PDBs, then diffed them afterwards. This post walks through those diffs and the behaviour tests.

**Target design:**

- **System nodes:** a small managed node group, one node per AZ, fixed size, tainted `node-role/system=true:NoSchedule`. It runs Karpenter itself, CoreDNS, the ingress and gateway controllers, cert-manager, KEDA and metrics-server. Karpenter can't run on nodes it manages, so these have to exist.
- **Workload nodes:** a Karpenter `NodePool` and `EC2NodeClass` for every app.

## Why Karpenter

|                   | Cluster Autoscaler                     | Karpenter                                                                         |
| ----------------- | -------------------------------------- | --------------------------------------------------------------------------------- |
| Unit of scaling   | Node group (ASG), fixed instance types | Individual instance, chosen per launch                                            |
| Capacity shortage | Scale-up stalls until the ASG retries  | Falls back to another allowed type or AZ                                          |
| Bin-packing       | Fixed node size                        | Sizes nodes to the pods that are waiting                                          |
| Scale-down        | Removes nodes when every pod can move  | Consolidation deletes empty nodes, and replaces under-used ones with cheaper ones |
| Node lifecycle    | Manual node group roll                 | Drift detection, expiry, disruption budgets                                       |

## The migration, step by step

**1. Prerequisites: discovery tags and CRDs.** We tagged every subnet and the cluster security groups with `karpenter.sh/discovery=<cluster>`, and installed the Karpenter CRDs.

- The cluster already used EKS access mode `API_AND_CONFIG_MAP`.
- No running workload changed.
- A terraform plan of our cluster add-ons showed no drift.

**2. Installing Karpenter.** The diff here was large:

- the controller (2 replicas, with a PDB, pinned to the system nodes);
- a `NodePool` and an `EC2NodeClass`;
- controller and node IAM roles, plus an instance profile;
- an **EKS access entry** for the node role;
- an SQS interruption queue and 4 EventBridge rules (spot interruption, rebalance, scheduled change, state change);
- Cluster Autoscaler scaled to 0.

We deliberately registered the node role through an **access entry**, not `aws-auth`. Our `aws-auth` ConfigMap is managed by terraform, and a later apply would have removed a manually added role, leaving new nodes unable to join.

At the same step we **tainted the existing managed nodes** `node-role/system=true:NoSchedule`, to reserve them for system pods. Running pods stayed where they were. But from that moment, **any new pod** (a deploy, a restart, a CronJob) landed on a fresh Karpenter node. **The migration begins when you taint, not when you drain.**

**3. Moving workloads.** We replaced the managed node group with a smaller one: 5 general-purpose nodes became 3 small system nodes (one per AZ), using a rolling node group update. The old nodes were cordoned and drained, and every app pod rescheduled onto Karpenter nodes.

We then rolled the system node group once more, to a different instance type. Only the system nodes were replaced. **The workload nodes and app pods weren't touched, with zero restarts.** That's a useful property: system node maintenance no longer disturbs apps.

## What broke: our DaemonSets

Right after tainting the existing nodes:

| DaemonSet                     | Desired | Running | Misscheduled |
| ----------------------------- | ------- | ------- | ------------ |
| Datadog agent                 | 0       | 5       | 5            |
| Vector (logs)                 | 0       | 5       | 5            |
| eks-pod-identity-agent        | 0       | 5       | 5            |
| aws-node, kube-proxy, ebs-csi | 5       | 5       | 0            |

A `NoSchedule` taint doesn't evict pods that are already running, so nothing went down **yet**. But the next rollout of those DaemonSets, or any new system node, would have come up without monitoring, logs or pod identity. At that moment every node was a system node, so a single Helm upgrade of the agent would have left the **whole cluster** unmonitored.

**The fix** for our own DaemonSets was the same toleration AWS uses on aws-node and kube-proxy:

```yaml
tolerations:
  - operator: Exists
```

It also covers build nodes and dedicated pools added later. The pod identity agent is an EKS add-on, and its tolerations are set through the add-on's configuration values:

```bash
aws eks update-addon --cluster-name <cluster> --addon-name eks-pod-identity-agent \
  --configuration-values '{"tolerations":[{"operator":"Exists"}]}'
```

**Lesson:** before enabling Karpenter, list every DaemonSet and check its tolerations against the taints your system and workload pools will carry.

## Testing done

**Environment.** A dev EKS cluster (3 AZs) running about 15 small services and a few CronJobs. KEDA scales the test HTTP service on request rate.

The `workload` NodePool was configured as:

```yaml
requirements:
  - key: karpenter.k8s.aws/instance-family
    operator: In
    values: ["t3a"]
  - key: karpenter.k8s.aws/instance-size
    operator: In
    values: ["medium", "large", "xlarge", "2xlarge"]
  - key: karpenter.sh/capacity-type
    operator: In
    values: ["on-demand"]
  - key: kubernetes.io/arch
    operator: In
    values: ["amd64"]
disruption:
  consolidationPolicy: WhenEmptyOrUnderutilized
  consolidateAfter: 30s
  budgets:
    - nodes: "20%"
template:
  spec:
    expireAfter: Never
limits:
  cpu: "100"
  memory: 400Gi
```

**Method.**

- Before and after every step, a script captured read-only snapshots: EKS access entries, subnet and SG tags, IAM roles, instance profiles, SQS, EventBridge rules, `aws-auth`, CRDs, nodes with labels and taints, pods per node, DaemonSet coverage, PDBs, and the NodePool and EC2NodeClass specs. Each snapshot was then diffed against the previous one with `diff -ru`.
- Behaviour was observed through NodeClaim events (`Launched`, `DisruptionTerminating`, `DisruptionBlocked`, `Unconsolidatable`), HPA events and the Karpenter controller logs.

| #   | Test                                     | How                                                                                       | Expected                                                         | Result                                                                                                                                        |
| --- | ---------------------------------------- | ----------------------------------------------------------------------------------------- | ---------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | Prerequisites                            | Discovery tags on subnets and SGs, install CRDs                                           | Tags only; no workload, IAM or auth change; terraform plan clean | ✅ As expected                                                                                                                                |
| 2   | Install Karpenter                        | Helm install, NodePool, EC2NodeClass, IAM, access entry, SQS, EventBridge; scale CAS to 0 | Controller Ready; nodes keep running; `aws-auth` untouched       | ✅ All created. ⚠️ Tainting the existing nodes left 3 DaemonSets with **0 desired** (fixed with tolerations)                                  |
| 3   | Migrate workloads                        | Replace the managed node group (5 → 3 small system nodes)                                 | Apps drain onto Karpenter nodes; no stuck drains                 | ✅ All apps moved, none unhealthy, no PDB blocks                                                                                              |
| 4   | Roll system nodes again                  | Change the system node group's instance type                                              | Only system nodes replaced                                       | ✅ Workload nodes untouched, **0 app restarts**                                                                                               |
| 5   | Scale-out                                | 6 pods × 1 vCPU / 1 GiB                                                                   | Karpenter chooses a right-sized node                             | ✅ **1 × 2xlarge**, ready in about 40s (not 5 mediums)                                                                                        |
| 6   | Consolidation                            | Scale back to 1 pod × 256m                                                                | Under-used nodes removed or replaced                             | ✅ 2xlarge + medium → **1 × xlarge** (`Underutilized`), then `Can't replace with a cheaper node`                                              |
| 7   | KEDA + Karpenter                         | Load on the HTTP service, KEDA range 1–12                                                 | Pending pods get a node fast; cleanup after the load             | ✅ Node launched about **3s** after pods went pending; extra nodes removed **50–80s** after scale-down                                        |
| 8   | Pool limit                               | Set `limits.cpu` = 5 with 4 vCPU in use, then load                                        | No new nodes; pods Pending                                       | ✅ `all available instance types exceed limits for nodepool`. **Unrelated CronJobs blocked too.** Restoring the limit launched a node at once |
| 9   | `do-not-disrupt`                         | Annotate a node, then reduce load                                                         | Node not consolidated                                            | ✅ `DisruptionBlocked … do-not-disrupt`; the other node was consolidated instead; the protected node still accepted pods                      |
| 10  | Remove the annotation                    | Remove the annotation from the node                                                       | Node evaluated normally again                                    | ✅ `Unconsolidatable: Can't replace with a cheaper node`                                                                                      |
| 11  | Monitoring endpoint                      | Scrape `:8080/metrics` on each controller pod                                             | Karpenter metrics available                                      | ✅ 56 metric families. ⚠️ **Only the leader** reports the `nodepools_*` and `nodeclaims_*` series                                             |
| —   | Disruption block window, rollback to CAS | —                                                                                         | —                                                                | Not run in this round                                                                                                                         |

## Test details

### Scale-out picks bigger nodes

Six pods requesting 1 vCPU each came up as pending. Karpenter batched them and launched **one t3a.2xlarge**, not five mediums. The node was ready in about 40 seconds.

### Consolidation merges and replaces

When I scaled back down, Karpenter replaced a 2xlarge **and** a half-empty medium with a single xlarge (`Underutilized`). It then reached a steady state, logging `Can't replace with a cheaper node`. During the scale-out it had already moved the contents of two under-used mediums onto the new 2xlarge, without being asked.

### KEDA plus Karpenter, end to end

Load triggered KEDA to scale pods from 1 to 12. Karpenter launched a node about **3 seconds** after the pods went pending, and everything was Running in under a minute. When the load stopped, KEDA scaled back down and Karpenter removed the extra nodes **within about 50–80 seconds**.

### Pool limits fail quietly

With the NodePool CPU limit set just above current use, new pods stayed Pending:

```text
Failed to schedule pod, all available instance types exceed limits for nodepool
```

- **It blocks every app on that pool,** including unrelated CronJobs, not just the one that's scaling.
- **Restoring the limit** launched a node straight away.
- **So:** set limits with generous headroom (2–3× peak), and **alert** on `nodepools_usage / nodepools_limit`.

### `do-not-disrupt` works, with a nuance

Annotating a node `karpenter.sh/do-not-disrupt=true` produced:

```text
DisruptionBlocked: Disruption is blocked through the "karpenter.sh/do-not-disrupt" annotation
```

Karpenter consolidated the **other** node instead, and moved its pods onto the protected one. **Protected nodes still accept new pods.**

## Observations worth planning for

- **Consolidation evicts single-replica pods freely.** Ingress controllers, gateways and single-replica APIs each saw a short outage during consolidation. Give anything critical at least 2 replicas and a PDB, or protect it with `do-not-disrupt`, or use a disruption block window.
- **No zone spread by default.** Karpenter packs nodes by cost. After consolidation, every dev app ran on **one node in one AZ**. Zone spread has to come from `topologySpreadConstraints` on each Deployment (`topologyKey: topology.kubernetes.io/zone`).
- **CronJobs cause node churn.** With `consolidateAfter: 30s`, a CronJob running every 5 minutes on an otherwise idle pool launched and removed a node on every run. On quiet pools, raise `consolidateAfter`.
- **Set node expiry to `Never` before migrating.** Every node created during the migration would otherwise expire on the same day 30 days later. **Expiry ignores disruption budgets,** and the value is fixed on each node when it's created. Patch nodes through AMI drift instead, which respects budgets, and pin the AMI alias for production.
- **System nodes are fixed overhead.** On a small dev cluster, 3 dedicated system nodes plus 1 workload node cost **about 40% more** than the original 5 identical nodes. The savings show up on larger clusters, where system nodes are a small share of the total.
- **Monitoring:** only the **leader** replica reports the cluster-level metrics (`nodepools_*`, `nodeclaims_*`), so scrape **each pod** rather than the Service ClusterIP. Also check your autodiscovery: Karpenter's image short name is `controller`, which also matches ingress-nginx's. An endpoints-based check on the Karpenter Service avoids the collision.

## Choosing instance families

Two rules from the tests:

- **Adding a family** doesn't replace anything. Existing nodes still match. A cheaper new family gets used for new nodes and gradually through consolidation. A pricier one becomes a fallback for capacity shortages.
- **Removing or replacing a family** marks every non-matching node **drifted**, and they're all replaced. The pace follows the disruption budget, and every pod restarts once. Add the new family first, then remove the old one in a planned window.

For a production fleet whose pod **CPU requests ran about 7× actual usage**, the bigger saving isn't the instance family. **It's right-sizing requests.** Karpenter packs nodes by requests, so it can't recover CPU that's been requested and never used.

## Summary

| Area               | Result                                                            |
| ------------------ | ----------------------------------------------------------------- |
| Enable and migrate | ✅ Clean, but tainting existing nodes needs DaemonSet tolerations |
| Scale-out          | ✅ Right-sized nodes, ready in about 40s                          |
| Consolidation      | ✅ Merges and replaces nodes; evicts single replicas ⚠️           |
| KEDA integration   | ✅ Pods to nodes in seconds, cleanup in about a minute            |
| Pool limits        | ✅ Enforced, quietly. Alert on usage                              |
| do-not-disrupt     | ✅ Works; protected nodes still accept pods                       |
| Zone spread        | ⚠️ Not automatic; opt in per service                              |

Karpenter delivered what it promised. Most of the work in migrating is in what it exposes: DaemonSet tolerations, disruption budgets for single replicas, zone spread, pool-limit alerts, and accurate pod requests.

**References:** [Karpenter docs](https://karpenter.sh/docs/), [Disruption](https://karpenter.sh/docs/concepts/disruption/), [NodePools](https://karpenter.sh/docs/concepts/nodepools/), [Karpenter getting started on EKS](https://karpenter.sh/docs/getting-started/getting-started-with-karpenter/), [EKS access entries](https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html).
