"""
Structured portfolio project data.
All information is grounded in verified repositories and actual technical implementations.
Prioritized for maximum recruiter and technical interviewer impact.
"""

PROJECTS = [
    {
        "id": "design-karo",
        "title": "DesignKaro",
        "subtitle": "Interactive System Design & Distributed Architecture Simulator",
        "tagline": "Discrete-Event Traffic Simulation (1M QPS), Anti-Pattern Rule Engine & Socratic AI Mentor",
        "category": "systems",
        "featured": True,
        "badge": "Flagship Systems Project",
        "image": "images/BihariBLogger2.png",
        "github_url": "https://github.com/mithilesh1627/DesignKaro",
        "demo_url": "",
        "demo_label": "",
        "problem_statement": (
            "Traditional system design preparation relies on memorizing static block diagrams without simulating "
            "actual traffic dynamics, component failures, queue latencies, or quantitative capacity boundaries."
        ),
        "overview": (
            "An interactive distributed system design platform that combines a live architectural whiteboard canvas, "
            "a deterministic static analysis rule engine, a discrete-event traffic simulator (100 QPS to 1,000,000 QPS), "
            "and a Socratic AI Staff Architect mentor."
        ),
        "engineering_highlights": [
            "Discrete-Event Traffic Simulation: Simulates 100 QPS to 1M QPS applying Little's Law, M/M/c queuing models, and server concurrency bounds to identify throughput bottlenecks.",
            "Deterministic Rule Engine: Runs automated graph validation against typed JSON architecture topology to detect Single Points of Failure (SPOF), unbounded message queues, and un-cached hot database paths.",
            "Interactive Architecture Canvas: 30+ distributed components (Envoy, Kafka, Redis, PostgreSQL, Vector DBs, ML inference servers) rendered with React Flow (@xyflow/react).",
            "Chaos & Failure Injection: Tests system resilience by killing database nodes, injecting network latency, and triggering cache invalidation storms in real time.",
            "Socratic AI Staff Architect: Leverages a progressive 4-level hint ladder to challenge architectural decisions without prematurely giving away solutions."
        ],
        "tech_stack": [
            {"name": "FastAPI", "icon": "devicon-fastapi-plain"},
            {"name": "Python 3.12", "icon": "devicon-python-plain"},
            {"name": "Next.js 14", "icon": "devicon-nextjs-plain"},
            {"name": "React Flow", "icon": "devicon-react-original"},
            {"name": "PostgreSQL", "icon": "devicon-postgresql-plain"},
            {"name": "Tailwind CSS", "icon": "devicon-tailwindcss-plain"},
        ],
    },
    {
        "id": "smart-traffic",
        "title": "Smart Traffic Management System",
        "subtitle": "Production-Grade Computer Vision & MLOps Pipeline",
        "tagline": "End-to-End Object Detection, Multi-Object Tracking & Apache Airflow Orchestration",
        "category": "ai-mlops",
        "featured": True,
        "badge": "Flagship MLOps Project",
        "image": "images/poster1.png",
        "github_url": "https://github.com/mithilesh1627/smart-traffic-management-system",
        "demo_url": "https://drive.google.com/file/d/1xmBCdNr5SF1Etrsip_3LKA1uowlMNEeN/view",
        "demo_label": "Watch Architecture Demo",
        "problem_statement": (
            "Deploying computer vision to real-world edge systems requires not just model training, but reliable "
            "MLOps lifecycle automation: dataset versioning, pipeline orchestration, experiment reproducibility, and multi-object tracking."
        ),
        "overview": (
            "A production-oriented intelligent traffic analytics pipeline that performs vehicle detection, "
            "persistent ID tracking, counting, and traffic density estimation. Orchestrated via Apache Airflow "
            "with end-to-end dataset versioning (DVC) and experiment tracking (MLflow)."
        ),
        "engineering_highlights": [
            "End-to-End Pipeline: Dataset (22GB Indian Driving Dataset) → Preprocessing & Augmentation → YOLO Training → Experiment Tracking (MLflow) → Versioning (DVC) → Multi-Object Inference → Streamlit Monitoring.",
            "Multi-Object Tracking (MOT): Integrated ByteTrack & BoT-SORT for persistent ID assignment across occlusion and rapid frame changes.",
            "Traffic Intelligence: Computes real-time vehicle flow rates, directional counts, density classification, and lane congestion indices.",
            "Reproducible MLOps: Automated DAG execution via Apache Airflow; DVC dataset hashing ensures exact reproducibility; MLflow logs metrics and checkpoints.",
            "Training Deduplication: Skips redundant training jobs when dataset hash and hyperparameter configurations match prior runs, conserving GPU budget."
        ],
        "tech_stack": [
            {"name": "YOLO (Ultralytics)", "icon": "devicon-python-plain"},
            {"name": "OpenCV", "icon": "devicon-opencv-plain"},
            {"name": "Apache Airflow", "icon": "devicon-apacheairflow-plain"},
            {"name": "MLflow", "icon": "fas fa-flask"},
            {"name": "DVC", "icon": "devicon-git-plain"},
            {"name": "PyTorch", "icon": "devicon-pytorch-original"},
            {"name": "MongoDB", "icon": "devicon-mongodb-plain"},
            {"name": "Streamlit", "icon": "devicon-streamlit-plain"},
        ],
    },
    {
        "id": "agentic-ops",
        "title": "AgenticOps (AgentIQ)",
        "subtitle": "Autonomous AI Incident Investigation & Decision Platform",
        "tagline": "Multi-Agent DAG State Machine, Hybrid RAG 2.0 & Knowledge Graph Root-Cause Analysis",
        "category": "generative-ai",
        "featured": True,
        "badge": "Flagship GenAI Project",
        "image": "images/MockAnalysis_image.png",
        "github_url": "https://github.com/mithilesh1627/AgenticIQ",
        "demo_url": "",
        "demo_label": "",
        "problem_statement": (
            "Complex site reliability incidents produce overwhelming volumes of telemetry, logs, and runbooks, "
            "slowing down human on-call engineers during critical production outages."
        ),
        "overview": (
            "An autonomous multi-agent platform designed for technical incident triage and root-cause analysis (RCA). "
            "Decomposes ambiguous incidents into a directed acyclic task graph, executes parallel hybrid retrievals, "
            "verifies configuration diffs, and synthesizes evidence-backed postmortems."
        ),
        "engineering_highlights": [
            "Multi-Agent DAG State Machine: 8 specialized agents (Planner, RAG, Telemetry, Hypothesis, Critic, Report) with topological batching via asyncio.gather.",
            "Hybrid RAG 2.0: Fuses dense vector cosine search (Qdrant) and sparse BM25Okapi with Reciprocal Rank Fusion (RRF, k=60) and Cross-Encoder reranking.",
            "Safe Structured Telemetry: Read-only AST query validator (sqlparse) enforcing strict SELECT-only constraints and row limits.",
            "Knowledge Graph Blast Radius: NetworkX MultiDiGraph modeling dependencies across services, databases, teams, and deployment runbooks.",
            "MLflow Prompt Registry: Versioned prompt pipelines with continuous evaluation gates enforcing faithfulness (≥0.90) and citation accuracy (≥0.95)."
        ],
        "tech_stack": [
            {"name": "Python 3.12", "icon": "devicon-python-plain"},
            {"name": "FastAPI", "icon": "devicon-fastapi-plain"},
            {"name": "Qdrant Vector DB", "icon": "fas fa-database"},
            {"name": "MLflow", "icon": "fas fa-flask"},
            {"name": "NetworkX", "icon": "fas fa-diagram-project"},
            {"name": "Docker", "icon": "devicon-docker-plain"},
        ],
    },
    {
        "id": "career-radar",
        "title": "CareerRadar (RoleIQ)",
        "subtitle": "AI-Powered Job Intelligence & Resume Match Engine",
        "tagline": "Automated ATS Web Crawler, Semantic Resume Parsing & Embedding Similarity",
        "category": "generative-ai",
        "featured": False,
        "badge": "AI & Systems",
        "image": "images/MockAnalysis_image.png",
        "github_url": "https://github.com/mithilesh1627",
        "demo_url": "",
        "demo_label": "",
        "problem_statement": (
            "Job seekers and recruiters struggle with fragmented portal postings and opaque ATS keyword filters "
            "that fail to capture semantic skill alignment."
        ),
        "overview": (
            "An automated career intelligence system that crawls corporate portals with Playwright (supporting Greenhouse, Lever, "
            "and generic portals), extracts structured resume profiles via PyMuPDF, and computes hybrid embedding match scores "
            "using Sentence-Transformers."
        ),
        "engineering_highlights": [
            "Automated ATS Crawler: Playwright-driven crawler extracting, deduplicating, and normalizing live job postings with APScheduler.",
            "Structured Resume Extraction: PyMuPDF pipeline parsing candidate work history, education, and domain competencies.",
            "Hybrid Match Engine: Sentence-Transformers semantic cosine similarity fused with exact keyword overlap to generate missing-skill gap reports.",
            "Architecture: FastAPI backend with MongoDB Atlas document storage and clean RESTful API schemas."
        ],
        "tech_stack": [
            {"name": "FastAPI", "icon": "devicon-fastapi-plain"},
            {"name": "Playwright", "icon": "fas fa-robot"},
            {"name": "Sentence-Transformers", "icon": "devicon-python-plain"},
            {"name": "MongoDB Atlas", "icon": "devicon-mongodb-plain"},
            {"name": "PyMuPDF", "icon": "fas fa-file-pdf"},
        ],
    },
    {
        "id": "stock-etl",
        "title": "Stock Market ETL Pipeline",
        "subtitle": "Automated Market Data Ingestion & Analytics Pipeline",
        "tagline": "Apache Airflow DAG Scheduling, MongoDB NoSQL Storage & Streamlit Dashboard",
        "category": "data-engineering",
        "featured": False,
        "badge": "Data Engineering",
        "image": "images/stock_etl_airflow.png",
        "github_url": "https://github.com/mithilesh1627/Stock-Market-ETL-Airflow",
        "demo_url": "",
        "demo_label": "",
        "problem_statement": (
            "Financial market analytics requires robust daily data ingestion pipelines that handle API rate limits, "
            "transient network failures, and data schema normalization."
        ),
        "overview": (
            "An automated daily ETL pipeline fetching financial ticker data from market APIs. "
            "Built with fault-tolerant DAG scheduling in Apache Airflow, data transformation in Pandas, "
            "and structured document storage in MongoDB."
        ),
        "engineering_highlights": [
            "Airflow DAG Orchestration: Automated daily execution scheduling Extract → Transform → Load tasks with retry hooks and XCom state sharing.",
            "Pandas Transformations: Automated data cleaning, rolling moving average (SMA) computations, and anomaly checks.",
            "MongoDB Indexing: Optimized compound indexing on ticker symbol and UTC timestamp for fast downstream queries.",
            "Monitoring: Streamlit interactive analytical dashboard displaying daily volume and price momentum."
        ],
        "tech_stack": [
            {"name": "Apache Airflow", "icon": "devicon-apacheairflow-plain"},
            {"name": "Python", "icon": "devicon-python-plain"},
            {"name": "MongoDB", "icon": "devicon-mongodb-plain"},
            {"name": "Pandas", "icon": "devicon-pandas-plain"},
            {"name": "Streamlit", "icon": "devicon-streamlit-plain"},
        ],
    },
    {
        "id": "heart-disease",
        "title": "Heart Disease Risk Classifier",
        "subtitle": "Clinical Diagnostic Machine Learning Classifier",
        "tagline": "Scikit-Learn Classification Models with Interactive Streamlit Cloud Deployment",
        "category": "machine-learning",
        "featured": False,
        "badge": "Machine Learning",
        "image": "images/heart_disease.png",
        "github_url": "https://github.com/mithilesh1627/ML-Projects/tree/main/Heart%20Disease%20Prediction",
        "demo_url": "https://heartdiseasepredictmodel1627.streamlit.app/",
        "demo_label": "Launch Live App",
        "problem_statement": (
            "Early identification of cardiovascular risk factors from clinical measurements supports timely medical intervention."
        ),
        "overview": (
            "A clinical diagnostic classifier predicting cardiovascular disease risk from patient clinical factors "
            "including blood pressure, serum cholesterol, and exercise-induced angina. Deployed as a live interactive app on Streamlit Cloud."
        ),
        "engineering_highlights": [
            "Exploratory Data Analysis: Correlation analysis across clinical features to remove redundant indicators.",
            "Benchmarked Classifiers: Logistic Regression, Random Forest, and Support Vector Machines (~86% accuracy).",
            "Evaluation Metrics: Analyzed ROC-AUC curves, precision-recall trade-offs, and confusion matrix distributions.",
            "Deployment: Publicly accessible interactive web interface deployed on Streamlit Cloud."
        ],
        "tech_stack": [
            {"name": "Scikit-learn", "icon": "devicon-scikitlearn-plain"},
            {"name": "Python", "icon": "devicon-python-plain"},
            {"name": "Pandas", "icon": "devicon-pandas-plain"},
            {"name": "NumPy", "icon": "devicon-numpy-plain"},
            {"name": "Streamlit", "icon": "devicon-streamlit-plain"},
        ],
    },
    {
        "id": "diabetes-prediction",
        "title": "PIMA Diabetes Risk Classifier",
        "subtitle": "Predictive Health Risk Diagnostic Model",
        "tagline": "Feature Normalization, Classification Benchmarks & Streamlit Cloud App",
        "category": "machine-learning",
        "featured": False,
        "badge": "Machine Learning",
        "image": "images/Diabetes.png",
        "github_url": "https://github.com/mithilesh1627/ML-Projects/tree/main/PIMA%20Diabetes%20Prediction",
        "demo_url": "https://diabetespredictmodel1627.streamlit.app/",
        "demo_label": "Launch Live App",
        "problem_statement": (
            "Predicting diabetes onset from diagnostic measures requires robust feature imputation for physiological missing values."
        ),
        "overview": (
            "A predictive diagnostic system trained on clinical measures from the PIMA Indian Diabetes dataset. "
            "Employs robust feature normalization and multi-model benchmarking."
        ),
        "engineering_highlights": [
            "Data Preprocessing: Addressed physiological zero measurements via median imputation and standard feature scaling.",
            "Benchmarked Models: Evaluated Decision Trees, K-Nearest Neighbors, and Logistic Regression (~82% accuracy).",
            "Interactive Deployment: Live Streamlit Cloud application with dynamic patient risk input sliders."
        ],
        "tech_stack": [
            {"name": "Scikit-learn", "icon": "devicon-scikitlearn-plain"},
            {"name": "Python", "icon": "devicon-python-plain"},
            {"name": "Pandas", "icon": "devicon-pandas-plain"},
            {"name": "Streamlit", "icon": "devicon-streamlit-plain"},
        ],
    },
    {
        "id": "gender-detection",
        "title": "Real-Time Facial Gender Classification",
        "subtitle": "Deep Convolutional Neural Network with Live Inference",
        "tagline": "CNN Feature Extraction & OpenCV Real-Time Webcam Stream Inference",
        "category": "computer-vision",
        "featured": False,
        "badge": "Computer Vision",
        "image": "images/Gender_Detection.png",
        "github_url": "https://github.com/mithilesh1627/ML-Projects",
        "demo_url": "",
        "demo_label": "",
        "problem_statement": (
            "Real-time video inference requires lightweight CNN architectures that balance feature extraction depth with inference latency."
        ),
        "overview": (
            "A deep learning vision pipeline that classifies gender from facial imagery. Integrates CNN-based feature representation "
            "with real-time facial boundary detection via OpenCV."
        ),
        "engineering_highlights": [
            "Dataset & Augmentation: Trained on 3,000+ labeled facial images with data augmentation (rotations, horizontal flips, illumination shifts).",
            "CNN Architecture: Multi-layer convolutional network with batch normalization and dropout layers to prevent overfitting (~87.8% validation accuracy).",
            "Live Stream Inference: OpenCV video stream capture feeding localized face crops into the CNN for live classification."
        ],
        "tech_stack": [
            {"name": "TensorFlow / Keras", "icon": "devicon-tensorflow-original"},
            {"name": "OpenCV", "icon": "devicon-opencv-plain"},
            {"name": "Python", "icon": "devicon-python-plain"},
            {"name": "NumPy", "icon": "devicon-numpy-plain"},
        ],
    },
    {
        "id": "mock-analysis",
        "title": "MockAnalysis: Automation & Performance Extractor",
        "subtitle": "Selenium-driven Academic Analytics System",
        "tagline": "Automated Web Scraping, Tabular Normalization & Reporting",
        "category": "systems",
        "featured": False,
        "badge": "Automation & ETL",
        "image": "images/MockAnalysis_image.png",
        "github_url": "https://github.com/mithilesh1627/ML-Projects/tree/main/MockAnalysisProject",
        "demo_url": "",
        "demo_label": "",
        "problem_statement": (
            "Manual tracking and compilation of student test records from online testing portals was error-prone and time-consuming."
        ),
        "overview": (
            "An automation engine that extracts, standardizes, and visualizes student test performance data from online learning portals. "
            "Replaced repetitive manual compilation with automated scripts, cutting analysis overhead by 40%."
        ),
        "engineering_highlights": [
            "Headless Portal Automation: Selenium WebDriver automation navigating multi-step authentication and paginated result portals.",
            "Data Normalization: Pandas tabular cleaning parsing nested score tables into structured DataFrames.",
            "Automated Reporting: Matplotlib visualization generating class-wide score distributions and ranking summaries."
        ],
        "tech_stack": [
            {"name": "Selenium", "icon": "devicon-selenium-original"},
            {"name": "Python", "icon": "devicon-python-plain"},
            {"name": "Pandas", "icon": "devicon-pandas-plain"},
            {"name": "Matplotlib", "icon": "devicon-matplotlib-plain"},
        ],
    },
    {
        "id": "bihari-blogger",
        "title": "BihariBlogger Platform",
        "subtitle": "Full-Stack Dynamic Blogging Platform",
        "tagline": "Flask Modular Architecture with MongoDB NoSQL Document Storage",
        "category": "systems",
        "featured": False,
        "badge": "Full-Stack Backend",
        "image": "images/BihariBlogger.jpg",
        "github_url": "https://github.com/mithilesh1627/BihariBlogger",
        "demo_url": "",
        "demo_label": "",
        "problem_statement": (
            "Developing scalable content platforms requires modular backend architecture with secure session auth and flexible document schemas."
        ),
        "overview": (
            "A modular community blogging application built with Flask and MongoDB. Demonstrates clean MVC/Blueprint architecture, "
            "session authentication with Flask-Login, and robust CRUD capabilities."
        ),
        "engineering_highlights": [
            "Modular Backend: Clean separation of blueprints, WTForms input validation, and PyMongo data access.",
            "Authentication & Security: Session management and password hashing via Flask-Login and Werkzeug security.",
            "CRUD Operations: End-to-end authoring, editing, category tagging, and post retrieval."
        ],
        "tech_stack": [
            {"name": "Flask", "icon": "devicon-flask-original"},
            {"name": "MongoDB", "icon": "devicon-mongodb-plain"},
            {"name": "Python", "icon": "devicon-python-plain"},
            {"name": "Bootstrap 5", "icon": "devicon-bootstrap-plain"},
        ],
    },
]

