"""
Seed script to populate MongoDB with all portfolio projects.
Idempotent: updates existing projects based on unique 'slug', inserts missing ones.
Never prints or logs database credentials.
"""

import os
import sys
import logging
from typing import List, Dict, Any

# Ensure project root is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from dotenv import load_dotenv
load_dotenv(os.path.join(project_root, ".env"))

from config import Config
from repositories.project_repository import ProjectRepository
from models.project import Project, slugify
import pymongo

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("seed_projects")


# Complete verified projects dataset combining data/projects.py and template modals
SEED_PROJECTS: List[Dict[str, Any]] = [
    {
        "title": "DesignKaro",
        "slug": "designkaro",
        "subtitle": "Interactive Distributed System Design & Architecture Simulator",
        "short_description": "Discrete-event traffic simulation (1M QPS), static architecture rule engine, and Socratic AI mentor.",
        "description": (
            "An interactive distributed system design platform that combines a live architectural whiteboard canvas, "
            "a deterministic static analysis rule engine, a discrete-event traffic simulator (100 QPS to 1,000,000 QPS), "
            "and a Socratic AI Staff Architect mentor."
        ),
        "status": "completed",
        "featured": True,
        "featured_order": 1,
        "category": "systems",
        "badge": "Flagship Systems Project",
        "image": "images/BihariBLogger2.png",
        "github_url": "https://github.com/mithilesh1627/DesignKaro",
        "live_url": "",
        "demo_label": "Explore Architecture",
        "technologies": ["FastAPI", "Python", "React Flow", "PostgreSQL", "Next.js", "Tailwind CSS"],
        "features": [
            "Discrete-Event Traffic Simulation: Simulates 100 QPS to 1M QPS applying Little's Law, M/M/c queuing models, and server concurrency bounds to identify throughput bottlenecks.",
            "Deterministic Rule Engine: Runs automated graph validation against typed JSON architecture topology to detect Single Points of Failure (SPOF), unbounded message queues, and un-cached hot database paths.",
            "Interactive Architecture Canvas: 30+ distributed components (Envoy, Kafka, Redis, PostgreSQL, Vector DBs, ML inference servers) rendered with React Flow.",
            "Chaos & Failure Injection: Tests system resilience by killing database nodes, injecting network latency, and triggering cache invalidation storms in real time.",
            "Socratic AI Staff Architect: Leverages a progressive 4-level hint ladder to challenge architectural decisions without prematurely giving away solutions."
        ],
        "challenges": [
            "Modeling realistic distributed latency distributions (p50, p95, p99) under simulated concurrent load.",
            "Validating arbitrary cycle graphs and dependency DAGs in the browser without freezing the UI thread."
        ],
        "future_improvements": [
            "Distributed tracing integration with OpenTelemetry spans visualization.",
            "Automated cost estimator modeling monthly AWS/GCP infrastructure expenditure."
        ],
        "published": True
    },
    {
        "title": "Smart Traffic Management System",
        "slug": "smart-traffic",
        "subtitle": "Production-Grade Computer Vision & MLOps Pipeline",
        "short_description": "End-to-End Object Detection, Multi-Object Tracking & Apache Airflow Orchestration.",
        "description": (
            "A production-oriented intelligent traffic analytics pipeline that performs vehicle detection, "
            "persistent ID tracking, counting, and traffic density estimation. Orchestrated via Apache Airflow "
            "with end-to-end dataset versioning (DVC) and experiment tracking (MLflow)."
        ),
        "status": "completed",
        "featured": True,
        "featured_order": 2,
        "category": "ai-mlops",
        "badge": "Flagship MLOps Project",
        "image": "images/poster1.png",
        "github_url": "https://github.com/mithilesh1627/smart-traffic-management-system",
        "live_url": "https://drive.google.com/file/d/1xmBCdNr5SF1Etrsip_3LKA1uowlMNEeN/view",
        "demo_label": "Watch Demo Video",
        "technologies": ["YOLO", "OpenCV", "Apache Airflow", "MLflow", "DVC", "PyTorch", "MongoDB", "Streamlit"],
        "features": [
            "End-to-End Pipeline: Dataset (22GB Indian Driving Dataset) → Preprocessing & Augmentation → YOLO Training → Experiment Tracking (MLflow) → Versioning (DVC) → Multi-Object Inference → Streamlit Monitoring.",
            "Multi-Object Tracking (MOT): Integrated ByteTrack & BoT-SORT for persistent ID assignment across occlusion and rapid frame changes.",
            "Traffic Intelligence: Computes real-time vehicle flow rates, directional counts, density classification, and lane congestion indices.",
            "Reproducible MLOps: Automated DAG execution via Apache Airflow; DVC dataset hashing ensures exact reproducibility; MLflow logs metrics and checkpoints.",
            "Training Deduplication: Skips redundant training jobs when dataset hash and hyperparameter configurations match prior runs, conserving GPU budget."
        ],
        "challenges": [
            "Handling severe occlusions and small vehicle bounding boxes in dense multi-lane traffic feeds.",
            "Maintaining persistent tracking IDs when vehicles temporarily leave and re-enter the camera frame."
        ],
        "future_improvements": [
            "Multi-camera spatial-temporal cross-junction tracking.",
            "Automated number plate recognition (ANPR) and traffic violation detection.",
            "Real-time streaming ingestion pipeline using Apache Kafka."
        ],
        "published": True
    },
    {
        "title": "AgenticOps (AgentIQ)",
        "slug": "agentic-ops",
        "subtitle": "Autonomous AI Incident Investigation & Decision Platform",
        "short_description": "Multi-Agent DAG State Machine, Hybrid RAG 2.0 & Knowledge Graph Root-Cause Analysis.",
        "description": (
            "An autonomous multi-agent incident investigation system that ingests alert streams, explores observability "
            "telemetry, queries hybrid documentation stores (vector + BM25 + knowledge graph), and synthesizes actionable "
            "root-cause hypotheses and remediation runbooks."
        ),
        "status": "completed",
        "featured": True,
        "featured_order": 3,
        "category": "generative-ai",
        "badge": "Flagship GenAI Project",
        "image": "images/MockAnalysis_image.png",
        "github_url": "https://github.com/mithilesh1627/AgenticIQ",
        "live_url": "",
        "demo_label": "View Architecture",
        "technologies": ["Python", "FastAPI", "LangChain", "Qdrant", "Docker"],
        "features": [
            "Multi-Agent DAG: 8 specialized agents (Triage, Telemetry, LogParser, ArchitectureMapper, RunbookSearch, Correlator, Verifier, Reporter) orchestrated via state machine.",
            "Hybrid RAG 2.0: Combines dense vector similarity with sparse BM25 and Neo4j graph traversal for high precision retrieval.",
            "Self-Correction & Hallucination Guardrails: Verifier agent inspects hypotheses against live system logs before emitting recommendations."
        ],
        "challenges": [
            "Preventing agent loops and hallucinations during anomalous telemetry events.",
            "Balancing prompt context window limitations when summarizing large log dumps."
        ],
        "future_improvements": [
            "Direct bidirectional integration with PagerDuty and Slack workflows.",
            "Interactive runbook execution sandbox with human-in-the-loop approvals."
        ],
        "published": True
    },
    {
        "title": "CareerRadar (RoleIQ)",
        "slug": "career-radar",
        "subtitle": "Autonomous Career Portal Crawler & Skill Intelligence Engine",
        "short_description": "Playwright Career Portal Crawler, NLP Skill Gap Extraction & Automated Tracking.",
        "description": (
            "An automated career portal intelligence engine that navigates enterprise job portals, extracts dynamic postings, "
            "performs semantic skill matching against candidate profiles, and highlights missing competencies."
        ),
        "status": "completed",
        "featured": False,
        "featured_order": 4,
        "category": "data-engineering",
        "badge": "Data & Automation",
        "image": "images/poster1.png",
        "github_url": "https://github.com/mithilesh1627/Career-Radar",
        "live_url": "",
        "demo_label": "View Project",
        "technologies": ["Playwright", "FastAPI", "MongoDB", "Python", "Streamlit"],
        "features": [
            "Headless Portal Crawler: Navigates modern single-page enterprise job portals with Playwright.",
            "Semantic Skill Extraction: Parses job descriptions into structured skill vectors.",
            "Skill Gap Analysis: Computes cosine similarity between resume competencies and required qualifications.",
            "MongoDB Atlas Datastore: Maintains normalized job listings, deduplication hashes, and tracking histories."
        ],
        "challenges": [
            "Handling dynamic client-side pagination and infinite scrolls across varying corporate career sites."
        ],
        "future_improvements": [
            "Automated weekly email summaries of matching roles.",
            "AI-assisted cover letter personalization tailored to extracted job requirements."
        ],
        "published": True
    },
    {
        "title": "Stock Market ETL Pipeline",
        "slug": "stock-market-etl",
        "subtitle": "Daily Financial Market Data Pipeline (Airflow + MongoDB)",
        "short_description": "Fault-tolerant daily financial market data ingestion, Pandas transformations, and MongoDB storage.",
        "description": (
            "A production-ready ETL pipeline automating daily financial market data extraction from external APIs. "
            "Built with Apache Airflow DAGs, Pandas data transformations, and structured MongoDB document storage."
        ),
        "status": "completed",
        "featured": False,
        "featured_order": 5,
        "category": "data-engineering",
        "badge": "Data Engineering",
        "image": "images/stock_etl_airflow.png",
        "github_url": "https://github.com/mithilesh1627/Stock-Market-ETL-Airflow",
        "live_url": "",
        "demo_label": "View Pipeline",
        "technologies": ["Apache Airflow", "Python", "MongoDB", "Pandas", "Streamlit"],
        "features": [
            "Airflow DAG Orchestration: Scheduled daily execution for Extract → Transform → Load tasks with automatic retries.",
            "Pandas Transformations: Automated data cleaning, rolling moving average (SMA) computations, and anomaly filtering.",
            "MongoDB Indexing: Optimized compound indexing on ticker symbol and UTC timestamp for fast downstream queries.",
            "Streamlit Dashboard: Analytical interface displaying price momentum and volume trends."
        ],
        "challenges": [
            "Managing external financial API rate limits and handling transient connection dropouts."
        ],
        "future_improvements": [
            "Dockerized deployment for one-command containerized local execution.",
            "Slack webhook notifications for DAG run failures."
        ],
        "published": True
    },
    {
        "title": "Heart Disease Risk Classifier",
        "slug": "heart-disease",
        "subtitle": "Clinical Diagnostic Machine Learning Classifier",
        "short_description": "Scikit-Learn classification models with interactive Streamlit Cloud deployment.",
        "description": (
            "A clinical diagnostic classifier predicting cardiovascular disease risk from patient clinical factors "
            "including blood pressure, serum cholesterol, and exercise-induced angina. Deployed as a live interactive app on Streamlit Cloud."
        ),
        "status": "completed",
        "featured": False,
        "featured_order": 6,
        "category": "machine-learning",
        "badge": "Machine Learning",
        "image": "images/heart_disease.png",
        "github_url": "https://github.com/mithilesh1627/ML-Projects/tree/main/Heart%20Disease%20Prediction",
        "live_url": "https://heartdiseasepredictmodel1627.streamlit.app/",
        "demo_label": "Launch Live App",
        "technologies": ["Scikit-learn", "Python", "Pandas", "NumPy", "Streamlit"],
        "features": [
            "Exploratory Data Analysis: Correlation analysis across clinical features to remove redundant indicators.",
            "Benchmarked Classifiers: Logistic Regression, Random Forest, and Support Vector Machines (~86% accuracy).",
            "Evaluation Metrics: Analyzed ROC-AUC curves, precision-recall trade-offs, and confusion matrix distributions.",
            "Deployment: Publicly accessible interactive web interface deployed on Streamlit Cloud."
        ],
        "challenges": [
            "Mitigating feature multicollinearity and handling skewed clinical distributions."
        ],
        "future_improvements": [
            "SHAP / LIME explainability integration for clinician-friendly model interpretability."
        ],
        "published": True
    },
    {
        "title": "PIMA Diabetes Risk Classifier",
        "slug": "diabetes-prediction",
        "subtitle": "Predictive Health Risk Diagnostic Model",
        "short_description": "Feature normalization, classification benchmarks, and interactive Streamlit Cloud app.",
        "description": (
            "A predictive diagnostic system trained on clinical measures from the PIMA Indian Diabetes dataset. "
            "Employs robust feature normalization and multi-model benchmarking."
        ),
        "status": "completed",
        "featured": False,
        "featured_order": 7,
        "category": "machine-learning",
        "badge": "Machine Learning",
        "image": "images/Diabetes.png",
        "github_url": "https://github.com/mithilesh1627/ML-Projects/tree/main/PIMA%20Diabetes%20Prediction",
        "live_url": "https://diabetespredictmodel1627.streamlit.app/",
        "demo_label": "Launch Live App",
        "technologies": ["Scikit-learn", "Python", "Pandas", "NumPy", "Streamlit"],
        "features": [
            "Data Preprocessing: Addressed physiological zero measurements via median imputation and standard feature scaling.",
            "Benchmarked Models: Evaluated Decision Trees, K-Nearest Neighbors, and Logistic Regression (~82% accuracy).",
            "Interactive Deployment: Live Streamlit Cloud application with dynamic patient risk input sliders."
        ],
        "challenges": [
            "Treating missing physiological data without distorting biological distributions."
        ],
        "future_improvements": [
            "Ensemble stacking with XGBoost to boost classification recall on borderline cases."
        ],
        "published": True
    },
    {
        "title": "Gender Classification using CNN",
        "slug": "gender-cnn",
        "subtitle": "Deep Learning Computer Vision Model with OpenCV",
        "short_description": "Convolutional Neural Network achieving 87.8% accuracy with real-time OpenCV webcam inference.",
        "description": (
            "A deep learning computer vision model classifying gender from facial images using a custom Convolutional "
            "Neural Network (CNN). Integrated with OpenCV for real-time live webcam face detection and inference."
        ),
        "status": "completed",
        "featured": False,
        "featured_order": 8,
        "category": "computer-vision",
        "badge": "Computer Vision",
        "image": "images/Gender_Detection.png",
        "github_url": "https://github.com/mithilesh1627/ML-Projects/tree/main/MockAnalysisProject",
        "live_url": "",
        "demo_label": "View Project",
        "technologies": ["TensorFlow", "Keras", "OpenCV", "Python", "NumPy"],
        "features": [
            "CNN Architecture: Multi-layer convolutional model trained on 3,000+ labeled facial images reaching 87.8% accuracy.",
            "Data Augmentation: Rotations, flips, zoom, and contrast adjustments to improve generalization.",
            "Real-time OpenCV Inference: Haar-cascade / DNN face localization coupled with immediate frame-by-frame gender prediction."
        ],
        "challenges": [
            "Overcoming overfitting on facial variations like glasses, head angles, and lighting conditions."
        ],
        "future_improvements": [
            "Migrate from custom CNN to a fine-tuned MobileNetV3 backbone for higher FPS on edge devices."
        ],
        "published": True
    },
    {
        "title": "MockAnalysis",
        "slug": "mock-analysis",
        "subtitle": "Automated Student Assessment & Analytics Platform",
        "short_description": "Selenium web automation and Pandas data cleaning pipeline for institutional academic analytics.",
        "description": (
            "An automation and data analysis tool designed to extract, clean, and analyze student mock test performance "
            "from online educational testing portals using Selenium and Pandas."
        ),
        "status": "completed",
        "featured": False,
        "featured_order": 9,
        "category": "data-engineering",
        "badge": "Automation",
        "image": "images/MockAnalysis_image.png",
        "github_url": "https://github.com/mithilesh1627/ML-Projects/tree/main/MockAnalysisProject",
        "live_url": "",
        "demo_label": "View Project",
        "technologies": ["Selenium", "Python", "Pandas", "NumPy", "OpenCV"],
        "features": [
            "Web Automation: Programmatic portal login, session handling, and bulk test result scraping with Selenium.",
            "Tabular Processing: Aggregates student score distributions, subject-wise percentiles, and completion times with Pandas.",
            "Insight Generation: Computes class-wide performance metrics to identify learning gaps."
        ],
        "challenges": [
            "Adapting to asynchronous AJAX pagination and dynamic DOM changes on the testing portal."
        ],
        "future_improvements": [
            "Exportable PDF report generation for batch student performance cards."
        ],
        "published": True
    },
    {
        "title": "BihariBlogger",
        "slug": "bihari-blogger",
        "subtitle": "Social Blogging Web Platform (Flask + MongoDB)",
        "short_description": "Modular social blogging web application with Flask-Login session auth and MongoDB storage.",
        "description": (
            "A dynamic social blogging web platform allowing users to publish, edit, and explore content. "
            "Built with Flask, Flask-Login authentication, modular blueprints, and MongoDB document storage."
        ),
        "status": "completed",
        "featured": False,
        "featured_order": 10,
        "category": "systems",
        "badge": "Web Application",
        "image": "images/BihariBlogger.jpg",
        "github_url": "https://github.com/mithilesh1627/BihariBlogger",
        "live_url": "",
        "demo_label": "View Platform",
        "technologies": ["Flask", "MongoDB", "Python", "Bootstrap 5", "HTML5", "CSS3"],
        "features": [
            "User Authentication: Secure registration and session-based login workflows powered by Flask-Login.",
            "CRUD Operations: Write, update, and delete blog posts with Markdown formatting support.",
            "Author Dashboard: Personalized management view of all authored articles and interaction statistics.",
            "NoSQL Backend: PyMongo integration with flexible document schemas for posts and user profiles."
        ],
        "challenges": [
            "Designing scalable MongoDB schemas for nested comments and author relationships."
        ],
        "future_improvements": [
            "Rich Markdown WYSIWYG editor.",
            "Social interactions including likes, bookmarks, and tag-based filtering."
        ],
        "published": True
    }
]

