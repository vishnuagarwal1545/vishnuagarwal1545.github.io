---
layout: post
title: CloudWatch Database Insights vs. RDS Performance Insights - A Complete Comparison
date: 2025-01-07
description: A comprehensive guide comparing CloudWatch Database Insights and RDS Performance Insights, including pricing, features, and migration considerations
tags: aws, cloudwatch, rds, database, devops, performance-monitoring
categories: devops, aws
---

# CloudWatch Database Insights vs. RDS Performance Insights - A Complete Comparison

If you're using Amazon RDS or Aurora databases, you've likely encountered both RDS Performance Insights and CloudWatch Database Insights. AWS is transitioning from Performance Insights to CloudWatch Database Insights, with Performance Insights being deprecated (end-of-life target: June 30, 2026).

This guide provides a comprehensive comparison to help you understand the differences, costs, and migration path. Whether you're evaluating which monitoring solution to use, planning a migration, or trying to optimize costs, this article covers everything you need to know.

## TL;DR

- **CloudWatch Database Insights** provides a free Standard tier (7-day retention, similar to PI free tier) and a paid Advanced tier (15-month retention with SQL analytics and execution plans), though some features previously free in PI (like execution plan capture for Oracle/SQL Server) now require the Advanced paid tier.
- **RDS Performance Insights** is being deprecated (June 30, 2026) in favor of CloudWatch Database Insights, which offers enhanced fleet monitoring and CloudWatch integration but costs more (~$9/vCPU/month for Advanced vs ~$4.76/vCPU/month for PI paid tier).
- **Cost:**
  - **DB Insights Standard**: Free, ~7 days retention.
  - **DB Insights Advanced**: Paid, ~15 months retention, priced per vCPU-hour (~$0.0125/vCPU-hr ≈ ~$9/vCPU/mo). Example: 2 vCPU ≈ ~$18/mo per instance.
  - **Performance Insights (PI) paid tier**: Paid, 15-24 months retention. Historically cheaper for same retention (~$4.76/mo for 2 vCPU at 15 months), but PI console is being sunset.
- **Status**: AWS is transitioning from PI to CloudWatch Database Insights. PI's console experience and flexible retention are being deprecated (end-of-life target: June 30, 2026 per AWS comms). Expect charges to roll under CloudWatch after that date.
- **Recommendation**: Use DB Insights Standard by default. Enable Advanced only for critical databases needing >7d history and advanced analysis.

## Quick Start: How to Access Database Insights

Database Insights is accessible through the AWS CloudWatch console:

1. Navigate to **CloudWatch** in the AWS Console
2. In the left navigation, expand **Insights** and select **Database Insights**
3. You'll see all your RDS and Aurora databases that have Database Insights enabled
4. Click on any database to view its performance metrics

Standard mode is enabled by default for new instances, so you should see your databases listed automatically. If you don't see a database, ensure it's a supported engine (MySQL, PostgreSQL, MariaDB, Oracle, SQL Server) and that it was created recently (older instances may need to be updated).

## Pricing

### DB Insights Standard

- **Cost**: $0
- **Retention**: ~7 days
- **Suitable for**: Day-to-day triage, short-lived incidents, basic load analysis

Reference: [Amazon CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/)

### DB Insights Advanced

- **Cost**: ~$0.0125 per vCPU-hour (~$9/vCPU/mo). Example: 2 vCPU × 730 hrs × $0.0125 ≈ $18.25/mo.
- **Retention**: ~15 months
- **Unlocks**: Fleet views, deeper SQL/lock analysis, richer historical analysis

Reference: [Amazon CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/)

### Performance Insights (Legacy Reference)

- **Free tier**: Short retention (varies by engine/region)
- **Paid tier**: Historically 15–24 months retention at lower cost vs DBI Advanced (e.g., ~$4.76/mo for 2 vCPU at 15 months)
- **Deprecation**: Console/experience being sunset; costs may appear under CloudWatch after EOL

**Note**: Exact pricing varies by region and instance type; verify in AWS pricing pages and your bill.

## Cost Examples (DB Insights Advanced)

Understanding the cost implications is crucial when deciding whether to use Advanced mode. Here are some practical examples:

### Pricing Summary

