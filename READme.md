# Mithilesh Chaurasiya — Personal Portfolio & Engineering Showcase

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12%20%7C%203.13-3776AB?logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.0-000000?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas%20%7C%20PyMongo-47A248?logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Render](https://img.shields.io/badge/Deployed-Render-46E3B7?logo=render&logoColor=white)](https://render.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

🟢 **Live Website**: [https://mithileshchaurasiya.me/](https://mithileshchaurasiya.me/)
📂 **Source Code**: [https://github.com/mithilesh1627/CV_Project](https://github.com/mithilesh1627/CV_Project)

---

## 📌 Overview

This repository powers the personal engineering portfolio of **Mithilesh Chaurasiya**, targeted for **AI Engineer**, **Machine Learning Engineer**, and **MLOps Engineer** roles.

It highlights:
- **2.8 Years at Infosys** across production data engineering, ETL pipeline validation, and MLOps tooling adoption.
- **MCA @ National Institute of Technology, Agartala (2024–2027)** & ML Team Lead at the Developers & Coders Club (DCC).
- **Production Systems**: Computer Vision (YOLO, OpenCV), MLOps pipelines (Apache Airflow, MLflow, DVC), and Agentic AI architectures.

---

## 🛠️ Tech Stack & Architecture

- **Backend Framework**: Python 3.12+, Flask 3.1.0 (Application Factory pattern, Blueprints)
- **Database & CMS**: MongoDB Atlas / PyMongo (NoSQL structured document storage, slug indexing, repository pattern)
- **Templating**: Jinja2 (Dynamic reusable components for cards & modals, OpenGraph, JSON-LD schema)
- **Frontend**: Semantic HTML5, CSS3 Custom Properties (Dark Slate Design System), Vanilla JavaScript (Accessible Dialogs & Tabs)
- **Form Security**: Session CSRF protection, Bot Honeypot, Google reCAPTCHA v2, header-sanitized SMTP delivery via `email.message.EmailMessage`
- **Deployment**: Render Web Service via Gunicorn with custom domain and HTTPS

---

## 📁 Project Structure

```text
CV_Project/
├── config.py                 # Central configuration (Development, Production, Testing)
├── app.py                    # Application factory and WSGI entrypoint
├── models/
│   └── project.py            # Project domain model, slugify, safe tech icon mapping
├── repositories/
│   └── project_repository.py # MongoDB CRUD repository with resilient offline fallback
├── services/
│   ├── project_service.py    # Business logic, input validation, list normalization
│   ├── email_service.py      # Header-sanitized SMTP delivery via EmailMessage
│   └── recaptcha_service.py  # Google reCAPTCHA v2 verification
├── routes/
│   ├── main.py               # Home, Projects, Academic, robots.txt, sitemap.xml
│   ├── contact.py            # Secure contact form, CSRF, honeypot, validation
│   └── admin_projects.py     # Protected Admin Project CMS (auth, CSRF, CRUD)
├── data/
│   ├── projects.py           # Seed project & certification data
│   ├── experience.py         # Verified employment, education, leadership
│   └── skills.py             # Categorized skill taxonomy
├── static/
│   ├── css/                  # Modular stylesheets
│   ├── js/                   # Accessible vanilla JS
│   ├── images/               # Screenshots and profile assets
│   └── CV_Mithilesh.pdf      # Resume document
├── templates/
│   ├── index.html            # Dynamic homepage rendering featured projects
│   ├── projects_certifications.html # Dynamic all-projects catalog
│   ├── components/           # Reusable Jinja template components
│   │   ├── project_card.html # Dynamic project card component
│   │   └── project_modal.html# Dynamic accessible modal dialog component
│   └── admin/
│       ├── login.html        # Admin sign-in view
│       └── projects/
│           ├── index.html    # CMS dashboard & project inventory
│           └── form.html     # Create / Edit project form
├── scripts/
│   └── seed_projects.py      # Idempotent MongoDB seed utility
├── tests/
│   ├── test_app.py           # Core portfolio routes & security test suite
│   └── test_project_cms.py   # Complete 16-scenario Project CMS test suite
├── .env.example              # Documented environment variables
├── .gitignore                # Clean Python/Flask ignore rules
├── Procfile                  # Gunicorn start command for Render
└── requirements.txt          # Pinned production dependencies
```

---

## 📦 Dynamic Project CMS

The portfolio features a fully dynamic, MongoDB-backed Project Content Management System (CMS). Projects and their complete modal dialogs are no longer hardcoded inside HTML templates.

### Workflow

```text
Add / Edit Project in Admin CMS
            ↓
       Flask Route (/admin/projects)
            ↓
       Project Service (Validation & Normalization)
            ↓
       Project Repository
            ↓
       MongoDB Collection (`projects`)
            ↓
       Public Routes (/ & /projects_certifications)
            ↓
       Jinja2 Components (`project_card.html`, `project_modal.html`)
            ↓
       Portfolio Automatically Updated
```

- **MongoDB** stores structured content, metadata, and arrays (technologies, features, challenges, future improvements).
- **Flask & ProjectService** handle validation, unique slug generation, sorting, and publish state.
- **Jinja Components** render project cards and modal windows dynamically (`id="modal-{{ project.slug }}"`).
- **Resilient Fallback**: If MongoDB is temporarily unreachable or unconfigured, the repository automatically falls back to static seed data—ensuring the live portfolio never crashes with a 500 error.
- **Admin Dashboard**: Accessible at `/admin/login`, allowing full creation, editing, deletion, and publish toggling without touching code.

---

## 🚀 Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/mithilesh1627/CV_Project.git
   cd CV_Project
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your MongoDB URI, Admin credentials, and Email settings
   ```

5. **Seed existing projects to MongoDB**:
   ```bash
   python scripts/seed_projects.py
   ```

6. **Run the test suite**:
   ```bash
   pytest -v
   ```

7. **Start local development server**:
   ```bash
   python app.py
   ```
   Open `http://127.0.0.1:5000` in your browser.<br>
   To manage projects, visit `http://127.0.0.1:5000/admin/login`.

---

## 🔒 Security & Deployment Considerations

- **MongoDB Protection**: Connection strings are read exclusively from environment variables and never logged or exposed.
- **Admin Authentication**: Uses hashed passwords verified via `werkzeug.security.check_password_hash`. All state-changing admin actions enforce CSRF tokens.
- **Production Headers**: Includes `X-Content-Type-Options: nosniff`, `X-Frame-Options: SAMEORIGIN`, and strict referrer policy.
- **Render Start Command**: Configured in `Procfile` (`web: gunicorn app:app --bind 0.0.0.0:$PORT`).

---

## 📬 Contact & Connect

- **Email**: [mithileshchaurasiya1627@gmail.com](mailto:mithileshchaurasiya1627@gmail.com)
- **LinkedIn**: [linkedin.com/in/mithileshchaurasiya](https://www.linkedin.com/in/mithileshchaurasiya/)
- **GitHub**: [github.com/mithilesh1627](https://github.com/mithilesh1627)
- **LeetCode**: [leetcode.com/u/Mithilesh_1627](https://leetcode.com/u/Mithilesh_1627/)