SEED_CERTIFICATES: List[Dict[str, Any]] = [
    {
        "order": 1,
        "title": "Accenture North America - Data Analytics and Visualization Job Simulation",
        "issuer": "Accenture (Forage)",
        "credential_id": "2tG6WLM2W5Yv9jJ",
        "link": "https://drive.google.com/file/d/1WGgg5hHKA10Agr1UDe1cc9v8yei--NIp/view?usp=sharing"
    },
    {
        "order": 2,
        "title": "Python Training by Spoken Tutorial",
        "issuer": "IIT Bombay (Govt. of India Spoken Tutorial Project)",
        "credential_id": "",
        "link": "https://drive.google.com/file/d/1zkq1Tq54rDRfPo_top5RA2-tuxgrA7j8/view?usp=drive_link"
    },
    {
        "order": 3,
        "title": "Machine Learning Foundations",
        "issuer": "Great Learning",
        "credential_id": "",
        "link": "https://drive.google.com/file/d/1MUI6bV8lwD41G0fq0rwjEbcm70c5aN6b/view"
    },
    {
        "order": 4,
        "title": "Computer Vision Essentials",
        "issuer": "Great Learning",
        "credential_id": "",
        "link": "https://drive.google.com/file/d/1xYdhVR-tp0AesaXBLhIqRzMoN1dUVtfX/view"
    },
    {
        "order": 5,
        "title": "Python for Machine Learning",
        "issuer": "Great Learning",
        "credential_id": "",
        "link": "https://drive.google.com/file/d/10pIBT-J5Nb1cQ_0zvaddFfK-UTcfLc1X/view"
    },
    {
        "order": 6,
        "title": "Unsupervised ML with K-Means",
        "issuer": "Great Learning",
        "credential_id": "",
        "link": "https://drive.google.com/file/d/1Wusu6V_c7t0Y3736-PTNuFOEhGntbH6p/view?usp=drive_link"
    },
    {
        "order": 7,
        "title": "Neural Networks & Deep Learning",
        "issuer": "Great Learning",
        "credential_id": "",
        "link": "https://drive.google.com/file/d/1CWCENkhAoaa3o8BVrwVXasfcGtuXa-cD/view?usp=drive_link"
    },
    {
        "order": 8,
        "title": "Infosys Certified Selenium with Python Automation Tester",
        "issuer": "Infosys Ltd.",
        "credential_id": "",
        "link": ""
    },
    {
        "order": 9,
        "title": "Infosys Certified Software Development Engineer in Test (SDET)",
        "issuer": "Infosys Ltd.",
        "credential_id": "",
        "link": ""
    },
    {
        "order": 10,
        "title": "Infosys Certified Digital Assurance Professional",
        "issuer": "Infosys Ltd.",
        "credential_id": "",
        "link": ""
    },
    {
        "order": 11,
        "title": "Infosys Certified Python Programmer",
        "issuer": "Infosys Ltd.",
        "credential_id": "",
        "link": ""
    },
    {
        "order": 12,
        "title": "Infosys Certified Data Management Associate",
        "issuer": "Infosys Ltd.",
        "credential_id": "",
        "link": ""
    }
]