| Instance Type  | vCPU Count | Monthly Cost (Advanced) |
| -------------- | ---------- | ----------------------- |
| db.t3.micro    | 2          | ~$18.25                 |
| db.t3.small    | 2          | ~$18.25                 |
| db.m6g.large   | 2          | ~$18.25                 |
| db.m6g.xlarge  | 4          | ~$36.50                 |
| db.m6g.2xlarge | 8          | ~$73.00                 |
| db.r8g.2xlarge | 8          | ~$73.00                 |

_Note: Standard mode is free for all instance types._

### Assumptions:

- Rate: $0.0125 per vCPU-hour (provisioned instances). Month = 730 hours.
- vCPU counts: m6g.2xlarge = 8 vCPU; r8g.2xlarge = 8 vCPU.
- Standard mode costs $0.
- Multi-AZ writer consists of a primary and a standby instance; some billing views count both instances. Verify in your bill whether the standby is charged for Database Insights.
- **Aurora Serverless v2**: Charged per Aurora Capacity Unit (ACU) per hour instead of vCPU. Check AWS pricing for current ACU rates.

### Example A: RDS setup with Multi-AZ writer (m6g.2xlarge) and Single-AZ reader (m6g.2xlarge)

- Instances considered for Advanced billing:
  - Writer Multi-AZ: primary (8 vCPU) (billing only counts the active writer not standby)
  - Reader Single-AZ: 1 instance (8 vCPU)
- Total vCPU = 8 + 8 = 16 vCPU
- Monthly cost ≈ 16 vCPU × $0.0125/vCPU-hr × 730 hr = **$146.00**

### Example B: Aurora provisioned cluster with 2 instances r8g.2xlarge (1 writer + 1 reader)

- Total vCPU = 8 + 8 = 16 vCPU
- Monthly cost ≈ 16 vCPU × $0.0125/vCPU-hr × 730 hr ≈ **$146.00**

## Feature Comparison Matrix

| Feature                                        | RDS Performance Insights Free Tier | DB Insights Standard | RDS Performance Insights Paid Tier     | DB Insights Advanced                    |
| ---------------------------------------------- | ---------------------------------- | -------------------- | -------------------------------------- | --------------------------------------- |
| **Cost**                                       | Free                               | Free                 | ~$4.76/mo (2 vCPU, 15-month retention) | ~$9/vCPU/month (~$0.0125/vCPU-hour)     |
| **Data Retention**                             | 7 days                             | 7 days               | 1-24 months (configurable)             | 15 months                               |
| **Database Load Metrics**                      | ☑ Yes                             | ☑ Yes               | ☑ Yes                                 | ☑ Yes                                  |
| **Wait State Analysis**                        | ☑ Yes                             | ☑ Yes               | ☑ Yes                                 | ☑ Yes                                  |
| **Top SQL Statements**                         | ☑ Yes                             | ☑ Basic             | ☑ Yes                                 | ☑ Enhanced with analytics              |
| **SQL Query Analytics**                        | ❌ No                              | ❌ No                | ☑ Yes                                 | ☑ Yes                                  |
| **Execution Plan Capture**                     | ☑ Yes (Oracle, SQL Server)        | ❌ No                | ☑ Yes (Oracle, SQL Server)            | ☑ Yes (Oracle, SQL Server, PostgreSQL) |
| **On-Demand Analysis**                         | ❌ No                              | ❌ No                | ☑ Yes (PostgreSQL, MySQL)             | ☑ Yes (PostgreSQL, MySQL)              |
| **Proactive Recommendations**                  | ❌ No                              | ❌ No                | ❌ No                                  | ☑ Yes                                  |
| **Lock Diagnostics**                           | ❌ No                              | ❌ No                | ❌ No                                  | ☑ Yes (Aurora PostgreSQL)              |
| **Fleet-Level Monitoring**                     | ❌ No                              | ❌ No                | ❌ No                                  | ☑ Yes                                  |
| **Session Analysis**                           | ☑ Basic                           | ☑ Basic             | ☑ Enhanced                            | ☑ Enhanced                             |
| **Historical Trend Analysis**                  | ☑ Limited (7 days)                | ☑ Limited (7 days)  | ☑ Yes (up to 24 months)               | ☑ Yes (15 months)                      |
| **CloudWatch Application Signals Integration** | ❌ No                              | ❌ No                | ❌ No                                  | ☑ Yes                                  |
| **OS Process Visibility**                      | ❌ No                              | ❌ No                | ❌ No                                  | ☑ Yes (with Enhanced Monitoring)       |
| **Metric Granularity**                         | 1-second intervals                 | 1-second intervals   | 1-second intervals                     | 1-second intervals                      |
| **Customizable Alarms**                        | ☑ Yes                             | ☑ Yes               | ☑ Yes                                 | ☑ Yes                                  |

