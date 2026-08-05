import json
import os
import threading
from typing import List, Dict, Any

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)

USERS_FILE = os.path.join(DATA_DIR, "users.json")
JOBS_FILE = os.path.join(DATA_DIR, "jobs.json")
APPLICATIONS_FILE = os.path.join(DATA_DIR, "applications.json")

db_lock = threading.Lock()

def _load_file(filepath: str, default: Any) -> Any:
    if not os.path.exists(filepath):
        return default
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def _save_file(filepath: str, data: Any):
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving to {filepath}: {e}")

def load_users() -> List[Dict[str, Any]]:
    with db_lock:
        users = _load_file(USERS_FILE, [])
        if not users:
            users = [
                {
                    "id": 1,
                    "name": "Laiba Taj",
                    "email": "laibataj1306@gmail.com",
                    "password": "acab wfla vmlk pfnl",
                    "role": "manager"
                },
                {
                    "id": 2,
                    "name": "Laiba Candidate",
                    "email": "laiba.candidate@gmail.com",
                    "password": "laiba",
                    "role": "user"
                },
                {
                    "id": 3,
                    "name": "Demo User",
                    "email": "user@gmail.com",
                    "password": "user123",
                    "role": "user"
                },
                {
                    "id": 4,
                    "name": "Demo Manager",
                    "email": "manager@gmail.com",
                    "password": "manager123",
                    "role": "manager"
                }
            ]
            _save_file(USERS_FILE, users)
        return users

def save_users(users: List[Dict[str, Any]]):
    with db_lock:
        _save_file(USERS_FILE, users)

