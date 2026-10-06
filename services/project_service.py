"""
Project Service Layer.
Encapsulates business logic, validation, slug generation, normalization, and template preparation.
"""

import logging
import re
from typing import List, Dict, Any, Optional
from models.project import Project, slugify
from repositories.project_repository import ProjectRepository

logger = logging.getLogger(__name__)

URL_REGEX = re.compile(
    r"^(https?://)?"  # http:// or https:// (optional in user input, normalized to https://)
    r"([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}"  # domain
    r"(:[0-9]+)?"  # optional port
    r"(/.*)?$"  # path
)


class ProjectService:
    """Service handling validation, normalization, and business rules for projects."""

    def __init__(self, repository: Optional[ProjectRepository] = None):
        self.repo = repository or ProjectRepository()

    def get_projects(self, published_only: bool = True) -> List[Project]:
        """Fetch all projects converted into Project models."""
        docs = self.repo.find_all(published_only=published_only)
        projects = []
        for doc in docs:
            try:
                projects.append(Project.from_doc(doc))
            except Exception as e:
                logger.warning("Skipping malformed project document: %s", e)
        return projects

    def get_featured_projects(self, limit: int = 6) -> List[Project]:
        """Fetch featured projects for homepage display."""
        docs = self.repo.find_featured(limit=limit)
        projects = []
        for doc in docs:
            try:
                projects.append(Project.from_doc(doc))
            except Exception as e:
                logger.warning("Skipping malformed featured project document: %s", e)
        return projects

    def get_project(self, slug: str) -> Optional[Project]:
        """Fetch a single project by slug."""
        if not slug:
            return None
        doc = self.repo.find_by_slug(slug)
        if not doc:
            return None
        try:
            return Project.from_doc(doc)
        except Exception as e:
            logger.error("Error creating Project model for slug '%s': %s", slug, e)
            return None

    def validate_project_data(self, data: Dict[str, Any], is_update: bool = False, current_slug: str = "") -> List[str]:
        """Validate project input data. Returns a list of error message strings."""
        errors = []

        title = str(data.get("title", "")).strip()
        if not title:
            errors.append("Project title is required.")
        elif len(title) > 150:
            errors.append("Project title must not exceed 150 characters.")

        slug = str(data.get("slug", "")).strip()
        if not slug and not is_update:
            slug = slugify(title)

        if slug:
            clean_slug = slugify(slug)
            if not clean_slug:
                errors.append("Invalid project slug format.")
            # Uniqueness check
            if not is_update or (is_update and clean_slug != current_slug):
                existing = self.repo.find_by_slug(clean_slug)
                if existing:
                    errors.append(f"Project slug '{clean_slug}' is already in use. Please provide a unique slug.")

        github_url = str(data.get("github_url", "")).strip()
        if github_url and not URL_REGEX.match(github_url):
            errors.append("GitHub URL is invalid.")

        live_url = str(data.get("live_url", "")).strip()
        if live_url and not URL_REGEX.match(live_url):
            errors.append("Live demo URL is invalid.")

        return errors

    def normalize_list_input(self, val: Any) -> List[str]:
        """Convert textarea newline/comma input or lists into a clean list of strings."""
        if isinstance(val, list):
            return [str(item).strip() for item in val if str(item).strip()]
        if not val or not isinstance(val, str):
            return []
        # Split by newlines or commas
        lines = val.replace("\r\n", "\n").replace("\r", "\n").split("\n")
        items = []
        for line in lines:
            line_str = line.strip()
            # If line has bullet points, strip them
            line_str = re.sub(r"^[-*•▹]\s*", "", line_str).strip()
            if line_str:
                items.append(line_str)
        return items

    def create_project(self, data: Dict[str, Any]) -> Project:
        """Validate, normalize, and save a new project to the database."""
        errors = self.validate_project_data(data, is_update=False)
        if errors:
            raise ValueError("; ".join(errors))

        title = str(data.get("title", "")).strip()
        user_slug = str(data.get("slug", "")).strip()
        slug = slugify(user_slug) if user_slug else slugify(title)

        # Make sure slug is unique
        base_slug = slug
        counter = 1
        while self.repo.find_by_slug(slug) is not None:
            slug = f"{base_slug}-{counter}"
            counter += 1

        project = Project(
            title=title,
            slug=slug,
            subtitle=str(data.get("subtitle", "")).strip(),
            short_description=str(data.get("short_description", "")).strip(),
            description=str(data.get("description", "")).strip(),
            status=str(data.get("status", "completed")).strip() or "completed",
            featured=bool(data.get("featured", False)),
            featured_order=int(data.get("featured_order", 0) or 0),
            category=str(data.get("category", "systems")).strip() or "systems",
            badge=str(data.get("badge", "")).strip(),
            image=str(data.get("image", "images/poster1.png")).strip() or "images/poster1.png",
            github_url=str(data.get("github_url", "")).strip(),
            live_url=str(data.get("live_url", "")).strip(),
            demo_label=str(data.get("demo_label", "Launch Live App")).strip() or "Launch Live App",
            technologies=self.normalize_list_input(data.get("technologies")),
            features=self.normalize_list_input(data.get("features")),
            challenges=self.normalize_list_input(data.get("challenges")),
            future_improvements=self.normalize_list_input(data.get("future_improvements")),
            published=bool(data.get("published", True)),
        )

        doc = project.to_doc()
        self.repo.insert(doc)
        return project

    def update_project(self, slug: str, data: Dict[str, Any]) -> Project:
        """Validate, normalize, and update an existing project."""
        existing = self.repo.find_by_slug(slug)
        if not existing:
            raise KeyError(f"Project with slug '{slug}' not found.")

        errors = self.validate_project_data(data, is_update=True, current_slug=slug)
        if errors:
            raise ValueError("; ".join(errors))

        new_title = str(data.get("title", existing.get("title"))).strip()
        new_slug = slugify(data.get("slug")) if data.get("slug") else slug

        update_doc = {
            "title": new_title,
            "slug": new_slug,
            "subtitle": str(data.get("subtitle", existing.get("subtitle", ""))).strip(),
            "short_description": str(data.get("short_description", existing.get("short_description", ""))).strip(),
            "description": str(data.get("description", existing.get("description", ""))).strip(),
            "status": str(data.get("status", existing.get("status", "completed"))).strip() or "completed",
            "featured": bool(data.get("featured", existing.get("featured", False))),
            "featured_order": int(data.get("featured_order", existing.get("featured_order", 0)) or 0),
            "category": str(data.get("category", existing.get("category", "systems"))).strip() or "systems",
            "badge": str(data.get("badge", existing.get("badge", ""))).strip(),
            "image": str(data.get("image", existing.get("image", "images/poster1.png"))).strip() or "images/poster1.png",
            "github_url": str(data.get("github_url", existing.get("github_url", ""))).strip(),
            "live_url": str(data.get("live_url", existing.get("live_url", ""))).strip(),
            "demo_label": str(data.get("demo_label", existing.get("demo_label", "Launch Live App"))).strip() or "Launch Live App",
            "technologies": self.normalize_list_input(data.get("technologies", existing.get("technologies", []))),
            "features": self.normalize_list_input(data.get("features", existing.get("features", []))),
            "challenges": self.normalize_list_input(data.get("challenges", existing.get("challenges", []))),
            "future_improvements": self.normalize_list_input(data.get("future_improvements", existing.get("future_improvements", []))),
            "published": bool(data.get("published", existing.get("published", True))),
        }

        self.repo.update(slug, update_doc)
        return Project.from_doc(update_doc)

    def delete_project(self, slug: str) -> bool:
        """Delete a project by slug."""
        return self.repo.delete(slug)

    def toggle_publish(self, slug: str) -> bool:
        """Toggle a project's published visibility."""
        doc = self.repo.find_by_slug(slug)
        if not doc:
            raise KeyError(f"Project '{slug}' not found.")
        current_status = bool(doc.get("published", True))
        return self.repo.set_published(slug, not current_status)

    def get_certificates(self) -> List[Dict[str, Any]]:
        """Fetch all certificates from the repository."""
        return self.repo.find_all_certificates()