## Features - Standard vs Advanced Detailed Comparison

### CloudWatch Database Insights Standard Mode (Free)

**Cost**: $0 (included in AWS Free Tier)

**Data Retention:**

- 7 days rolling history of database load metrics
- Real-time and recent historical data only
- Suitable for immediate troubleshooting and short-term incident analysis

**Core Monitoring Features (Included):**

**Database Load Analysis:**

- Database load metric with time series visualization
- Breakdown of database load by wait states/categories
- Identify top wait events impacting database performance
- Database time vs. CPU time comparison

**Basic SQL Insights:**

- Top SQL statements by database load contribution
- SQL query text display (limited context)
- Basic filtering capabilities

**Instance-Level Metrics:**

- Per-instance database performance drilldowns
- Basic resource overlay (CPU utilization tied to database load)

**Session Monitoring:**

- Active session count overview
- Basic session-level insights

### CloudWatch Database Insights Advanced Mode (Paid)

**Cost**: ~$0.0125 per vCPU-hour (≈ $9 per vCPU per month)

- Example: 2 vCPU instance = ~$18.25/month
- For Aurora Serverless v2: Charged per Aurora Capacity Unit (ACU) per hour
- Pricing varies by AWS region

**Data Retention:**

- 15 months of performance data history
- Long-term trend analysis and capacity planning
- Seasonal pattern identification

**All Standard Mode Features PLUS:**

**Advanced SQL Query Analytics:**

- Detailed SQL performance insights with query-level metrics
- SQL query analytics dashboard with comprehensive filtering
- Query dimensions (database, user, client host, etc.)
- Query parameter analysis
- Top SQL by multiple dimensions (load, calls, latency, rows processed)
- SQL text normalization and pattern analysis
- Query performance trends over extended periods

**Execution Plan Capture:**

- RDS for Oracle: Full execution plan capture and analysis
- RDS for SQL Server: Execution plan visibility
- Aurora PostgreSQL: Query execution plan support
- Helps identify inefficient query patterns and optimization opportunities

**On-Demand Analysis:**

- Available for Aurora PostgreSQL, Aurora MySQL, and RDS for PostgreSQL
- Performance bottleneck identification for selected time periods
- Automated recommendations for performance improvements
- Root cause analysis tools

**Proactive Recommendations:**

- AI-powered alerts for impending database performance issues
- Predictive analytics for potential availability problems
- Performance optimization suggestions

**Lock Diagnostics & Analysis:**

- Aurora PostgreSQL: Detailed lock tree visualization
- Blocking and blocked session identification
- Lock wait analysis
- Deadlock detection and reporting

**Fleet-Level Monitoring:**

- Monitor multiple databases from a single dashboard
- Cross-database performance comparison
- Sort and filter databases by load, anomalies, and recent spikes
- Fleet-wide anomaly detection

**Enhanced Correlation & Integration:**

- Integration with CloudWatch Application Signals for end-to-end application-to-database tracing
- Correlation between database metrics, logs, and events
- Unified observability experience within CloudWatch

**Extended Historical Analysis:**

- Long-term performance trending
- Capacity planning insights
- Seasonal pattern recognition
- Historical incident analysis (beyond 7 days)

**OS Process-Level Visibility:**

- When Enhanced Monitoring is enabled, provides OS-level process insights
- Correlation between database load and system-level processes

## Infrastructure as Code: Terraform Configuration

> **Note**: This section is for readers using Terraform for infrastructure management. If you're using the AWS Console, CloudFormation, or other tools, you can enable Database Insights through those interfaces. The concepts remain the same, but the syntax will differ.

### Default Behavior

**CloudWatch Database Insights Standard mode is the default** for RDS and Aurora instances. No Terraform configuration is required to enable Standard mode—it's automatically enabled at no cost with 7-day retention.

### Enabling Standard Mode (Explicit)

If you want to explicitly set Standard mode in Terraform:

```hcl
resource "aws_db_instance" "example" {
  # ... other configurations ...

  database_insights_mode = "standard"  # Free, 7-day retention

  # ... other configurations ...
}
```

