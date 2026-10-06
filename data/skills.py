"""
Categorized, truth-grounded technical skill taxonomy.
Reorganized around engineering domains and target roles (AI Engineer, ML Engineer, MLOps Engineer).
"""

SKILL_CATEGORIES = [
    {
        "category": "Languages",
        "icon": "fas fa-code",
        "skills": [
            {"name": "Python (Advanced)", "devicon": "devicon-python-plain"},
            {"name": "SQL (Oracle, PostgreSQL)", "devicon": "devicon-postgresql-plain"},
            {"name": "Java", "devicon": "devicon-java-plain"},
            {"name": "Bash / Shell", "devicon": "devicon-linux-plain"},
        ]
    },
    {
        "category": "Machine Learning & Deep Learning",
        "icon": "fas fa-brain",
        "skills": [
            {"name": "PyTorch", "devicon": "devicon-pytorch-plain"},
            {"name": "Scikit-Learn", "devicon": "devicon-scikitlearn-plain"},
            {"name": "Transformers (Hugging Face)", "devicon": "fas fa-network-wired"},
            {"name": "YOLO (Ultralytics v8/v11)", "devicon": "fas fa-camera"},
            {"name": "OpenCV", "devicon": "devicon-opencv-plain"},
            {"name": "TensorFlow / Keras", "devicon": "devicon-tensorflow-original"},
            {"name": "CNN Architectures", "devicon": "fas fa-layer-group"},
            {"name": "Feature Engineering & Scaling", "devicon": "fas fa-chart-line"},
        ]
    },
    {
        "category": "Generative AI & Agentic Systems",
        "icon": "fas fa-robot",
        "skills": [
            {"name": "RAG (Retrieval-Augmented Generation)", "devicon": "fas fa-magnifying-glass"},
            {"name": "LangChain", "devicon": "fas fa-link"},
            {"name": "LangGraph", "devicon": "fas fa-diagram-project"},
            {"name": "AI Agents & Multi-Agent DAGs", "devicon": "fas fa-diagram-project"},
            {"name": "Qdrant Vector DB", "devicon": "fas fa-database"},
            {"name": "Cross-Encoder Reranking", "devicon": "fas fa-arrow-down-short-wide"},
            {"name": "Prompt Versioning & Evaluation", "devicon": "fas fa-check-double"},
        ]
    },
    {
        "category": "MLOps & Orchestration",
        "icon": "fas fa-cogs",
        "skills": [
            {"name": "MLflow (Tracking & Registry)", "devicon": "fas fa-flask"},
            {"name": "DVC (Data Version Control)", "devicon": "devicon-git-plain"},
            {"name": "DagsHub", "devicon": "fas fa-code-branch"},
            {"name": "Apache Airflow (DAGs)", "devicon": "devicon-apacheairflow-plain"},
            {"name": "Docker", "devicon": "devicon-docker-plain"},
            {"name": "Kubernetes (Minikube)", "devicon": "devicon-kubernetes-plain"},
            {"name": "Jenkins CI/CD", "devicon": "devicon-jenkins-line"},
        ]
    },
    {
        "category": "Backend & API Engineering",
        "icon": "fas fa-server",
        "skills": [
            {"name": "FastAPI", "devicon": "devicon-fastapi-plain"},
            {"name": "Flask", "devicon": "devicon-flask-original"},
            {"name": "RESTful API Design", "devicon": "fas fa-network-wired"},
            {"name": "Selenium Automation", "devicon": "devicon-selenium-original"},
            {"name": "Postman API Testing", "devicon": "devicon-postman-plain"},
        ]
    },
    {
        "category": "Data Engineering & Storage",
        "icon": "fas fa-database",
        "skills": [
            {"name": "Apache Spark (PySpark)", "devicon": "devicon-apachespark-plain"},
            {"name": "MongoDB (NoSQL)", "devicon": "devicon-mongodb-plain"},
            {"name": "Snowflake Data Cloud", "devicon": "fas fa-snowflake"},
            {"name": "Oracle Database", "devicon": "devicon-oracle-original"},
            {"name": "Pandas & NumPy", "devicon": "devicon-pandas-plain"},
            {"name": "Hadoop HDFS", "devicon": "devicon-hadoop-plain"},
            {"name": "ETL Pipeline Validation", "devicon": "fas fa-filter"},
        ]
    },
    {
        "category": "Cloud & DevOps",
        "icon": "fas fa-cloud",
        "skills": [
            {"name": "Microsoft Azure", "devicon": "devicon-azure-plain"},
            {"name": "Azure DevOps", "devicon": "devicon-azure-plain"},
            {"name": "Git & GitHub", "devicon": "devicon-github-original"},
            {"name": "Linux / Unix Administration", "devicon": "devicon-linux-plain"},
            {"name": "Render Deployment", "devicon": "fas fa-cloud-arrow-up"},
        ]
    }
]