def seed_database() -> bool:
    """Connect to MongoDB and upsert all projects and certificates."""
    mongo_uri = Config.MONGODB_URI
    db_name = Config.MONGODB_DATABASE

    if not mongo_uri:
        logger.warning("MONGODB_URI not configured in environment or .env. Cannot seed live MongoDB cluster.")
        return False

    try:
        repo = ProjectRepository(mongo_uri=mongo_uri, db_name=db_name)
        if not repo.is_connected():
            logger.error("Could not establish connection to MongoDB. Verify network and MONGODB_URI.")
            return False

        repo.ensure_indexes()
        col = repo.get_collection()

        logger.info("Starting seed process for %d projects into database: %s", len(SEED_PROJECTS), db_name)
        inserted_count = 0
        updated_count = 0

        for p_data in SEED_PROJECTS:
            project = Project.from_doc(p_data)
            doc = project.to_doc()

            # Upsert by slug
            res = col.update_one(
                {"slug": project.slug},
                {"$set": doc},
                upsert=True
            )

            if res.upserted_id:
                inserted_count += 1
                logger.info("  [+] Inserted new project: %s (slug: %s)", project.title, project.slug)
            elif res.matched_count > 0:
                updated_count += 1
                logger.info("  [*] Updated existing project: %s (slug: %s)", project.title, project.slug)

        total_projects = repo.count()
        logger.info("Projects seed completed! Inserted: %d, Updated: %d, Total in DB: %d",
                    inserted_count, updated_count, total_projects)

        # Seed certificates
        client = repo._get_client()
        cert_col = client[db_name]["certificates"]
        cert_col.create_index([("order", pymongo.ASCENDING)])
        cert_col.create_index([("title", pymongo.ASCENDING)], unique=True)

        logger.info("Starting seed process for %d certificates into database: %s", len(SEED_CERTIFICATES), db_name)
        cert_inserted = 0
        cert_updated = 0

        for c_data in SEED_CERTIFICATES:
            res = cert_col.update_one(
                {"title": c_data["title"]},
                {"$set": c_data},
                upsert=True
            )
            if res.upserted_id:
                cert_inserted += 1
                logger.info("  [+] Inserted certificate: %s", c_data["title"])
            elif res.matched_count > 0:
                cert_updated += 1
                logger.info("  [*] Updated certificate: %s", c_data["title"])

        total_certs = cert_col.count_documents({})
        logger.info("Certificates seed completed! Inserted: %d, Updated: %d, Total in DB: %d",
                    cert_inserted, cert_updated, total_certs)

        return True

    except Exception as e:
        logger.error("Unexpected error during seeding: %s", type(e).__name__)
        return False


if __name__ == "__main__":
    success = seed_database()
    sys.exit(0 if success else 1)