def load_jobs() -> List[Dict[str, Any]]:
    with db_lock:
        jobs = _load_file(JOBS_FILE, [])
        if not jobs or len(jobs) < 10:
            jobs = [
                {
                    "id": 0,
                    "title": "Frontend Developer",
                    "description": "About the Role:\nAs a Frontend Developer at Razorpay, you will build and optimize user interfaces for our merchant dashboards. You will work with product teams and designers to turn Figma mockups into clean, high-performance React components.\n\nKey Responsibilities:\n- Build and maintain reusable, responsive React components and frontend utility libraries.\n- Optimize application loading times, resource footprint, and cross-browser rendering speeds.\n- Integrate REST/GraphQL APIs and handle asynchronous application workflows.\n- Collaborating with UX developers to enforce design consistency.\n\nRequirements & Qualifications:\n- 2+ years of experience in frontend engineering using React.js and Javascript (ES6+).\n- Solid mastery of HTML5, CSS3, Flexbox/Grid, and modern TailwindCSS frameworks.\n- Experience with state-management systems (Redux Toolkit, Recoil, or React Context).\n- Familiarity with Git, modern bundling tools (Vite, Webpack), and client-side performance profiling.",
                    "location": "Bengaluru, KA",
                    "salary": 650000,
                    "job_type": "Full Time",
                    "skills": "React, JavaScript, TailwindCSS, HTML/CSS",
                    "company_name": "Razorpay",
                    "expiry_date": "2026-08-15"
                },
                {
                    "id": 1,
                    "title": "Full Stack Python Developer",
                    "description": "About the Role:\nAs a Full Stack Developer at Zomato, you will work across our backend service layers and frontend apps. You will build and scale APIs that handle millions of live delivery tracking coordinates, restaurant database queries, and payment processing loops daily.\n\nKey Responsibilities:\n- Develop scalable REST APIs using FastAPI and Python.\n- Design database structures, optimize PostgreSQL queries, and handle Redis key-value caching.\n- Build administrative and guest portals using React.js and Tailwind CSS.\n- Write robust unit and integration tests to guarantee code coverage and deployment reliability.\n\nRequirements & Qualifications:\n- 3+ years of professional backend or full-stack software development experience.\n- Strong command of Python, FastAPI/Django, and asynchronous programming (asyncio).\n- Deep familiarity with PostgreSQL design, indexing, and transactional isolation.\n- Working knowledge of containerization (Docker) and microservices orchestrations.",
                    "location": "Mumbai, MH",
                    "salary": 800000,
                    "job_type": "Full Time",
                    "skills": "Python, FastAPI, React, PostgreSQL",
                    "company_name": "Zomato",
                    "expiry_date": "2026-08-01"
                },
                {
                    "id": 2,
                    "title": "UI/UX Designer",
                    "description": "About the Role:\nAs a UI/UX Designer at Swiggy, you will own the user experience for various delivery and commerce micro-flows. You will design flows, construct high-fidelity mockups, and build visual prototypes that make food ordering seamless for millions of users.\n\nKey Responsibilities:\n- Research user behavior patterns, draft wireframes, and design end-to-end user journeys.\n- Maintain and scale the core design tokens and components in Figma.\n- Conduct user testing loops to iterate on navigation efficiency and checkout conversion.\n- Deliver design specification files and work alongside frontend engineers during visual audits.\n\nRequirements & Qualifications:\n- 2+ years of experience as a product designer or UI/UX specialist for high-traffic mobile apps.\n- Masterful command of Figma, including advanced prototyping, auto-layouts, and variables.\n- Portfolio showcasing real-world designs, problem-solving reasoning, and final visual layouts.\n- Passion for user-centric design principles, hierarchy, micro-interactions, and accessibility.",
                    "location": "Bengaluru, KA",
                    "salary": 550000,
                    "job_type": "Contract",
                    "skills": "Figma, UI Design, Prototyping, Wireframing",
                    "company_name": "Swiggy",
                    "expiry_date": "2026-08-20"
                },
                {
                    "id": 3,
                    "title": "Data Analyst",
                    "description": "About the Role:\nAs a Data Analyst at Paytm, you will transform database transactions into insights. You will compile data warehouses, build business dashboards, and work with leadership to highlight metrics on payments growth and merchant acquisition.\n\nKey Responsibilities:\n- Build and maintain interactive dashboards using Tableau or PowerBI for management overview.\n- Write optimized SQL scripts to clean, transform, and join multi-million row transaction tables.\n- Conduct statistical audits to identify transaction trends, user retention spikes, and churn risks.\n- Automate recurring reports using Python and cron configurations.\n\nRequirements & Qualifications:\n- 1.5+ years of experience in data analytics, business intelligence, or data engineering roles.\n- Expertise in PostgreSQL / MySQL query optimization and analytical functions.\n- Strong hands-on proficiency with Tableau, PowerBI, or comparable dashboard engines.\n- Basic scripting proficiency in Python (Pandas, NumPy) for data parsing and cleansing.",
                    "location": "Noida, UP",
                    "salary": 500000,
                    "job_type": "Full Time",
                    "skills": "SQL, Python, Excel, Tableau, PowerBI",
                    "company_name": "Paytm",
                    "expiry_date": "2026-07-28"
                },
                {
                    "id": 4,
                    "title": "Backend Engineer (Go/Python)",
                    "description": "About the Role:\nAs a Backend Engineer at Zepto, you will build the technology powering 10-minute delivery loops. You will build order management routing engines, real-time inventory synchronizations, and warehouse dispatch APIs that run at sub-millisecond latencies.\n\nKey Responsibilities:\n- Write backend microservices in Go and Python with highly concurrent request handlers.\n- Design pub/sub communication channels using RabbitMQ, Apache Kafka, or Redis Streams.\n- Optimize query caching layers to minimize database roundtrips.\n- Deploy services onto Kubernetes clusters and debug distributed runtime logs.\n\nRequirements & Qualifications:\n- 3+ years of backend engineering experience with high-load web architectures.\n- High proficiency in Go (Golang) or Python, with strong OOP and functional programming skills.\n- Mastery of SQL/NoSQL databases (PostgreSQL, MongoDB, DynamoDB) and caching patterns (Redis).\n- Solid knowledge of network layer protocols, HTTP/2, WebSockets, and gRPC integrations.",
                    "location": "Mumbai, MH",
                    "salary": 900000,
                    "job_type": "Full Time",
                    "skills": "Go, Python, Redis, Docker, Microservices",
                    "company_name": "Zepto",
                    "expiry_date": "2026-08-12"
                },
                {
                    "id": 5,
                    "title": "DevOps Engineer",
                    "description": "About the Role:\nAs a DevOps Engineer at Cred, you will maintain the uptime, security, and automation infrastructure of our production clusters. You will build CI/CD deployment automation pipelines, maintain cloud security groups, and monitor system metrics.\n\nKey Responsibilities:\n- Deploy, maintain, and upgrade Docker containers across multiple cloud environments.\n- Build and secure deployment pipelines using GitHub Actions, Jenkins, or GitLab CI/CD.\n- Write and manage infrastructure templates using Terraform or AWS CloudFormation.\n- Configure log aggregators and server metrics using Prometheus, Grafana, and ELK Stack.\n\nRequirements & Qualifications:\n- 2+ years of experience in site reliability engineering, cloud administration, or DevOps.\n- Deep familiarity with cloud provider suites (specifically Amazon Web Services / AWS).\n- Hands-on expertise managing production Kubernetes clusters (EKS) and Helm packages.\n- Strong command of Bash scripting and Linux server administration protocols.",
                    "location": "Bengaluru, KA",
                    "salary": 750000,
                    "job_type": "Full Time",
                    "skills": "AWS, Kubernetes, Docker, CI/CD, Terraform",
                    "company_name": "Cred",
                    "expiry_date": "2026-08-02"
                },
                {
                    "id": 6,
                    "title": "Mobile App Developer (Flutter/React Native)",
                    "description": "About the Role:\nAs a Mobile Developer at PhonePe, you will construct user interfaces, offline-first transaction ledgers, and secure transaction workflows inside our Android and iOS applications.\n\nKey Responsibilities:\n- Write clean, structured mobile client code using Flutter and Dart.\n- Build fluid UI animations, custom widgets, and responsive screen flows.\n- Optimize application bundles, image caching, and battery consumption parameters.\n- Integrate native platform device drivers, camera scan engines, and location services.\n\nRequirements & Qualifications:\n- 2+ years of production mobile app engineering experience utilizing Flutter or React Native.\n- Clear conceptual understanding of mobile architectures (BLoC, Provider, MVC, MVVM).\n- Familiarity with releasing apps onto the Google Play Store and Apple App Store.\n- Experience using secure local storage libraries (SQLite, Hive, Encrypted Shared Preferences).",
                    "location": "Bengaluru, KA",
                    "salary": 700000,
                    "job_type": "Full Time",
                    "skills": "Flutter, Dart, React Native, iOS, Android",
                    "company_name": "PhonePe",
                    "expiry_date": "2026-08-25"
                },
                {
                    "id": 7,
                    "title": "Machine Learning Engineer",
                    "description": "About the Role:\nAs a Machine Learning Engineer at TCS, you will develop machine learning pipelines for predictive modeling, text parsing (NLP), and customer classification systems for global client systems.\n\nKey Responsibilities:\n- Build, validate, and train regression, classification, and neural model architectures.\n- Clean raw unstructured text datasets, configure tokenizers, and construct embedding models.\n- Collaborate with data engineers to deploy models onto serverless endpoints.\n- Monitor production model outputs for predictions shift and re-training cycles.\n\nRequirements & Qualifications:\n- 3+ years of analytical software programming with focus on machine learning and statistics.\n- Proficient coding skills in Python and ML frameworks (PyTorch, TensorFlow, Scikit-Learn).\n- Strong knowledge of database queries, data cleaning libraries (Pandas), and MLflow.\n- Experience with natural language processing pipelines (HuggingFace transformers) is a plus.",
                    "location": "Pune, MH",
                    "salary": 950000,
                    "job_type": "Full Time",
                    "skills": "Python, PyTorch, TensorFlow, Scikit-Learn",
                    "company_name": "Tata Consultancy Services (TCS)",
                    "expiry_date": "2026-08-30"
                },
                {
                    "id": 8,
                    "title": "Cloud Infrastructure Architect",
                    "description": "About the Role:\nAs a Cloud Infrastructure Architect at Wipro, you will design enterprise migration roadmaps, cloud safety structures, and directory services for international accounts.\n\nKey Responsibilities:\n- Architect highly available cloud solutions spanning Azure, AWS, and private data hubs.\n- Establish Virtual Networks (VPCs), identity access groups (IAM), and firewalls.\n- Advise development groups on serverless architectures, storage tiers, and cluster sizing.\n- Audit resource runsheets to formulate cost reduction paths.\n\nRequirements & Qualifications:\n- 5+ years of experience designing and managing cloud infrastructures.\n- Industry certifications: Azure Solutions Architect, AWS Certified Solutions Architect, or equivalent.\n- Strong command of networking protocols: DNS, VPN gateways, subnets, routing tables, and firewalls.\n- Hands-on familiarity using Terraform configurations for multi-cloud deployments.",
                    "location": "Hyderabad, TS",
                    "salary": 1200000,
                    "job_type": "Full Time",
                    "skills": "Azure, GCP, Cloud Security, Enterprise Architecture",
                    "company_name": "Wipro",
                    "expiry_date": "2026-07-20"
                },
                {
                    "id": 9,
                    "title": "Cybersecurity Analyst",
                    "description": "About the Role:\nAs a Cybersecurity Analyst at HCL Tech, you will guard infrastructure nodes from threats, configure firewalls, audit access configurations, and deploy intrusion monitoring tools.\n\nKey Responsibilities:\n- Review access logs, analyze security events, and coordinate responses to alerts.\n- Execute manual vulnerability scans and run network penetration tests.\n- Audit user permission groups to enforce least-privileged authentication guidelines.\n- Construct automated threat alerts inside SIEM tools (Splunk, Wazuh, Microsoft Sentinel).\n\nRequirements & Qualifications:\n- 2+ years of experience in network administration, system audit, or security analysis.\n- Standard security certificates (CompTIA Security+, CEH, or CISSP) are highly valued.\n- Masterful command of network troubleshooting commands, Wireshark, and Kali Linux toolkits.\n- Working familiarity with identity directories (Active Directory, Okta OAuth configurations).",
                    "location": "Chennai, TN",
                    "salary": 600000,
                    "job_type": "Full Time",
                    "skills": "Penetration Testing, Kali Linux, SIEM, Firewalls",
                    "company_name": "HCL Tech",
                    "expiry_date": "2026-08-18"
                },
                {
                    "id": 10,
                    "title": "Product Manager",
                    "description": "About the Role:\nAs a Product Manager at Flipkart, you will define features and drive development lifecycle for product checkout checkout systems, cart logistics, and recommendation algorithms.\n\nKey Responsibilities:\n- Design the product vision and draft features specifications.\n- Work closely with user researchers and design groups to detail interaction wireframes.\n- Coordinate development sprints with design and backend teams inside Agile loops.\n- Audit conversion numbers to implement design iterations.\n\nRequirements & Qualifications:\n- 3+ years of software product management experience, preferably in high-growth e-commerce domains.\n- Proven track record of launching consumer products from initial scoping to rollout.\n- Strong analytical thinking; experience using data queries (SQL) and analytics dashboards.\n- Exceptional communication skills; comfortable presenting to technical teams and business directors.",
                    "location": "Bengaluru, KA",
                    "salary": 1200000,
                    "job_type": "Full Time",
                    "skills": "Product Roadmap, Agile/Scrum, User Analytics, Jira",
                    "company_name": "Flipkart",
                    "expiry_date": "2026-08-04"
                },
                {
                    "id": 11,
                    "title": "Software Engineering Intern",
                    "description": "About the Role:\nAs a Software Engineering Intern at Infosys, you will work on team sprints, write tests, fix dashboard bugs, and learn to deploy enterprise code.\n\nKey Responsibilities:\n- Help write unit testing scripts inside JUnit, PyTest, or Jest frameworks.\n- Fix minor frontend styling bugs and update administrative dashboard panels.\n- Review system documents and compile architectural diagrams.\n- Participate in design sprints, peer code reviews, and project meetings.\n\nRequirements & Qualifications:\n- Currently enrolled in or recently graduated from a Computer Science or Engineering degree.\n- Good conceptual understanding of object-oriented programming (OOP) in Java, Python, or C++.\n- Familiarity with Git command workflows and branch structures.\n- Enthusiastic learner with a desire to solve technical software problems.",
                    "location": "Mysuru, KA",
                    "salary": 240000,
                    "job_type": "Internship",
                    "skills": "Java, Python, Git, Basic Data Structures",
                    "company_name": "Infosys",
                    "expiry_date": "2026-08-09"
                },
                {
                    "id": 12,
                    "title": "Systems Engineer",
                    "description": "About the Role:\nAs a Systems Engineer at Reliance Jio, you will monitor production servers, manage local directories, configure backups, and troubleshoot corporate networks.\n\nKey Responsibilities:\n- Configure Linux/Windows virtual machines, install security patches, and monitor system performance.\n- Manage network storage configurations, automated database backups, and recover test setups.\n- Oversee internal directories (Active Directory) and set user permissions.\n- Resolve internal infrastructure alerts, router errors, and database connection issues.\n\nRequirements & Qualifications:\n- 1.5+ years of experience in system administration, IT support, or server maintenance.\n- Masterful command of Linux administration, shell scripting, and service configuration.\n- Deep familiarity with directory systems (Active Directory), DNS, and DHCP server options.\n- Working command of cloud environments (AWS, Azure) and hypervisors (VMWare, VirtualBox).",
                    "location": "Navi Mumbai, MH",
                    "salary": 450000,
                    "job_type": "Full Time",
                    "skills": "Linux, Server Admin, Active Directory, Networking",
                    "company_name": "Reliance Jio",
                    "expiry_date": "2026-08-05"
                },
                {
                    "id": 13,
                    "title": "Embedded Systems Developer",
                    "description": "About the Role:\nAs an Embedded Developer at Tata Motors, you will design firmware, code hardware protocols, and compile controllers inside vehicle systems.\n\nKey Responsibilities:\n- Write firmware code in C/C++ for automotive microcontrollers and system boards.\n- Establish communication layers utilizing CAN bus, I2C, SPI, and UART interfaces.\n- Perform manual board testing using hardware debugging tools and scopes.\n- Optimize firmware layouts to maintain low power states.\n\nRequirements & Qualifications:\n- 3+ years of firmware design experience for electronic micro-systems.\n- Mastery of C/C++ coding practices and bare-metal programming.\n- Experience using automotive network models, CAN standards, and debugging tools.\n- Familiarity working under RTOS architectures and configuring bootloaders.",
                    "location": "Pune, MH",
                    "salary": 600000,
                    "job_type": "Full Time",
                    "skills": "C/C++, Microcontrollers, RTOS, CAN bus",
                    "company_name": "Tata Motors",
                    "expiry_date": "2026-07-31"
                },
                {
                    "id": 14,
                    "title": "QA Automation Engineer",
                    "description": "About the Role:\nAs a QA Automation Engineer at Ola Cabs, you will build automated end-to-end integration tests, report software bugs, and verify deployment reliability.\n\nKey Responsibilities:\n- Write end-to-end regression tests using Selenium, Playwright, or Cypress.\n- Integrate automated test suites with Jenkins/GitHub Actions CI/CD pipelines.\n- Perform system load audits to identify endpoint bottleneck bottlenecks.\n- Track database bugs, log reports, and collaborate with engineers to resolve issues.\n\nRequirements & Qualifications:\n- 2+ years of QA testing experience with strong focus on automation scripting.\n- Masterful coding skills in Java, Python, or Javascript for test design.\n- Strong familiarity testing API endpoints utilizing Postman/REST-Assured tools.\n- Working knowledge of SQL queries to inspect transaction states.",
                    "location": "Bengaluru, KA",
                    "salary": 500000,
                    "job_type": "Full Time",
                    "skills": "Selenium, Java, Playwright, E2E Testing",
                    "company_name": "Ola Cabs",
                    "expiry_date": "2026-08-22"
                },
                {
                    "id": 15,
                    "title": "UI Engineer",
                    "description": "About the Role:\nAs a UI Engineer at Razorpay, you will bridge the gap between design and technology. You will write high-performance HTML/CSS layouts, micro-interactions, and visual transitions inside our merchant checkout templates.\n\nKey Responsibilities:\n- Collaborate with product designers to build visual design systems.\n- Write clean, modular CSS/Tailwind layouts that perform at scale.\n- Build animations and smooth screen flows.",
                    "location": "Bengaluru, KA",
                    "salary": 550000,
                    "job_type": "Full Time",
                    "skills": "React, CSS, HTML5, TailwindCSS",
                    "company_name": "Razorpay",
                    "expiry_date": "2026-08-28"
                },
                {
                    "id": 16,
                    "title": "Backend Python Engineer",
                    "description": "About the Role:\nAs a Backend Python Developer at Zomato, you will develop robust business APIs. You will deploy code on cloud clusters, optimize PostgreSQL tables, and handle Redis caches.\n\nKey Responsibilities:\n- Maintain Django backend routing services and user access tables.\n- Write efficient raw SQL scripts for complex operations.\n- Set up Redis queues for food delivery order flows.",
                    "location": "Gurugram, HR",
                    "salary": 720000,
                    "job_type": "Full Time",
                    "skills": "Python, Django, PostgreSQL, Redis",
                    "company_name": "Zomato",
                    "expiry_date": "2026-08-19"
                },
                {
                    "id": 17,
                    "title": "Product Designer",
                    "description": "About the Role:\nAs a Product Designer at Swiggy, you will own the user experience for our delivery apps. You will build wireframes, design screen flows, and test navigation patterns.\n\nKey Responsibilities:\n- Establish wireframes and draft user flow diagrams.\n- Maintain and build component design systems in Figma.\n- Validate layouts with engineering teams.",
                    "location": "Bengaluru, KA",
                    "salary": 680000,
                    "job_type": "Full Time",
                    "skills": "Figma, UX Design, Prototyping, Wireframing",
                    "company_name": "Swiggy",
                    "expiry_date": "2026-08-25"
                },
                {
                    "id": 18,
                    "title": "SRE Engineer",
                    "description": "About the Role:\nAs an SRE at Zepto, you will ensure high availability for 10-minute delivery apps. You will write Ansible playbooks, manage Kubernetes instances, and configure AWS groups.\n\nKey Responsibilities:\n- Set up automated scaling groups on cloud networks.\n- Monitor traffic loads using Prometheus and Grafana.\n- Solve database latency bottlenecks.",
                    "location": "Mumbai, MH",
                    "salary": 850000,
                    "job_type": "Full Time",
                    "skills": "AWS, Kubernetes, Ansible, Grafana",
                    "company_name": "Zepto",
                    "expiry_date": "2026-08-16"
                },
                {
                    "id": 19,
                    "title": "Software Engineer (L4)",
                    "description": "About the Role:\nAs a Software Engineer at Google, you will work on core search backend models. You will write clean C++/Python services, maintain API layers, and scale database pipelines.\n\nKey Responsibilities:\n- Design scalable backend architectures for global scale requests.\n- Conduct deep-dive performance analysis on distributed platforms.\n- Coordinate projects across multi-functional engineering teams.",
                    "location": "Bengaluru, KA",
                    "salary": 1400000,
                    "job_type": "Full Time",
                    "skills": "C++, Python, Algorithms, Distributed Systems",
                    "company_name": "Google",
                    "expiry_date": "2026-08-27"
                },
                {
                    "id": 20,
                    "title": "Site Reliability Specialist",
                    "description": "About the Role:\nAs an SRS at Google, you will own deployment runtimes and cluster scaling scripts.\n\nKey Responsibilities:\n- Write Python/Go automation tools for cluster management.\n- Manage Google Cloud Platform networks and safety groups.\n- Audit service level targets.",
                    "location": "Hyderabad, TS",
                    "salary": 1500000,
                    "job_type": "Full Time",
                    "skills": "Google Cloud, Python, Kubernetes, Automation",
                    "company_name": "Google",
                    "expiry_date": "2026-08-24"
                },
                {
                    "id": 21,
                    "title": "Production Engineer",
                    "description": "About the Role:\nAs a Production Engineer at Meta, you will maintain reliability for millions of concurrent server sessions.\n\nKey Responsibilities:\n- Optimize container orchestrations using Docker and Kubernetes.\n- Develop infrastructure scripts in Go and Python.\n- Direct system failover drills.",
                    "location": "Bengaluru, KA",
                    "salary": 1300000,
                    "job_type": "Full Time",
                    "skills": "Go, Python, Docker, Kubernetes, Linux",
                    "company_name": "Meta",
                    "expiry_date": "2026-08-29"
                },
                {
                    "id": 22,
                    "title": "Azure Cloud Consultant",
                    "description": "About the Role:\nAs a Cloud Consultant at Microsoft, you will guide enterprise migration architectures on Azure.\n\nKey Responsibilities:\n- Architect highly available cloud solutions spanning Azure cloud services.\n- Write Infrastructure as Code templates using Bicep/Terraform.\n- Conduct safety reviews.",
                    "location": "Hyderabad, TS",
                    "salary": 1150000,
                    "job_type": "Full Time",
                    "skills": "Azure, Cloud Architecture, Terraform, Consulting",
                    "company_name": "Microsoft",
                    "expiry_date": "2026-08-22"
                },
                {
                    "id": 23,
                    "title": "Solutions Architect (AWS)",
                    "description": "About the Role:\nAs a Solutions Architect at AWS, you will advise clients on scalable serverless designs and storage options.\n\nKey Responsibilities:\n- Advise development teams on sizing containers and Lambda endpoints.\n- Construct secure multi-tenant network VPC designs.\n- Formulate cloud budget plans.",
                    "location": "Bengaluru, KA",
                    "salary": 1250000,
                    "job_type": "Full Time",
                    "skills": "AWS, Serverless, Cloud Architecture, Cost Optimization",
                    "company_name": "Amazon",
                    "expiry_date": "2026-08-26"
                }
            ]
            _save_file(JOBS_FILE, jobs)
        
        modified = False
        for idx, job in enumerate(jobs):
            if "id" not in job:
                job["id"] = idx
                modified = True
        if modified:
            _save_file(JOBS_FILE, jobs)
            
        return jobs

