---
layout: page
permalink: /resume/
title: Resume
nav: false
description: ATS-compliant resume for Vishnu Agarwal - Senior DevOps Engineer
---

<div class="resume-container" style="max-width: 800px; margin: 0 auto; padding: 20px; font-family: Arial, Helvetica, sans-serif; line-height: 1.6; color: #333;">
  
  <header style="text-align: center; margin-bottom: 30px; border-bottom: 2px solid #333; padding-bottom: 20px;">
    <h1 style="margin: 0; font-size: 28px; font-weight: bold;">VISHNU AGARWAL</h1>
    <p style="margin: 5px 0; font-size: 18px; font-weight: 600;">Senior DevOps Engineer | Remote</p>
    <p style="margin: 5px 0; font-size: 14px;">
      Email: <a href="mailto:vishnuagarwal1545@gmail.com" style="color: #0066cc; text-decoration: none;">vishnuagarwal1545@gmail.com</a> | 
      Phone: <a href="tel:+919884213512" style="color: #0066cc; text-decoration: none;">+91 9884213512</a>
    </p>
    <p style="margin: 5px 0; font-size: 14px;">
      Website: <a href="https://vishnuagarwal1545.github.io" style="color: #0066cc; text-decoration: none;">https://vishnuagarwal1545.github.io</a>
    </p>
  </header>

  <section style="margin-bottom: 25px;">
    <h2 style="font-size: 20px; font-weight: bold; margin-bottom: 10px; border-bottom: 1px solid #ccc; padding-bottom: 5px;">PROFESSIONAL SUMMARY</h2>
    <p style="margin: 0; text-align: justify;">
      Senior DevOps Engineer with 6+ years of experience in cloud infrastructure, platform reliability, and large-scale automation. Proven expertise in AWS, Kubernetes, Terraform, CI/CD, database engineering, and streaming platforms. Strong background in driving cost optimization, security hardening, and high-availability architectures for SaaS and data-intensive systems.
    </p>
  </section>

  <section style="margin-bottom: 25px;">
    <h2 style="font-size: 20px; font-weight: bold; margin-bottom: 10px; border-bottom: 1px solid #ccc; padding-bottom: 5px;">CORE SKILLS</h2>
    <p style="margin: 0;">
      AWS, Kubernetes (EKS), Terraform, ArgoCD, Argo Workflows, Kafka, Databricks, PostgreSQL, Aurora, Redis, Valkey, OpenSearch, CI/CD, Python, Bash, GitOps, FinOps, Observability, Security Engineering, IAM, VPC, Route53, Nginx, OpenVPN, Datadog, Squadcast, PagerDuty, SSM Parameter Store, Elasticache, S3, EC2, ECR
    </p>
  </section>

  <section style="margin-bottom: 25px;">
    <h2 style="font-size: 20px; font-weight: bold; margin-bottom: 10px; border-bottom: 1px solid #ccc; padding-bottom: 5px;">PROFESSIONAL EXPERIENCE</h2>
    
    <div style="margin-bottom: 20px;">
      <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
        <h3 style="font-size: 16px; font-weight: bold; margin: 0;">Teikametrics — Senior DevOps Engineer (Remote)</h3>
        <span style="font-size: 14px; font-weight: 600;">Nov 2022 – Present</span>
      </div>
      
      <div style="margin-top: 15px;">
        <h4 style="font-size: 15px; font-weight: bold; margin: 10px 0 5px 0;">DATABASE ENGINEERING</h4>
        <ul style="margin: 5px 0; padding-left: 20px;">
          <li>Led migration POC from RDS to Aurora PostgreSQL, designing parallel infra to benchmark cost and performance</li>
          <li>Engineered Aurora cluster topologies including provisioned and serverless writers/readers</li>
          <li>Implemented blue-green deployments for database downsizing ensuring zero downtime</li>
          <li>Tuned PostgreSQL parameters and implemented RDS Proxy to fix high concurrency issues</li>
          <li>Led major PostgreSQL version upgrades and resolved Flyway compatibility issues</li>
        </ul>
        
        <h4 style="font-size: 15px; font-weight: bold; margin: 10px 0 5px 0;">CLOUD INFRASTRUCTURE & NETWORKING</h4>
        <ul style="margin: 5px 0; padding-left: 20px;">
          <li>Architected staging OpenVPN infra and managed lifecycle including security patching</li>
          <li>Resolved intermittent VPN connectivity issues for secure access to private subnets</li>
          <li>Migrated traffic from Convox LB to centralized Nginx Ingress</li>
          <li>Implemented VPC peering, Route53 DNS, DMARC/DKIM, and security groups</li>
          <li>Implemented Terraform-based rate limiting on ingress</li>
        </ul>
        
        <h4 style="font-size: 15px; font-weight: bold; margin: 10px 0 5px 0;">KUBERNETES & GITOPS</h4>
        <ul style="margin: 5px 0; padding-left: 20px;">
          <li>Upgraded EKS clusters from v1.24 to v1.33 ensuring addon compatibility</li>
          <li>Implemented HA for ArgoCD, Argo Workflows, and Cluster Autoscaler</li>
          <li>Optimized Argo Workflows reliability and safely decommissioned legacy clusters</li>
        </ul>
        
        <h4 style="font-size: 15px; font-weight: bold; margin: 10px 0 5px 0;">DATA ENGINEERING & STREAMING</h4>
        <ul style="margin: 5px 0; padding-left: 20px;">
          <li>Migrated Databricks infra to Terraform with full state management</li>
          <li>Implemented service principals and Unity Catalog credentials</li>
          <li>Managed Kafka ecosystem including retention tuning and ACL governance</li>
          <li>Built Kafka lag monitoring in Datadog</li>
        </ul>
        
        <h4 style="font-size: 15px; font-weight: bold; margin: 10px 0 5px 0;">CI/CD & DEVOPS TOOLING</h4>
        <ul style="margin: 5px 0; padding-left: 20px;">
          <li>Built secure CI tunnels for integration tests to access private infra</li>
          <li>Fixed Java OOM pipeline failures via resource optimization</li>
          <li>Built Python CLIs tm-ctl and tf_bootstrap to standardize Terraform bootstrapping</li>
          <li>Enhanced TerraformCD tooling with safety controls and drift detection</li>
        </ul>
        
        <h4 style="font-size: 15px; font-weight: bold; margin: 10px 0 5px 0;">CACHING & RELIABILITY</h4>
        <ul style="margin: 5px 0; padding-left: 20px;">
          <li>Led Redis to Valkey migration with zero data loss</li>
          <li>Scaled Elasticache clusters for Prime Day traffic and tuned eviction policies</li>
        </ul>
        
        <h4 style="font-size: 15px; font-weight: bold; margin: 10px 0 5px 0;">FINOPS & COST OPTIMIZATION</h4>
        <ul style="margin: 5px 0; padding-left: 20px;">
          <li>Migrated RDS fleets to Graviton and GP3 for cost-performance gains</li>
          <li>Implemented aggressive S3 lifecycle rules to reduce storage costs</li>
          <li>Investigated AWS budget overruns and removed unused resources</li>
        </ul>
        
        <h4 style="font-size: 15px; font-weight: bold; margin: 10px 0 5px 0;">OBSERVABILITY & INCIDENT RESPONSE</h4>
        <ul style="margin: 5px 0; padding-left: 20px;">
          <li>Implemented Datadog monitoring for RDS, Kafka lag, and services</li>
          <li>Managed OpenSearch upgrades and Vector log pipelines</li>
          <li>Integrated alerts with Squadcast and PagerDuty for Sev1 automation</li>
        </ul>
        
        <h4 style="font-size: 15px; font-weight: bold; margin: 10px 0 5px 0;">SECURITY & ACCESS MANAGEMENT</h4>
        <ul style="margin: 5px 0; padding-left: 20px;">
          <li>Migrated secrets to AWS SSM Parameter Store</li>
          <li>Led emergency credential rotations for OpenSearch and Aiven</li>
          <li>Re-architected IAM and Databricks permissions with least-privilege model</li>
        </ul>
      </div>
    </div>
    
    <div style="margin-bottom: 20px;">
      <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
        <h3 style="font-size: 16px; font-weight: bold; margin: 0;">Infosys — Specialist Programmer, DevOps Lead (Bengaluru)</h3>
        <span style="font-size: 14px; font-weight: 600;">Jun 2020 – Nov 2022</span>
      </div>
      <p style="margin: 5px 0; font-size: 14px; font-style: italic;">Project: Finacle OePayments (Edgeverve) - Payment solutions (NEFT, RTGS, UPI) deployed at multiple banks</p>
      
      <div style="margin-top: 15px;">
        <h4 style="font-size: 15px; font-weight: bold; margin: 10px 0 5px 0;">DEVOPS & CI/CD</h4>
        <ul style="margin: 5px 0; padding-left: 20px;">
          <li>Developed CI/CD pipeline using GitLab CI for payment solutions</li>
          <li>Established DevOps processes and conducted team awareness programs</li>
          <li>Managed and coordinated with a team of 4 engineers, increasing team performance by 50%</li>
          <li>Spearheaded client delivery scripts and implementation support with Ansible and Bash</li>
        </ul>
        
        <h4 style="font-size: 15px; font-weight: bold; margin: 10px 0 5px 0;">SECURITY & COMPLIANCE</h4>
        <ul style="margin: 5px 0; padding-left: 20px;">
          <li>Devised licensing code and integrated it to internal license provider</li>
          <li>Supervised FOSS scan for licensing checks; developed component for automated FOSS scan on GitLab CI</li>
          <li>Enhanced efficiency by 250% with customized FOSS scan integration artifact with Black Duck</li>
          <li>Integrated Seeker Scan in K8s to do dynamic code scan (Interactive App Security Scan - IAST)</li>
          <li>Applied Security Vulnerability fixes in code to the process</li>
        </ul>
        
        <h4 style="font-size: 15px; font-weight: bold; margin: 10px 0 5px 0;">KUBERNETES & INFRASTRUCTURE</h4>
        <ul style="margin: 5px 0; padding-left: 20px;">
          <li>Organized infrastructure components like Redis, RabbitMQ, InfluxDB as well as Grafana on VM and as pods on K8s</li>
          <li>Utilized multiple environments for Kubernetes/Istio, DevOps and Test activities on On-Premise, AWS and GCP environment</li>
          <li>Created Bash/Linux utility to reset, refresh k8s area and image tagging utility to tag stable, latest build of apps</li>
          <li>Implemented Login-Logout Architecture design, and associated with JWT, OAuth 2.0</li>
          <li>Used Grafana SSO integration with in-house IDP and applied Grafana startup configuration and deployment</li>
        </ul>
        
        <h4 style="font-size: 15px; font-weight: bold; margin: 10px 0 5px 0;">PERFORMANCE OPTIMIZATION</h4>
        <ul style="margin: 5px 0; padding-left: 20px;">
          <li>Performed System Performance Testing with JMeter, Oracle/PG db, Redis and Redis Sentinel</li>
          <li>Maximized app performance using tools like JMeter, Grafana & Flame-Graph to achieve 3x TPS increase</li>
        </ul>
      </div>
    </div>
    
    <div style="margin-bottom: 20px;">
      <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
        <h3 style="font-size: 16px; font-weight: bold; margin: 0;">Infosys — System Engineer Specialist, Java Spring-Boot Developer (Bengaluru)</h3>
        <span style="font-size: 14px; font-weight: 600;">May 2019 – Jun 2020</span>
      </div>
      <p style="margin: 5px 0; font-size: 14px; font-style: italic;">Project: Nexus (CareFirst BlueCross BlueShield) - Healthcare re-imaging product with latest tech stack and cloud implementation</p>
      
      <div style="margin-top: 15px;">
        <ul style="margin: 5px 0; padding-left: 20px;">
          <li>Created Spring Boot app to implement business logic using Kafka and Postgres DB</li>
          <li>Independently developed Kafka POC in initial phase of project to implement Kafka library</li>
          <li>Implemented logging and log masking</li>
          <li>Proficiently developed Apigee integrations</li>
          <li>Developed Authorization Architecture with Open Policy Agent and Kubernetes</li>
          <li>Participated in internal hackathon</li>
        </ul>
      </div>
    </div>
  </section>

  <section style="margin-bottom: 25px;">
    <h2 style="font-size: 20px; font-weight: bold; margin-bottom: 10px; border-bottom: 1px solid #ccc; padding-bottom: 5px;">EDUCATION</h2>
    <div style="margin-bottom: 10px;">
      <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
        <h3 style="font-size: 16px; font-weight: bold; margin: 0;">B.Tech in Computer Science</h3>
        <span style="font-size: 14px; font-weight: 600;">2015 – 2019</span>
      </div>
      <p style="margin: 0; font-size: 14px;">SRM Institute of Science & Technology, Chennai, India</p>
      <p style="margin: 5px 0 0 0; font-size: 14px;">CGPA: 8.92</p>
    </div>
  </section>

  <section style="margin-bottom: 25px;">
    <h2 style="font-size: 20px; font-weight: bold; margin-bottom: 10px; border-bottom: 1px solid #ccc; padding-bottom: 5px;">AWARDS & RECOGNITIONS</h2>
    <ul style="margin: 5px 0; padding-left: 20px;">
      <li>Certificate of Excellence - STG Ninja Award for Individual Performance (2022)</li>
      <li>ESOP for Outstanding Performance (2021-2022)</li>
      <li>Insta Award for contribution towards Nexus, CareFirst (2019)</li>
    </ul>
  </section>

  <section style="margin-bottom: 25px;">
    <h2 style="font-size: 20px; font-weight: bold; margin-bottom: 10px; border-bottom: 1px solid #ccc; padding-bottom: 5px;">CERTIFICATIONS</h2>
    <ul style="margin: 5px 0; padding-left: 20px;">
      <li>AWS Certified Developer - Associate (2020)</li>
    </ul>
  </section>

</div>

<style>
@media print {
  .resume-container {
    max-width: 100%;
    padding: 0;
  }
  a {
    color: #000 !important;
    text-decoration: none !important;
  }
}
</style>