### Enabling Advanced Mode

**Important**: As of the current AWS implementation, enabling Database Insights Advanced mode via Terraform **still requires Performance Insights to be enabled** with a retention period set. This is a current dependency that may change as AWS completes the migration.

To enable Advanced mode, you need both:

```hcl
resource "aws_db_instance" "example" {
  # ... other configurations ...

  # Required: Performance Insights must be enabled for Advanced mode
  performance_insights_enabled          = true
  performance_insights_retention_period = 456  # 15 months (to match Database Insights Advanced retention)
  performance_insights_kms_key_id       = "arn:aws:kms:region:account-id:key/key-id"  # Optional but recommended

  # Enable Database Insights Advanced mode
  database_insights_mode = "advanced"  # Paid, ~$9/vCPU/month, 15-month retention

  # ... other configurations ...
}
```

**For Aurora clusters**, configure at the cluster level:

```hcl
resource "aws_rds_cluster" "example" {
  # ... other configurations ...

  # Performance Insights configuration
  performance_insights_enabled          = true
  performance_insights_retention_period = 456  # 15 months (to match Database Insights Advanced retention)
  performance_insights_kms_key_id       = "arn:aws:kms:region:account-id:key/key-id"

  # Database Insights Advanced mode
  database_insights_mode = "advanced"

  # ... other configurations ...
}
```

### Module Configuration Recommendations

1. **Add `database_insights_mode` variable to module configuration:**

   - Add to `variables.tf` with default value `null` (which results in Standard mode by default)
   - Pass through to Aurora/RDS module resources
   - Document the parameter with cost implications

2. **Performance Insights variables (currently still required for Advanced mode):**
   - Keep `performance_insights_enabled` variable (required for Advanced mode)
   - Keep `performance_insights_kms_key_id` variable (recommended for encryption)
   - Keep `performance_insights_retention_period` variable (should be set to 15 months/456 days for Advanced mode to match Database Insights retention)
   - Document that these are currently required when `database_insights_mode = "advanced"`

### Migration Notes

- **Standard mode**: No Performance Insights configuration needed—it's the default
- **Advanced mode**: Currently requires `performance_insights_enabled = true` and `performance_insights_retention_period = 456` (15 months) to match Database Insights Advanced retention
- **Future changes**: Monitor AWS documentation as this dependency may be removed as the migration progresses

### Enabling via AWS Console

If you're not using Terraform, you can enable Database Insights through the AWS Console:

1. **Standard Mode (Default)**: No action required—automatically enabled for new RDS/Aurora instances
2. **Advanced Mode**:
   - Navigate to your RDS instance or Aurora cluster in the AWS Console
   - Go to the "Monitoring" tab
   - Enable "Performance Insights" (currently required for Advanced mode)
   - Set retention period to 15 months (456 days)
   - Enable "Database Insights" and select "Advanced" mode

For detailed console instructions, refer to the [Getting Started with Database Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Insights-Database-getting-started.html) documentation.

## When to Use What: Decision Guide

### Use Database Insights Standard (Free) When:

- You need basic performance monitoring for day-to-day operations
- 7 days of retention is sufficient for your troubleshooting needs
- You're monitoring development, staging, or non-critical databases
- You want to minimize costs while still having visibility
- You're just getting started with database performance monitoring

### Use Database Insights Advanced (Paid) When:

- You need long-term historical analysis (beyond 7 days)
- You're troubleshooting complex performance issues requiring detailed SQL analytics
- You manage multiple databases and need fleet-level monitoring
- You require execution plan analysis for query optimization
- You need proactive recommendations and predictive analytics
- You're running critical production databases that justify the cost

### If You're Currently Using Performance Insights:

- **Free tier users**: Migrate to Database Insights Standard (no cost change, similar features)
- **Paid tier users**: Plan migration to Database Insights Advanced before June 2026
- **Evaluate costs**: Advanced tier costs more (~$9/vCPU/month vs ~$4.76/vCPU/month), but offers additional features like fleet monitoring

## Migration Recommendations

1. **Start with Standard Mode**: Enable CloudWatch Database Insights Standard mode for all databases. It's free and provides 7 days of retention, which is sufficient for most day-to-day operations.

