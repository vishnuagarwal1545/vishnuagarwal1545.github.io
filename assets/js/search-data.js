// get the ninja-keys element
const ninja = document.querySelector('ninja-keys');

// add the home and posts menu items
ninja.data = [{
    id: "nav-about",
    title: "about",
    section: "Navigation",
    handler: () => {
      window.location.href = "/";
    },
  },{id: "nav-projects",
          title: "projects",
          description: "A showcase of my personal and professional projects.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/projects/";
          },
        },{id: "nav-resume",
          title: "resume",
          description: "Vishnu Agarwal - Senior DevOps Engineer with 6+ years of experience in cloud infrastructure, Kubernetes, and automation.",
          section: "Navigation",
          handler: () => {
            window.location.href = "/resume/";
          },
        },{id: "nav-blog",
          title: "blog",
          description: "",
          section: "Navigation",
          handler: () => {
            window.location.href = "/blog/";
          },
        },{id: "post-autoscaling-on-request-rate-with-keda-and-datadog-what-the-docs-don-39-t-tell-you",
        
          title: "Autoscaling on Request Rate with KEDA and Datadog - What the Docs Don&#39;t...",
        
        description: "Hands-on notes from replacing per-app Datadog external-metric HPAs with KEDA on EKS. How a Datadog trigger really turns into a replica count, a unit bug that made every service scale to max, and what the tests showed.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2026/keda-datadog-autoscaling-lessons/";
          
        },
      },{id: "post-moving-from-cluster-autoscaler-to-karpenter-on-eks-field-notes-from-a-dev-cluster-migration",
        
          title: "Moving from Cluster Autoscaler to Karpenter on EKS - Field Notes from a...",
        
        description: "A step-by-step test of replacing Cluster Autoscaler with Karpenter on an EKS cluster. What changed at each step, what broke (DaemonSets), and what consolidation, pool limits and disruption controls actually did.",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2026/karpenter-migration-field-notes/";
          
        },
      },{id: "post-cloudwatch-database-insights-vs-rds-performance-insights-a-complete-comparison",
        
          title: "CloudWatch Database Insights vs. RDS Performance Insights - A Complete Comparison",
        
        description: "A comprehensive guide comparing CloudWatch Database Insights and RDS Performance Insights, including pricing, features, and migration considerations",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2026/cloudwatch-database-insights-vs-rds-performance-insights/";
          
        },
      },{id: "post-welcome-to-my-blog",
        
          title: "Welcome to My Blog",
        
        description: "An introduction to my blog and what you can expect to find here",
        section: "Posts",
        handler: () => {
          
            window.location.href = "/blog/2026/welcome-to-my-blog/";
          
        },
      },{id: "projects-project-template",
          title: 'Project Template',
          description: "A template for creating new project entries",
          section: "Projects",handler: () => {
              window.location.href = "/projects/1_project/";
            },},{
        id: 'social-email',
        title: 'email',
        section: 'Socials',
        handler: () => {
          window.open("mailto:%76%69%73%68%6E%75%61%67%61%72%77%61%6C%31%35%34%35@%67%6D%61%69%6C.%63%6F%6D", "_blank");
        },
      },{
        id: 'social-linkedin',
        title: 'LinkedIn',
        section: 'Socials',
        handler: () => {
          window.open("https://www.linkedin.com/in/vishnuagarwal1545", "_blank");
        },
      },{
      id: 'light-theme',
      title: 'Change theme to light',
      description: 'Change the theme of the site to Light',
      section: 'Theme',
      handler: () => {
        setThemeSetting("light");
      },
    },
    {
      id: 'dark-theme',
      title: 'Change theme to dark',
      description: 'Change the theme of the site to Dark',
      section: 'Theme',
      handler: () => {
        setThemeSetting("dark");
      },
    },
    {
      id: 'system-theme',
      title: 'Use system default theme',
      description: 'Change the theme of the site to System Default',
      section: 'Theme',
      handler: () => {
        setThemeSetting("system");
      },
    },];
