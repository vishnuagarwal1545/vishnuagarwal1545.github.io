#!/usr/bin/env python3
"""
Generate ATS-compliant PDF resume from HTML
"""

try:
    from xhtml2pdf import pisa
except ImportError:
    print("xhtml2pdf not available, trying alternative method...")
    pisa = None

from pathlib import Path

# ATS-compliant resume HTML
resume_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Vishnu Agarwal - Resume</title>
    <style>
        @page {
            size: letter;
            margin: 0.75in;
        }
        body {
            font-family: Arial, Helvetica, sans-serif;
            font-size: 11pt;
            line-height: 1.4;
            color: #000;
            margin: 0;
            padding: 0;
        }
        header {
            text-align: center;
            margin-bottom: 20pt;
            border-bottom: 2pt solid #000;
            padding-bottom: 10pt;
        }
        h1 {
            font-size: 20pt;
            font-weight: bold;
            margin: 0;
            padding: 0;
        }
        h2 {
            font-size: 14pt;
            font-weight: bold;
            margin: 15pt 0 8pt 0;
            border-bottom: 1pt solid #666;
            padding-bottom: 3pt;
        }
        h3 {
            font-size: 12pt;
            font-weight: bold;
            margin: 10pt 0 5pt 0;
        }
        h4 {
            font-size: 11pt;
            font-weight: bold;
            margin: 8pt 0 3pt 0;
        }
        p {
            margin: 5pt 0;
            text-align: justify;
        }
        ul {
            margin: 5pt 0;
            padding-left: 20pt;
        }
        li {
            margin: 3pt 0;
        }
        .header-info {
            font-size: 10pt;
            margin: 3pt 0;
        }
        .section {
            margin-bottom: 15pt;
        }
        .job-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 5pt;
        }
        .job-title {
            font-weight: bold;
        }
        .job-date {
            font-weight: 600;
        }
        .project-name {
            font-style: italic;
            font-size: 10pt;
            margin: 3pt 0;
        }
        a {
            color: #000;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <header>
        <h1>VISHNU AGARWAL</h1>
        <p style="font-size: 12pt; font-weight: 600; margin: 5pt 0;">Senior DevOps Engineer | Remote</p>
        <p class="header-info">Email: vishnuagarwal1545@gmail.com | Phone: +91 9884213512</p>
        <p class="header-info">Website: https://vishnuagarwal1545.github.io</p>
    </header>

    <section class="section">
        <h2>PROFESSIONAL SUMMARY</h2>
        <p>Senior DevOps Engineer with 6+ years of experience in cloud infrastructure, platform reliability, and large-scale automation. Proven expertise in AWS, Kubernetes, Terraform, CI/CD, database engineering, and streaming platforms. Strong background in driving cost optimization, security hardening, and high-availability architectures for SaaS and data-intensive systems.</p>
    </section>

    <section class="section">
        <h2>CORE SKILLS</h2>
        <p>AWS, Kubernetes (EKS), Terraform, ArgoCD, Argo Workflows, Kafka, Databricks, PostgreSQL, Aurora, Redis, Valkey, OpenSearch, CI/CD, Python, Bash, GitOps, FinOps, Observability, Security Engineering, IAM, VPC, Route53, Nginx, OpenVPN, Datadog, Squadcast, PagerDuty, SSM Parameter Store, Elasticache, S3, EC2, ECR, GitLab CI, Ansible, Node.js, Java, Spring Boot</p>
    </section>

    <section class="section">
        <h2>PROFESSIONAL EXPERIENCE</h2>
        
        <div style="margin-bottom: 15pt;">
            <div class="job-header">
                <h3 class="job-title">Teikametrics — Senior DevOps Engineer (Remote)</h3>
                <span class="job-date">Nov 2022 – Present</span>
            </div>
            
            <div style="margin-top: 10pt;">
                <h4>DATABASE ENGINEERING</h4>
                <ul>
                    <li>Led migration POC from RDS to Aurora PostgreSQL, designing parallel infra to benchmark cost and performance</li>
                    <li>Engineered Aurora cluster topologies including provisioned and serverless writers/readers</li>
                    <li>Implemented blue-green deployments for database downsizing ensuring zero downtime</li>
                    <li>Tuned PostgreSQL parameters and implemented RDS Proxy to fix high concurrency issues</li>
                    <li>Led major PostgreSQL version upgrades and resolved Flyway compatibility issues</li>
                </ul>
                
                <h4>CLOUD INFRASTRUCTURE & NETWORKING</h4>
                <ul>
                    <li>Architected staging OpenVPN infra and managed lifecycle including security patching</li>
                    <li>Resolved intermittent VPN connectivity issues for secure access to private subnets</li>
                    <li>Migrated traffic from Convox LB to centralized Nginx Ingress</li>
                    <li>Implemented VPC peering, Route53 DNS, DMARC/DKIM, and security groups</li>
                    <li>Implemented Terraform-based rate limiting on ingress</li>
                </ul>
                
                <h4>KUBERNETES & GITOPS</h4>
                <ul>
                    <li>Upgraded EKS clusters from v1.24 to v1.33 ensuring addon compatibility</li>
                    <li>Implemented HA for ArgoCD, Argo Workflows, and Cluster Autoscaler</li>
                    <li>Optimized Argo Workflows reliability and safely decommissioned legacy clusters</li>
                </ul>
                
                <h4>DATA ENGINEERING & STREAMING</h4>
                <ul>
                    <li>Migrated Databricks infra to Terraform with full state management</li>
                    <li>Implemented service principals and Unity Catalog credentials</li>
                    <li>Managed Kafka ecosystem including retention tuning and ACL governance</li>
                    <li>Built Kafka lag monitoring in Datadog</li>
                </ul>
                
                <h4>CI/CD & DEVOPS TOOLING</h4>
                <ul>
                    <li>Built secure CI tunnels for integration tests to access private infra</li>
                    <li>Fixed Java OOM pipeline failures via resource optimization</li>
                    <li>Built Python CLIs tm-ctl and tf_bootstrap to standardize Terraform bootstrapping</li>
                    <li>Enhanced TerraformCD tooling with safety controls and drift detection</li>
                </ul>
                
                <h4>CACHING & RELIABILITY</h4>
                <ul>
                    <li>Led Redis to Valkey migration with zero data loss</li>
                    <li>Scaled Elasticache clusters for Prime Day traffic and tuned eviction policies</li>
                </ul>
                
                <h4>FINOPS & COST OPTIMIZATION</h4>
                <ul>
                    <li>Migrated RDS fleets to Graviton and GP3 for cost-performance gains</li>
                    <li>Implemented aggressive S3 lifecycle rules to reduce storage costs</li>
                    <li>Investigated AWS budget overruns and removed unused resources</li>
                </ul>
                
                <h4>OBSERVABILITY & INCIDENT RESPONSE</h4>
                <ul>
                    <li>Implemented Datadog monitoring for RDS, Kafka lag, and services</li>
                    <li>Managed OpenSearch upgrades and Vector log pipelines</li>
                    <li>Integrated alerts with Squadcast and PagerDuty for Sev1 automation</li>
                </ul>
                
                <h4>SECURITY & ACCESS MANAGEMENT</h4>
                <ul>
                    <li>Migrated secrets to AWS SSM Parameter Store</li>
                    <li>Led emergency credential rotations for OpenSearch and Aiven</li>
                    <li>Re-architected IAM and Databricks permissions with least-privilege model</li>
                </ul>
            </div>
        </div>
        
        <div style="margin-bottom: 15pt;">
            <div class="job-header">
                <h3 class="job-title">Infosys — Specialist Programmer, DevOps Lead (Bengaluru)</h3>
                <span class="job-date">Jun 2020 – Nov 2022</span>
            </div>
            <p class="project-name">Project: Finacle OePayments (Edgeverve) - Payment solutions (NEFT, RTGS, UPI) deployed at multiple banks</p>
            
            <div style="margin-top: 10pt;">
                <h4>DEVOPS & CI/CD</h4>
                <ul>
                    <li>Developed CI/CD pipeline using GitLab CI for payment solutions</li>
                    <li>Established DevOps processes and conducted team awareness programs</li>
                    <li>Managed and coordinated with a team of 4 engineers, increasing team performance by 50%</li>
                    <li>Spearheaded client delivery scripts and implementation support with Ansible and Bash</li>
                </ul>
                
                <h4>SECURITY & COMPLIANCE</h4>
                <ul>
                    <li>Devised licensing code and integrated it to internal license provider</li>
                    <li>Supervised FOSS scan for licensing checks; developed component for automated FOSS scan on GitLab CI</li>
                    <li>Enhanced efficiency by 250% with customized FOSS scan integration artifact with Black Duck</li>
                    <li>Integrated Seeker Scan in K8s to do dynamic code scan (Interactive App Security Scan - IAST)</li>
                    <li>Applied Security Vulnerability fixes in code to the process</li>
                </ul>
                
                <h4>KUBERNETES & INFRASTRUCTURE</h4>
                <ul>
                    <li>Organized infrastructure components like Redis, RabbitMQ, InfluxDB as well as Grafana on VM and as pods on K8s</li>
                    <li>Utilized multiple environments for Kubernetes/Istio, DevOps and Test activities on On-Premise, AWS and GCP environment</li>
                    <li>Created Bash/Linux utility to reset, refresh k8s area and image tagging utility to tag stable, latest build of apps</li>
                    <li>Implemented Login-Logout Architecture design, and associated with JWT, OAuth 2.0</li>
                    <li>Used Grafana SSO integration with in-house IDP and applied Grafana startup configuration and deployment</li>
                </ul>
                
                <h4>PERFORMANCE OPTIMIZATION</h4>
                <ul>
                    <li>Performed System Performance Testing with JMeter, Oracle/PG db, Redis and Redis Sentinel</li>
                    <li>Maximized app performance using tools like JMeter, Grafana & Flame-Graph to achieve 3x TPS increase</li>
                </ul>
            </div>
        </div>
        
        <div style="margin-bottom: 15pt;">
            <div class="job-header">
                <h3 class="job-title">Infosys — System Engineer Specialist, Java Spring-Boot Developer (Bengaluru)</h3>
                <span class="job-date">May 2019 – Jun 2020</span>
            </div>
            <p class="project-name">Project: Nexus (CareFirst BlueCross BlueShield) - Healthcare re-imaging product with latest tech stack and cloud implementation</p>
            
            <div style="margin-top: 10pt;">
                <ul>
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

    <section class="section">
        <h2>EDUCATION</h2>
        <div style="margin-bottom: 10pt;">
            <div class="job-header">
                <h3 class="job-title">B.Tech in Computer Science</h3>
                <span class="job-date">2015 – 2019</span>
            </div>
            <p style="margin: 3pt 0;">SRM Institute of Science & Technology, Chennai, India</p>
            <p style="margin: 3pt 0;">CGPA: 8.92</p>
        </div>
    </section>

    <section class="section">
        <h2>AWARDS & RECOGNITIONS</h2>
        <ul>
            <li>Certificate of Excellence - STG Ninja Award for Individual Performance (2022)</li>
            <li>ESOP for Outstanding Performance (2021-2022)</li>
            <li>Insta Award for contribution towards Nexus, CareFirst (2019)</li>
        </ul>
    </section>

    <section class="section">
        <h2>CERTIFICATIONS</h2>
        <ul>
            <li>AWS Certified Developer - Associate (2020)</li>
        </ul>
    </section>

</body>
</html>
"""

def generate_pdf():
    """Generate PDF resume"""
    output_path = Path("assets/pdf/resume.pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if pisa:
        with open(output_path, "w+b") as result_file:
            pisa_status = pisa.CreatePDF(resume_html, dest=result_file)
            if pisa_status.err:
                print(f"Error generating PDF: {pisa_status.err}")
                return False
        print(f"PDF generated successfully: {output_path}")
        return True
    else:
        # Fallback: copy existing ATS PDF
        import shutil
        source = Path("resume_content/Vishnu_Agarwal_Senior_DevOps_ATS.pdf")
        if source.exists():
            shutil.copy(source, output_path)
            print(f"Copied existing ATS PDF to: {output_path}")
            return True
        else:
            print("Error: No PDF generation method available")
            return False

if __name__ == "__main__":
    generate_pdf()
