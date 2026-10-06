"""
Admin Project CMS Blueprint.
Provides protected administrative interface to manage portfolio projects in MongoDB.
"""

import functools
import secrets
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session, current_app
)
from werkzeug.security import check_password_hash
from services.project_service import ProjectService
from repositories.project_repository import ProjectRepository
from config import Config

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# Initialize service instance using application config
def get_project_service() -> ProjectService:
    repo = ProjectRepository(
        mongo_uri=current_app.config.get("MONGODB_URI", ""),
        db_name=current_app.config.get("MONGODB_DATABASE", "portfolio")
    )
    return ProjectService(repository=repo)


def get_or_create_csrf_token() -> str:
    """Retrieve or create session CSRF token for admin actions."""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)
    return session["csrf_token"]


def validate_csrf() -> bool:
    """Validate submitted CSRF token against session."""
    token = request.form.get("csrf_token", "")
    return bool(token and token == session.get("csrf_token"))


def admin_required(view_func):
    """Decorator ensuring that only authenticated admins can access the endpoint."""
    @functools.wraps(view_func)
    def decorated_view(*args, **kwargs):
        if not session.get("admin_logged_in"):
            flash("Please sign in to access the Admin Project CMS.", "warning")
            return redirect(url_for("admin.login", next=request.url))
        return view_func(*args, **kwargs)
    return decorated_view


# -----------------------------------------------------------------------------
# Authentication Routes
# -----------------------------------------------------------------------------

@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    """Admin login page."""
    if session.get("admin_logged_in"):
        return redirect(url_for("admin.projects_list"))

    csrf_token = get_or_create_csrf_token()

    if request.method == "POST":
        if not validate_csrf():
            flash("Invalid security token. Please try again.", "error")
            return render_template("admin/login.html", csrf_token=csrf_token)

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        configured_user = current_app.config.get("ADMIN_USERNAME", "admin")
        configured_hash = current_app.config.get("ADMIN_PASSWORD_HASH", "")

        if username == configured_user and configured_hash and check_password_hash(configured_hash, password):
            session["admin_logged_in"] = True
            session["admin_user"] = username
            flash("Signed in successfully.", "success")
            next_url = request.args.get("next") or url_for("admin.projects_list")
            return redirect(next_url)
        else:
            flash("Invalid administrator credentials.", "error")

    return render_template("admin/login.html", csrf_token=csrf_token)


@admin_bp.route("/logout")
def logout():
    """Sign out the current administrator."""
    session.pop("admin_logged_in", None)
    session.pop("admin_user", None)
    flash("Signed out successfully.", "info")
    return redirect(url_for("admin.login"))


# -----------------------------------------------------------------------------
# Project Management Routes
# -----------------------------------------------------------------------------

@admin_bp.route("/")
@admin_bp.route("/projects")
@admin_required
def projects_list():
    """List all projects in the database."""
    service = get_project_service()
    projects = service.get_projects(published_only=False)
    csrf_token = get_or_create_csrf_token()
    is_connected = service.repo.is_connected()
    return render_template(
        "admin/projects/index.html",
        projects=projects,
        csrf_token=csrf_token,
        is_connected=is_connected
    )


@admin_bp.route("/projects/new", methods=["GET", "POST"])
@admin_required
def project_new():
    """Create a new project."""
    service = get_project_service()
    csrf_token = get_or_create_csrf_token()

    if request.method == "POST":
        if not validate_csrf():
            flash("Invalid security token.", "error")
            return redirect(url_for("admin.project_new"))

        data = {
            "title": request.form.get("title", ""),
            "slug": request.form.get("slug", ""),
            "subtitle": request.form.get("subtitle", ""),
            "short_description": request.form.get("short_description", ""),
            "description": request.form.get("description", ""),
            "status": request.form.get("status", "completed"),
            "featured": bool(request.form.get("featured")),
            "featured_order": request.form.get("featured_order", 0),
            "category": request.form.get("category", "systems"),
            "badge": request.form.get("badge", ""),
            "image": request.form.get("image", "images/poster1.png"),
            "github_url": request.form.get("github_url", ""),
            "live_url": request.form.get("live_url", ""),
            "demo_label": request.form.get("demo_label", "Launch Live App"),
            "technologies": request.form.get("technologies", ""),
            "features": request.form.get("features", ""),
            "challenges": request.form.get("challenges", ""),
            "future_improvements": request.form.get("future_improvements", ""),
            "published": bool(request.form.get("published")),
        }

        try:
            created = service.create_project(data)
            flash(f"Project '{created.title}' created and published successfully!", "success")
            return redirect(url_for("admin.projects_list"))
        except (ValueError, RuntimeError) as err:
            flash(f"Error: {err}", "error")
            return render_template(
                "admin/projects/form.html",
                project=data,
                csrf_token=csrf_token,
                is_edit=False
            )

    return render_template(
        "admin/projects/form.html",
        project={},
        csrf_token=csrf_token,
        is_edit=False
    )


