"""
Project domain model for the Portfolio Project CMS.
Provides typed access, validation, safe deserialization from MongoDB, and safe icon mapping.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
import re


TECH_ICON_MAP: Dict[str, str] = {
    "python": "devicon-python-plain",
    "python 3.12": "devicon-python-plain",
    "fastapi": "devicon-fastapi-plain",
    "flask": "devicon-flask-original",
    "react flow": "devicon-react-original",
    "react": "devicon-react-original",
    "next.js": "devicon-nextjs-plain",
    "next.js 14": "devicon-nextjs-plain",
    "postgresql": "devicon-postgresql-plain",
    "postgres": "devicon-postgresql-plain",
    "mongodb": "devicon-mongodb-plain",
    "tailwind css": "devicon-tailwindcss-plain",
    "tailwind": "devicon-tailwindcss-plain",
    "bootstrap": "devicon-bootstrap-plain",
    "bootstrap 5": "devicon-bootstrap-plain",
    "html": "devicon-html5-plain",
    "html5": "devicon-html5-plain",
    "css": "devicon-css3-plain",
    "css3": "devicon-css3-plain",
    "javascript": "devicon-javascript-plain",
    "docker": "devicon-docker-plain",
    "apache airflow": "devicon-apacheairflow-plain",
    "airflow": "devicon-apacheairflow-plain",
    "mlflow": "fas fa-flask",
    "dvc": "devicon-git-plain",
    "pytorch": "devicon-pytorch-original",
    "opencv": "devicon-opencv-plain",
    "yolo": "devicon-python-plain",
    "yolo (ultralytics)": "devicon-python-plain",
    "streamlit": "devicon-streamlit-plain",
    "pandas": "devicon-pandas-plain",
    "numpy": "devicon-numpy-plain",
    "scikit-learn": "devicon-scikitlearn-plain",
    "sklearn": "devicon-scikitlearn-plain",
    "tensorflow": "devicon-tensorflow-original",
    "keras": "devicon-keras-plain",
    "selenium": "devicon-selenium-original",
    "jupyter": "devicon-jupyter-plain-wordmark",
    "jupyter notebook": "devicon-jupyter-plain-wordmark",
    "matplotlib": "devicon-matplotlib-plain",
    "git": "devicon-git-plain",
}


def slugify(text: str) -> str:
    """Generate a clean, URL-safe slug from text."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    return text.strip("-")


@dataclass
class Project:
    """Domain model representing a portfolio project."""
    title: str
    slug: str
    subtitle: str = ""
    short_description: str = ""
    description: str = ""
    status: str = "completed"
    featured: bool = False
    featured_order: int = 0
    category: str = "systems"
    badge: str = ""
    image: str = "images/poster1.png"
    github_url: str = ""
    live_url: str = ""
    demo_label: str = "Launch Live App"
    technologies: List[str] = field(default_factory=list)
    features: List[str] = field(default_factory=list)
    challenges: List[str] = field(default_factory=list)
    future_improvements: List[str] = field(default_factory=list)
    published: bool = True
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    id: Optional[str] = None

    @property
    def modal_id(self) -> str:
        """Stable modal identifier used in HTML and JavaScript."""
        return f"modal-{self.slug}"

    @property
    def tech_items(self) -> List[Dict[str, str]]:
        """
        Return structured technology items with safe CSS icon classes.
        Avoids storing or injecting arbitrary HTML from the database.
        """
        items = []
        for tech in self.technologies:
            clean_name = str(tech).strip()
            if not clean_name:
                continue
            icon_class = TECH_ICON_MAP.get(clean_name.lower(), "fas fa-code")
            items.append({"name": clean_name, "icon": icon_class})
        return items

    def to_doc(self) -> Dict[str, Any]:
        """Convert model to MongoDB document dictionary."""
        doc = {
            "title": self.title,
            "slug": self.slug,
            "subtitle": self.subtitle,
            "short_description": self.short_description,
            "description": self.description,
            "status": self.status,
            "featured": bool(self.featured),
            "featured_order": int(self.featured_order or 0),
            "category": self.category,
            "badge": self.badge,
            "image": self.image or "images/poster1.png",
            "github_url": self.github_url or "",
            "live_url": self.live_url or "",
            "demo_label": self.demo_label or "Launch Live App",
            "technologies": [str(t).strip() for t in self.technologies if str(t).strip()],
            "features": [str(f).strip() for f in self.features if str(f).strip()],
            "challenges": [str(c).strip() for c in self.challenges if str(c).strip()],
            "future_improvements": [str(fi).strip() for fi in self.future_improvements if str(fi).strip()],
            "published": bool(self.published),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        return doc

    @classmethod
    def from_doc(cls, doc: Dict[str, Any]) -> "Project":
        """Safely create a Project instance from a MongoDB document or dictionary."""
        if not doc:
            raise ValueError("Document cannot be empty")

        doc_id = str(doc.get("_id")) if doc.get("_id") is not None else None
        title = doc.get("title", "").strip()
        slug = doc.get("slug") or slugify(title)

        # Handle technologies if given as strings or list of dicts (from legacy data)
        raw_techs = doc.get("technologies") or doc.get("tech_stack") or []
        tech_list = []
        for t in raw_techs:
            if isinstance(t, dict):
                tech_list.append(t.get("name", ""))
            elif isinstance(t, str):
                tech_list.append(t)

        # Handle description / overview legacy mapping
        desc = doc.get("description") or doc.get("overview") or ""
        short_desc = doc.get("short_description") or doc.get("tagline") or doc.get("problem_statement") or ""
        live_url = doc.get("live_url") or doc.get("demo_url") or ""

        # Handle features / highlights legacy mapping
        feats = doc.get("features") or doc.get("engineering_highlights") or []

        return cls(
            id=doc_id,
            title=title,
            slug=slug,
            subtitle=doc.get("subtitle", "") or "",
            short_description=short_desc,
            description=desc,
            status=doc.get("status", "completed") or "completed",
            featured=bool(doc.get("featured", False)),
            featured_order=int(doc.get("featured_order", 0) or 0),
            category=doc.get("category", "systems") or "systems",
            badge=doc.get("badge", "") or "",
            image=doc.get("image", "images/poster1.png") or "images/poster1.png",
            github_url=doc.get("github_url", "") or "",
            live_url=live_url,
            demo_label=doc.get("demo_label", "Launch Live App") or "Launch Live App",
            technologies=[t for t in tech_list if t],
            features=[str(f) for f in feats if f],
            challenges=[str(c) for c in (doc.get("challenges") or []) if c],
            future_improvements=[str(fi) for fi in (doc.get("future_improvements") or []) if fi],
            published=doc.get("published", True),
            created_at=str(doc.get("created_at", datetime.now(timezone.utc).isoformat())),
            updated_at=str(doc.get("updated_at", datetime.now(timezone.utc).isoformat())),
        )