2. **Evaluate Advanced Mode**: Consider enabling Advanced mode for:

   - Production databases requiring long-term historical analysis
   - Databases with complex performance issues needing detailed SQL analytics
   - Multi-database environments that benefit from fleet-level monitoring
   - Critical systems requiring proactive recommendations

3. **Plan Migration Timeline**: With Performance Insights being deprecated by June 30, 2026, plan your migration well in advance to avoid service disruption. Start testing Database Insights in non-production environments first.

4. **Cost Optimization**: Monitor your usage and costs. Use Standard mode for non-critical databases and Advanced mode selectively for databases that truly need extended retention and advanced features. Review your bill regularly to ensure you're not over-provisioning Advanced mode.

5. **Test Before Migrating**: If you're currently using Performance Insights paid tier, test Database Insights Advanced in a staging environment to understand the feature differences and cost implications before migrating production databases.

## References

### Official AWS Documentation

- [Database Insights User Guide](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Insights-Database.html) - Comprehensive guide on using Database Insights
- [Getting Started with Database Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Insights-Database-getting-started.html) - Setup and configuration guide
- [Database Insights SQL Query Analytics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Insights-Database-SQL.html) - SQL query analysis features
- [Database Insights Fleet Management](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Insights-Database-Fleet.html) - Fleet-level monitoring capabilities

### RDS Performance Insights (Legacy)

- [Using Performance Insights](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PerfInsights.html) - Overview and depreciation timeline
- [Performance Insights Metrics](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_PerfInsights.UsingDashboard.html#USER_PerfInsights.UsingDashboard.Metrics) - Metrics reference

### Pricing Information

- [Amazon CloudWatch Pricing](https://aws.amazon.com/cloudwatch/pricing/) - Official pricing page (includes Database Insights section)
- [Performance Insights Pricing](https://aws.amazon.com/rds/performance-insights/pricing/) - Legacy PI pricing (for comparison)
- [CloudWatch Billing and Cost Management](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/monitoring_aws_usage.html) - How to analyze and optimize costs

### Migration and Transition Resources

- [AWS re:Post - RDS Performance Insights to CloudWatch Database Insights migration](https://repost.aws/topics/cloudwatch-database-insights) - Community Q&A on migration
- [AWS re:Post - Transitioning from RDS Performance Insights](https://repost.aws/knowledge-center/rds-performance-insights-cloudwatch-database-insights) - Transition guide article

### Feature-Specific Documentation

- [CloudWatch Application Signals](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Application-Signals.html) - Application-to-database correlation
- [Enhanced Monitoring for RDS](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_Monitoring.OS.html) - OS-level metrics integration
- [Aurora PostgreSQL Lock Diagnostics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch-Insights-Database-Locks.html) - Lock analysis features

### Additional Resources

- [AWS Database Blog - Database Insights](https://aws.amazon.com/blogs/database/category/database/amazon-rds/cloudwatch-database-insights/) - Latest updates and best practices
- [AWS Support Center](https://support.aws.amazon.com/) - Support and resources for AWS services

---

## Conclusion

CloudWatch Database Insights represents the future of database performance monitoring on AWS. While it comes with a higher price tag for the Advanced tier compared to Performance Insights, it offers enhanced features like fleet monitoring, better CloudWatch integration, and proactive recommendations.

### Key Takeaways

1. **Start with Standard Mode**: The free Standard tier is enabled by default and provides 7 days of retention—sufficient for most day-to-day monitoring needs.

2. **Upgrade Selectively**: Enable Advanced mode only for databases that truly need extended retention (15 months) and advanced features like SQL analytics, execution plans, and fleet monitoring.

3. **Plan Your Migration**: With Performance Insights being deprecated in June 2026, begin planning your migration now. Test Database Insights in non-production environments first to understand feature differences and cost implications.

4. **Monitor Costs**: Advanced mode costs approximately $9 per vCPU per month. For a typical 2 vCPU instance, that's about $18/month. Review your usage regularly to ensure you're not over-provisioning.

5. **Leverage Fleet Monitoring**: If you manage multiple databases, Advanced mode's fleet-level monitoring can provide significant value by allowing you to monitor and compare performance across all your databases from a single dashboard.

The transition from Performance Insights to Database Insights is inevitable. By understanding the differences, costs, and features now, you can make informed decisions and ensure a smooth migration before the June 2026 deadline.

---

_Last updated: January 7, 2025_
