# Mithilesh Chaurasiya — Production Portfolio & Dynamic Project CMS

[![Python 3.12+](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-3776AB?logo=python&logoColor=white)](https://python.org)
[![Flask 3.1.0](https://img.shields.io/badge/Flask-3.1.0-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MongoDB Atlas](https://img.shields.io/badge/MongoDB-Atlas%20%7C%20PyMongo-47A248?logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Deployed on Render](https://img.shields.io/badge/Deployed-Render-46E3B7?logo=render&logoColor=white)](https://render.com)
[![Tests Passing](https://img.shields.io/badge/Tests-30%20%2F%2030%20Passing-brightgreen?logo=pytest&logoColor=white)](https://pytest.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

🟢 **Live Website**: [https://mithileshchaurasiya.me/](https://mithileshchaurasiya.me/)<br>
🔐 **Admin CMS**: [https://mithileshchaurasiya.me/admin/login](https://mithileshchaurasiya.me/admin/login)<br>
📄 **Resume (PDF)**: [Download CV](https://mithileshchaurasiya.me/static/CV_Mithilesh.pdf)<br>
📂 **GitHub Profile**: [github.com/mithilesh1627](https://github.com/mithilesh1627)<br>
💼 **LinkedIn Profile**: [linkedin.com/in/mithileshchaurasiya](https://www.linkedin.com/in/mithileshchaurasiya/)<br>
💻 **LeetCode Profile**: [leetcode.com/u/Mithilesh_1627](https://leetcode.com/u/Mithilesh_1627/)

---

## 📌 Executive Summary

This repository houses the production codebase for the personal portfolio and **MongoDB-backed Project Content Management System (CMS)** of **Mithilesh Chaurasiya**, built to showcase production engineering competencies for **AI Engineer**, **Machine Learning Engineer**, and **MLOps Engineer** roles.

### Key Highlights
- **2.8 Years at Infosys**: Data Engineering, ETL validation, SQL pipeline testing, and introducing reproducible MLOps tooling (MLflow, DVC) into production workflows.
- **MCA @ National Institute of Technology, Agartala (Class of 2027)**: Student ML Lead at the Developers & Coders Club (DCC).
- **Core Engineering Focus**: Real-time Computer Vision (YOLO, OpenCV), MLOps pipelines (Apache Airflow, MLflow, DVC, Docker), and Agentic/LLM systems.

---

## 🛠️ Tech Stack & Systems Architecture

| Layer | Technologies & Tools |
| :--- | :--- |
| **Backend Framework** | Python 3.12+, Flask 3.1.0 (Application Factory pattern, modular Blueprints) |
| **Database & CMS** | MongoDB Atlas / PyMongo (NoSQL document store, compound indexes, unique slug indexing) |
| **WSGI Server** | Gunicorn 23.0.0 (multi-worker production server bound to `$PORT`) |
| **Frontend & UI** | Semantic HTML5, CSS3 Custom Properties (Dark Slate Design System), Vanilla JS (Accessible modals & tabs) |
| **Security & Auth** | Session CSRF tokens, Bot Honeypot fields, Google reCAPTCHA v2, Werkzeug password hashing |
| **SEO & Semantic Web** | Schema.org `Person` JSON-LD, OpenGraph / Twitter Cards, dynamic canonical URLs, `robots.txt`, `sitemap.xml` |
| **Hosting & CI/CD** | Render Web Service with automated continuous deployment from `main`, Cloudflare TLS/HTTPS |

---

## 🏗️ Clean System Architecture

The codebase follows strict separation of concerns, separating data persistence, domain modeling, business logic, and presentation layers:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        PUBLIC CLIENTS & ADMIN                          │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                         HTTP Requests (GET/POST)
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        FLASK BLUEPRINT ROUTES                          │
│   • routes/main.py            (Home, Projects, Academic, SEO)         │
│   • routes/contact.py         (Contact form, CSRF, Honeypot)          │
│   • routes/admin_projects.py  (Protected Admin CMS & Authentication)  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                            SERVICES LAYER                              │
│   • services/project_service.py   (Validation, slugs, normalization)   │
│   • services/recaptcha_service.py (Google reCAPTCHA verification)     │
│   • services/email_service.py     (Header-sanitized SMTP delivery)    │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                          REPOSITORIES LAYER                            │
│   • repositories/project_repository.py (MongoDB CRUD + Fallback)       │
└───────────────────┬────────────────────────────────┬───────────────────┘
                    │                                │
      [MongoDB Connected]                  [Connection Error / Offline]
                    ▼                                ▼
       ┌────────────────────────┐      ┌────────────────────────┐
       │     MongoDB Atlas      │      │ Static Seed Fallback   │
       │  Collections: projects │      │   data/projects.py     │
       │  and certificates      │      │ (Zero-Downtime Safety) │
       └────────────────────────┘      └────────────────────────┘
```

---

## 📦 Dynamic Project CMS Features

Instead of hardcoding project descriptions and modal dialogs inside static HTML templates, the portfolio is backed by a dynamic CMS:

1. **Full CRUD Control via Web Dashboard**:
   - Access the protected dashboard at `/admin/projects`.
   - Add new projects with rich metadata: category, technologies, engineering highlights, GitHub links, and live demo URLs.
   - Edit, delete, or quickly toggle **Publish / Draft** status.
2. **Accessible Dynamic Modals**:
   - Jinja2 components (`templates/components/project_card.html` and `templates/components/project_modal.html`) render project cards and modal dialogs with semantic IDs (`id="modal-{{ project.slug }}"`).
   - Supports keyboard `Escape` closing, backdrop clicks, and focus restoration.
3. **Resilient Zero-Downtime Fallback**:
   - If MongoDB Atlas is temporarily unreachable, the repository automatically falls back to curated static seed data so the portfolio never throws a `500 Server Error`.

---

## 🚀 Flagship Projects Featured

| Project | Domain | Tech Stack | Highlights |
| :--- | :--- | :--- | :--- |
| **Smart Traffic Management System** | Computer Vision / MLOps | YOLO, OpenCV, Apache Airflow, Python | Real-time vehicle detection, tracking, congestion density calculation, and automated batch pipeline orchestration. |
| **Stock Market ETL Pipeline** | Data Engineering | Kafka, Airflow, Snowflake, PostgreSQL | End-to-end streaming & batch ETL architecture for financial ticker ingestion, transformation, and analytical warehouse loading. |
| **Heart Disease Risk Classifier** | Machine Learning | Scikit-learn, XGBoost, SHAP, Python | Clinical risk prediction system featuring exploratory data analysis, ensemble modeling, and SHAP feature explainability. |
| **PIMA Diabetes Risk Classifier** | Machine Learning | Scikit-learn, Pandas, NumPy | Predictive healthcare analytics with data imputation, outlier detection, and model benchmarking. |
| **Gender Classification CNN** | Deep Learning / CV | PyTorch / TensorFlow, CNNs, OpenCV | Convolutional Neural Network trained on facial images for high-accuracy feature extraction and classification. |
| **MockAnalysis** | Automation & Data Engineering | Python, BeautifulSoup, Pandas | Automated extraction, validation, and performance benchmarking for testing data suites. |
| **BihariBlogger Platform** | Full-Stack Web Development | Flask, Jinja2, MongoDB, CSS3 | Social blogging web application with user sessions, markdown authoring, and dynamic feeds. |

---

## 📁 Repository Directory Structure

```text
CV_Project/
├── config.py                 # Centralized configuration (Development, Production, Testing)
├── app.py                    # Application factory (create_app), WSGI instance, security headers
├── Procfile                  # Production start command: gunicorn app:app --bind 0.0.0.0:$PORT
├── requirements.txt          # Production dependencies
│
├── models/                   # Domain data models
│   ├── __init__.py
│   └── project.py            # Project dataclass, slugify utility, devicon mapping
│
├── repositories/             # Data access layer
│   ├── __init__.py
│   └── project_repository.py # MongoDB CRUD operations & resilient static fallback
│
├── services/                 # Business logic layer
│   ├── __init__.py
│   ├── project_service.py    # Project normalization, validation, and filtering
│   ├── recaptcha_service.py  # Google reCAPTCHA v2 verification
│   └── email_service.py      # Sanitized SMTP email dispatch
│
├── routes/                   # Flask Blueprints
│   ├── __init__.py
│   ├── main.py               # Public portfolio pages, robots.txt, sitemap.xml
│   ├── contact.py            # Contact form submission, validation, honeypot
│   └── admin_projects.py     # Protected admin dashboard, authentication, CRUD routes
│
├── data/                     # Seed and static portfolio data
│   ├── __init__.py
│   ├── projects.py           # Static fallback projects & certifications
│   ├── experience.py         # Employment, education, and leadership details
│   └── skills.py             # Categorized technical skill taxonomy
│
├── static/                   # Static web assets
│   ├── css/                  # Modular styles (style.css, project_certificate.css, etc.)
│   ├── js/                   # Vanilla JS (main.js, contact.js, skill.js)
│   ├── images/               # Screenshots and profile assets
│   ├── icons/                # Technical SVG icons
│   └── CV_Mithilesh.pdf      # Downloadable resume document
│
├── templates/                # Jinja2 HTML templates
│   ├── base.html             # Base layout, navbar, SEO tags, JSON-LD schema
│   ├── index.html            # Hero & professional overview
│   ├── projects_certifications.html # Dynamic project cards & modal triggers
│   ├── academic_technical.html      # Experience timeline, education, skill badges
│   ├── contact.html          # Contact form view
│   ├── 404.html              # Custom error page
│   ├── components/           # Reusable template components
│   │   ├── project_card.html # Project card item
│   │   └── project_modal.html# Project modal dialog
│   └── admin/                # Admin CMS views
│       ├── login.html        # Secure admin sign-in form
│       └── projects/
│           ├── index.html    # CMS dashboard & project inventory
│           └── form.html     # Add / Edit project form
│
├── scripts/                  # Utilities
│   └── seed_projects.py      # Idempotent MongoDB Atlas database seeder
│
└── tests/                    # Automated test suite (Pytest)
    ├── __init__.py
    ├── test_app.py           # Core routes, security headers, canonical redirects
    └── test_project_cms.py   # 16-scenario comprehensive CMS test suite
```

---

## 🔒 Security Best Practices

- **Zero Tracked Secrets**: `.env` is strictly git-ignored; `.env.example` provides placeholders only.
- **Password Hashing**: Admin passwords use cryptographic scrypt hashing (`werkzeug.security`).
- **CSRF Protection**: State-changing POST endpoints enforce cryptographically signed session tokens.
- **Bot Mitigation**: Contact forms feature an invisible honeypot trap and Google reCAPTCHA v2 verification.
- **Hardened HTTP Headers**: Every response includes:
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: SAMEORIGIN`
  - `Referrer-Policy: strict-origin-when-cross-origin`
  - `Permissions-Policy: camera=(), microphone=(), geolocation=()`

---

## ⚙️ Environment Configuration

Create a `.env` file in the root directory (based on `.env.example`):

| Variable | Description | Example / Default |
| :--- | :--- | :--- |
| `FLASK_APP` | Application entry point | `app.py` |
| `FLASK_ENV` | Application environment | `production` / `development` |
| `SECRET_KEY` | Flask session secret key | Secure random string |
| `PORT` | Local server port | `5000` |
| `MONGODB_URI` | MongoDB Atlas connection string | `mongodb+srv://<user>:<pwd>@cluster.mongodb.net/?retryWrites=true&w=majority` |
| `MONGODB_DATABASE` | Database name | `portfolio` |
| `ADMIN_USERNAME` | Admin CMS login username | `admin` |
| `ADMIN_PASSWORD_HASH` | Hashed admin password | Werkzeug scrypt hash |
| `RECAPTCHA_SITE_KEY` | Google reCAPTCHA v2 Site Key | Optional |
| `RECAPTCHA_SECRET_KEY`| Google reCAPTCHA v2 Secret Key | Optional |
| `EMAIL_USER` | SMTP sender email address | Optional |
| `EMAIL_PASS` | SMTP application password | Optional |
| `EMAIL_RECEIVER` | Destination email address | `mithileshchaurasiya1627@gmail.com` |

---

## 🧪 Testing & Verification

The repository includes a comprehensive automated test suite covering all routes, security protections, and CMS scenarios using in-memory mock repositories and Flask test clients:

```bash
# Run the entire test suite (30 tests)
pytest -v

# Verify clean bytecode compilation
python -m compileall -x "(\.venv|\.git)" .

# Check for whitespace issues and git conflict markers
git diff --check
```

---

## 💻 Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mithilesh1627/CV_Project.git
   cd CV_Project
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   # Windows:
   .\.venv\Scripts\Activate.ps1
   # macOS / Linux:
   source .venv/bin/activate
   ```

3. **Install pinned dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up local environment**:
   ```bash
   cp .env.example .env
   # Populate your .env with your local settings or MongoDB Atlas URI
   ```

5. **(Optional) Seed MongoDB Atlas**:
   ```bash
   python scripts/seed_projects.py
   ```

6. **Start the local server**:
   ```bash
   python app.py
   ```
   Open `http://127.0.0.1:5000` in your browser.<br>
   To manage projects, visit `http://127.0.0.1:5000/admin/login`.

---

## 📬 Contact & Connect

- **Portfolio**: [https://mithileshchaurasiya.me/](https://mithileshchaurasiya.me/)
- **Email**: [mithileshchaurasiya1627@gmail.com](mailto:mithileshchaurasiya1627@gmail.com)
- **LinkedIn**: [linkedin.com/in/mithileshchaurasiya](https://www.linkedin.com/in/mithileshchaurasiya/)
- **GitHub**: [github.com/mithilesh1627](https://github.com/mithilesh1627)
- **LeetCode**: [leetcode.com/u/Mithilesh_1627](https://leetcode.com/u/Mithilesh_1627/)

---

<p align="center">
  <sub>© 2026 Mithilesh Chaurasiya. Built with Python, Flask & MongoDB Atlas.</sub>
</p>