def save_jobs(jobs: List[Dict[str, Any]]):
    with db_lock:
        _save_file(JOBS_FILE, jobs)

def load_applications() -> List[Dict[str, Any]]:
    with db_lock:
        apps = _load_file(APPLICATIONS_FILE, [])
        if not apps or len(apps) < 3:
            apps = [
                {
                    "id": 1,
                    "job_id": 0,
                    "resume_url": "https://drive.google.com/file/d/1abc/view",
                    "cover_letter": "I am a skilled React.js developer eager to join Razorpay.",
                    "job_title": "Frontend Developer",
                    "company_name": "Razorpay",
                    "applied_at": "2026-08-05T14:10:00Z",
                    "status": "Selected",
                    "ats_score": 98,
                    "candidate_email": "laiba.candidate@gmail.com",
                    "candidate_name": "Laiba Candidate",
                    "skills": "React, JavaScript, TailwindCSS, HTML/CSS"
                },
                {
                    "id": 2,
                    "job_id": 2,
                    "resume_url": "https://drive.google.com/file/d/3abc/view",
                    "cover_letter": "I have experience designing mobile user interfaces in Figma.",
                    "job_title": "UI/UX Designer",
                    "company_name": "Swiggy",
                    "applied_at": "2026-08-05T11:30:00Z",
                    "status": "Interviewing",
                    "ats_score": 88,
                    "candidate_email": "laiba.candidate@gmail.com",
                    "candidate_name": "Laiba Candidate",
                    "skills": "Figma, UI Design, Prototyping, Wireframing"
                },
                {
                    "id": 3,
                    "job_id": 4,
                    "resume_url": "https://drive.google.com/file/d/4abc/view",
                    "cover_letter": "I build concurrent and optimized Go APIs.",
                    "job_title": "Backend Engineer (Go/Python)",
                    "company_name": "Zepto",
                    "applied_at": "2026-08-05T09:15:00Z",
                    "status": "Pending",
                    "ats_score": 72,
                    "candidate_email": "laiba.candidate@gmail.com",
                    "candidate_name": "Laiba Candidate",
                    "skills": "Go, Python, Redis, Docker, Microservices"
                },
                {
                    "id": 4,
                    "job_id": 5,
                    "resume_url": "https://drive.google.com/file/d/5abc/view",
                    "cover_letter": "SRE and Kubernetes cluster specialist.",
                    "job_title": "DevOps Engineer",
                    "company_name": "Cred",
                    "applied_at": "2026-08-04T16:45:00Z",
                    "status": "Rejected",
                    "ats_score": 58,
                    "candidate_email": "laiba.candidate@gmail.com",
                    "candidate_name": "Laiba Candidate",
                    "skills": "AWS, Kubernetes, Docker, CI/CD, Terraform"
                },
                {
                    "id": 5,
                    "job_id": 1,
                    "resume_url": "https://drive.google.com/file/d/2abc/view",
                    "cover_letter": "I want to work on Python full stack at Zomato.",
                    "job_title": "Full Stack Python Developer",
                    "company_name": "Zomato",
                    "applied_at": "2026-08-05T12:00:00Z",
                    "status": "Interviewing",
                    "ats_score": 85,
                    "candidate_email": "user@gmail.com",
                    "candidate_name": "Demo Candidate",
                    "skills": "Python, FastAPI, React, PostgreSQL"
                },
                {
                    "id": 6,
                    "job_id": 6,
                    "resume_url": "https://drive.google.com/file/d/6abc/view",
                    "cover_letter": "Experienced Flutter mobile coder.",
                    "job_title": "Mobile App Developer (Flutter/React Native)",
                    "company_name": "PhonePe",
                    "applied_at": "2026-08-05T08:30:00Z",
                    "status": "Pending",
                    "ats_score": 78,
                    "candidate_email": "user@gmail.com",
                    "candidate_name": "Demo Candidate",
                    "skills": "Flutter, Dart, React Native, iOS, Android"
                }
            ]
            _save_file(APPLICATIONS_FILE, apps)
        return apps

def save_applications(applications: List[Dict[str, Any]]):
    with db_lock:
        _save_file(APPLICATIONS_FILE, applications)