CERTIFICATIONS = [
    {
        "title": "Accenture North America - Data Analytics and Visualization Job Simulation",
        "issuer": "Accenture (Forage)",
        "credential_id": "2tG6WLM2W5Yv9jJ",
        "link": "https://drive.google.com/file/d/1WGgg5hHKA10Agr1UDe1cc9v8yei--NIp/view?usp=sharing"
    },
    {
        "title": "Python Training by Spoken Tutorial",
        "issuer": "IIT Bombay (Govt. of India Spoken Tutorial Project)",
        "credential_id": "",
        "link": "https://drive.google.com/file/d/1zkq1Tq54rDRfPo_top5RA2-tuxgrA7j8/view?usp=drive_link"
    },
    {
        "title": "Machine Learning Foundations",
        "issuer": "Great Learning",
        "credential_id": "",
        "link": "https://drive.google.com/file/d/1MUI6bV8lwD41G0fq0rwjEbcm70c5aN6b/view"
    },
    {
        "title": "Computer Vision Essentials",
        "issuer": "Great Learning",
        "credential_id": "",
        "link": "https://drive.google.com/file/d/1xYdhVR-tp0AesaXBLhIqRzMoN1dUVtfX/view"
    },
    {
        "title": "Python for Machine Learning",
        "issuer": "Great Learning",
        "credential_id": "",
        "link": "https://drive.google.com/file/d/10pIBT-J5Nb1cQ_0zvaddFfK-UTcfLc1X/view"
    },
    {
        "title": "Unsupervised ML with K-Means",
        "issuer": "Great Learning",
        "credential_id": "",
        "link": "https://drive.google.com/file/d/1Wusu6V_c7t0Y3736-PTNuFOEhGntbH6p/view?usp=drive_link"
    },
    {
        "title": "Neural Networks & Deep Learning",
        "issuer": "Great Learning",
        "credential_id": "",
        "link": "https://drive.google.com/file/d/1CWCENkhAoaa3o8BVrwVXasfcGtuXa-cD/view?usp=drive_link"
    },
    {
        "title": "Infosys Certified Selenium with Python Automation Tester",
        "issuer": "Infosys Ltd.",
        "credential_id": "",
        "link": ""
    },
    {
        "title": "Infosys Certified Software Development Engineer in Test (SDET)",
        "issuer": "Infosys Ltd.",
        "credential_id": "",
        "link": ""
    },
    {
        "title": "Infosys Certified Digital Assurance Professional",
        "issuer": "Infosys Ltd.",
        "credential_id": "",
        "link": ""
    },
    {
        "title": "Infosys Certified Python Programmer",
        "issuer": "Infosys Ltd.",
        "credential_id": "",
        "link": ""
    },
    {
        "title": "Infosys Certified Data Management Associate",
        "issuer": "Infosys Ltd.",
        "credential_id": "",
        "link": ""
    },
]