@admin_bp.route("/projects/<slug>/edit", methods=["GET", "POST"])
@admin_required
def project_edit(slug):
    """Edit an existing project."""
    service = get_project_service()
    project = service.get_project(slug)
    if not project:
        flash(f"Project '{slug}' not found.", "error")
        return redirect(url_for("admin.projects_list"))

    csrf_token = get_or_create_csrf_token()

    if request.method == "POST":
        if not validate_csrf():
            flash("Invalid security token.", "error")
            return redirect(url_for("admin.project_edit", slug=slug))

        data = {
            "title": request.form.get("title", ""),
            "slug": request.form.get("slug", slug),
            "subtitle": request.form.get("subtitle", ""),
            "short_description": request.form.get("short_description", ""),
            "description": request.form.get("description", ""),
            "status": request.form.get("status", "completed"),
            "featured": bool(request.form.get("featured")),
            "featured_order": request.form.get("featured_order", 0),
            "category": request.form.get("category", "systems"),
            "badge": request.form.get("badge", ""),
            "image": request.form.get("image", "images/poster1.png"),
            "github_url": request.form.get("github_url", ""),
            "live_url": request.form.get("live_url", ""),
            "demo_label": request.form.get("demo_label", "Launch Live App"),
            "technologies": request.form.get("technologies", ""),
            "features": request.form.get("features", ""),
            "challenges": request.form.get("challenges", ""),
            "future_improvements": request.form.get("future_improvements", ""),
            "published": bool(request.form.get("published")),
        }

        try:
            updated = service.update_project(slug, data)
            flash(f"Project '{updated.title}' updated successfully!", "success")
            return redirect(url_for("admin.projects_list"))
        except (ValueError, RuntimeError, KeyError) as err:
            flash(f"Update error: {err}", "error")
            return render_template(
                "admin/projects/form.html",
                project=data,
                csrf_token=csrf_token,
                is_edit=True,
                slug=slug
            )

    # Convert project model to form dictionary with newline-separated strings
    form_data = project.to_doc()
    form_data["technologies"] = "\n".join(project.technologies)
    form_data["features"] = "\n".join(project.features)
    form_data["challenges"] = "\n".join(project.challenges)
    form_data["future_improvements"] = "\n".join(project.future_improvements)

    return render_template(
        "admin/projects/form.html",
        project=form_data,
        csrf_token=csrf_token,
        is_edit=True,
        slug=slug
    )


@admin_bp.route("/projects/<slug>/delete", methods=["POST"])
@admin_required
def project_delete(slug):
    """Delete a project."""
    if not validate_csrf():
        flash("Invalid security token.", "error")
        return redirect(url_for("admin.projects_list"))

    service = get_project_service()
    try:
        service.delete_project(slug)
        flash(f"Project '{slug}' has been removed.", "info")
    except Exception as err:
        flash(f"Delete failed: {err}", "error")

    return redirect(url_for("admin.projects_list"))


@admin_bp.route("/projects/<slug>/publish", methods=["POST"])
@admin_required
def project_toggle_publish(slug):
    """Toggle publish visibility status."""
    if not validate_csrf():
        flash("Invalid security token.", "error")
        return redirect(url_for("admin.projects_list"))

    service = get_project_service()
    try:
        service.toggle_publish(slug)
        flash(f"Publish status updated for '{slug}'.", "success")
    except Exception as err:
        flash(f"Failed to update status: {err}", "error")

    return redirect(url_for("admin.projects_list"))
