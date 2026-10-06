from datetime import datetime, timezone
from flask import Blueprint, render_template, make_response, url_for, request, redirect, current_app

from data.projects import CERTIFICATIONS
from data.experience import EXPERIENCE, EDUCATION, LEADERSHIP
from data.skills import SKILL_CATEGORIES
from services.project_service import ProjectService
from repositories.project_repository import ProjectRepository

main_bp = Blueprint("main", __name__)


def get_project_service() -> ProjectService:
    """Instantiate ProjectService dynamically with current app configuration."""
    repo = ProjectRepository(
        mongo_uri=current_app.config.get("MONGODB_URI", ""),
        db_name=current_app.config.get("MONGODB_DATABASE", "portfolio")
    )
    return ProjectService(repository=repo)


@main_bp.route("/")
def home():
    service = get_project_service()
    featured_projects = service.get_featured_projects(limit=6)
    return render_template(
        "index.html",
        title="Mithilesh Chaurasiya | AI Engineer | ML Engineer | MLOps",
        featured_projects=featured_projects,
    )


@main_bp.route("/projects")
@main_bp.route("/projects_certifications")
def projects():
    service = get_project_service()
    all_projects = service.get_projects(published_only=True)
    all_certificates = service.get_certificates()

    categories = [
        {"id": "all", "label": "All Projects"},
        {"id": "systems", "label": "Distributed Systems"},
        {"id": "ai-mlops", "label": "AI & MLOps"},
        {"id": "generative-ai", "label": "Generative AI"},
        {"id": "data-engineering", "label": "Data Engineering"},
        {"id": "machine-learning", "label": "Machine Learning"},
        {"id": "computer-vision", "label": "Computer Vision"},
    ]
    return render_template(
        "projects_certifications.html",
        title="Projects & Certifications | Mithilesh Chaurasiya",
        projects=all_projects,
        categories=categories,
        certifications=all_certificates,
    )


@main_bp.route("/experience")
def experience_alias():
    return redirect(url_for("main.academic") + "#experience")


@main_bp.route("/skills")
def skills_alias():
    return redirect(url_for("main.academic") + "#skills")


@main_bp.route("/academic_technical")
def academic():
    return render_template(
        "academic_technical.html",
        title="Experience & Technical Skills | Mithilesh Chaurasiya",
        experience=EXPERIENCE,
        leadership=LEADERSHIP,
        education=EDUCATION,
        skill_categories=SKILL_CATEGORIES,
    )


@main_bp.route("/robots.txt")
def robots_txt():
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "Disallow: /admin/\n"
        "Disallow: /static/CV_Mithilesh.pdf\n\n"
        "Sitemap: https://mithileshchaurasiya.me/sitemap.xml\n"
    )
    response = make_response(content, 200)
    response.headers["Content-Type"] = "text/plain; charset=utf-8"
    return response


@main_bp.route("/sitemap.xml")
def sitemap_xml():
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    base_url = "https://mithileshchaurasiya.me"
    pages = [
        {"loc": f"{base_url}/", "priority": "1.0", "changefreq": "monthly"},
        {"loc": f"{base_url}/projects_certifications", "priority": "0.9", "changefreq": "monthly"},
        {"loc": f"{base_url}/academic_technical", "priority": "0.8", "changefreq": "monthly"},
        {"loc": f"{base_url}/contact", "priority": "0.7", "changefreq": "monthly"},
    ]
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for page in pages:
        xml_content += "  <url>\n"
        xml_content += f"    <loc>{page['loc']}</loc>\n"
        xml_content += f"    <lastmod>{now_str}</lastmod>\n"
        xml_content += f"    <changefreq>{page['changefreq']}</changefreq>\n"
        xml_content += f"    <priority>{page['priority']}</priority>\n"
        xml_content += "  </url>\n"
    xml_content += "</urlset>"

    response = make_response(xml_content, 200)
    response.headers["Content-Type"] = "application/xml; charset=utf-8"
    return response
