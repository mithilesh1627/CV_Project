"""
MongoDB Project Repository.
Provides clean data access to the MongoDB 'projects' collection with graceful offline fallback.
"""

import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
import pymongo
from pymongo.errors import PyMongoError, ServerSelectionTimeoutError, ConnectionFailure

logger = logging.getLogger(__name__)


class ProjectRepository:
    """Repository handling all MongoDB CRUD operations for projects."""

    def __init__(self, mongo_uri: str = "", db_name: str = "portfolio", client: Optional[pymongo.MongoClient] = None):
        self.mongo_uri = mongo_uri.strip() if mongo_uri else ""
        self.db_name = db_name or "portfolio"
        self._client = client
        self._connected: Optional[bool] = None

    def _get_client(self) -> Optional[pymongo.MongoClient]:
        """Get or initialize the MongoClient with a fast connection timeout."""
        if self._client is not None:
            return self._client

        if not self.mongo_uri:
            return None

        try:
            self._client = pymongo.MongoClient(
                self.mongo_uri,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000,
                appName="PortfolioCMS"
            )
            # Verify connectivity with a ping
            self._client.admin.command("ping")
            self._connected = True
            logger.info("MongoDB connected successfully to database: %s", self.db_name)
            return self._client
        except (ServerSelectionTimeoutError, ConnectionFailure, PyMongoError) as err:
            logger.warning("MongoDB unavailable. Falling back to local static project data. Error: %s", type(err).__name__)
            self._connected = False
            self._client = None
            return None

    def get_collection(self):
        """Return the 'projects' MongoDB collection, or None if unavailable."""
        client = self._get_client()
        if client is None:
            return None
        return client[self.db_name]["projects"]

    def ensure_indexes(self) -> bool:
        """Create required indexes on the projects collection."""
        col = self.get_collection()
        if col is None:
            return False
        try:
            col.create_index([("slug", pymongo.ASCENDING)], unique=True)
            col.create_index([("featured", pymongo.ASCENDING), ("featured_order", pymongo.ASCENDING)])
            col.create_index([("published", pymongo.ASCENDING)])
            return True
        except PyMongoError as err:
            logger.error("Failed to ensure MongoDB indexes: %s", type(err).__name__)
            return False

    def is_connected(self) -> bool:
        """Check if active MongoDB connection is available."""
        return self._get_client() is not None

    def find_all(self, published_only: bool = True) -> List[Dict[str, Any]]:
        """Retrieve all projects, optionally filtering by published status."""
        col = self.get_collection()
        if col is None:
            return self._get_fallback_projects(published_only=published_only)

        try:
            query = {"published": True} if published_only else {}
            cursor = col.find(query).sort([("featured_order", pymongo.ASCENDING), ("created_at", pymongo.DESCENDING)])
            return list(cursor)
        except PyMongoError as err:
            logger.warning("find_all failed: %s. Using static fallback.", type(err).__name__)
            return self._get_fallback_projects(published_only=published_only)

    def find_featured(self, limit: int = 6) -> List[Dict[str, Any]]:
        """Retrieve featured projects for homepage display."""
        col = self.get_collection()
        if col is None:
            fallback = self._get_fallback_projects(published_only=True)
            return [p for p in fallback if p.get("featured")][:limit]

        try:
            query = {"published": True, "featured": True}
            cursor = col.find(query).sort("featured_order", pymongo.ASCENDING).limit(limit)
            return list(cursor)
        except PyMongoError as err:
            logger.warning("find_featured failed: %s. Using static fallback.", type(err).__name__)
            fallback = self._get_fallback_projects(published_only=True)
            return [p for p in fallback if p.get("featured")][:limit]

    def find_by_slug(self, slug: str) -> Optional[Dict[str, Any]]:
        """Retrieve a single project by its unique slug."""
        slug = (slug or "").strip().lower()
        col = self.get_collection()
        if col is None:
            for p in self._get_fallback_projects(published_only=False):
                if p.get("slug") == slug:
                    return p
            return None

        try:
            return col.find_one({"slug": slug})
        except PyMongoError as err:
            logger.warning("find_by_slug failed: %s. Using static fallback.", type(err).__name__)
            for p in self._get_fallback_projects(published_only=False):
                if p.get("slug") == slug:
                    return p
            return None

    def insert(self, doc: Dict[str, Any]) -> bool:
        """Insert a new project document."""
        col = self.get_collection()
        if col is None:
            raise RuntimeError("Database unavailable. Cannot insert project.")

        try:
            now = datetime.now(timezone.utc).isoformat()
            doc["created_at"] = doc.get("created_at") or now
            doc["updated_at"] = now
            col.insert_one(doc)
            return True
        except PyMongoError as err:
            logger.error("Insert project failed: %s", type(err).__name__)
            raise

    def update(self, slug: str, doc: Dict[str, Any]) -> bool:
        """Update an existing project identified by slug."""
        col = self.get_collection()
        if col is None:
            raise RuntimeError("Database unavailable. Cannot update project.")

        try:
            doc["updated_at"] = datetime.now(timezone.utc).isoformat()
            res = col.update_one({"slug": slug}, {"$set": doc})
            return res.matched_count > 0
        except PyMongoError as err:
            logger.error("Update project failed: %s", type(err).__name__)
            raise

    def delete(self, slug: str) -> bool:
        """Delete a project identified by slug."""
        col = self.get_collection()
        if col is None:
            raise RuntimeError("Database unavailable. Cannot delete project.")

        try:
            res = col.delete_one({"slug": slug})
            return res.deleted_count > 0
        except PyMongoError as err:
            logger.error("Delete project failed: %s", type(err).__name__)
            raise

    def set_published(self, slug: str, published: bool) -> bool:
        """Toggle publish status of a project."""
        return self.update(slug, {"published": published})

    def count(self) -> int:
        """Return total number of projects in the collection."""
        col = self.get_collection()
        if col is None:
            return len(self._get_fallback_projects(published_only=False))
        try:
            return col.count_documents({})
        except PyMongoError:
            return len(self._get_fallback_projects(published_only=False))

    def _get_fallback_projects(self, published_only: bool = True) -> List[Dict[str, Any]]:
        """
        Safe fallback to local static data defined in data/projects.py.
        Ensures the portfolio never fails even if MongoDB is completely offline.
        """
        try:
            from data.projects import PROJECTS
            res = []
            for idx, p in enumerate(PROJECTS):
                slug = p.get("id") or p.get("slug") or f"project-{idx+1}"
                item = {
                    "title": p.get("title", ""),
                    "slug": slug,
                    "subtitle": p.get("subtitle", ""),
                    "short_description": p.get("tagline") or p.get("problem_statement") or "",
                    "description": p.get("overview") or "",
                    "status": "completed",
                    "featured": bool(p.get("featured", False)),
                    "featured_order": idx + 1,
                    "category": p.get("category", "systems"),
                    "badge": p.get("badge", ""),
                    "image": p.get("image", "images/poster1.png"),
                    "github_url": p.get("github_url", ""),
                    "live_url": p.get("demo_url", ""),
                    "demo_label": p.get("demo_label", "Launch Live App"),
                    "technologies": [t.get("name") if isinstance(t, dict) else t for t in p.get("tech_stack", [])],
                    "features": p.get("engineering_highlights", []),
                    "challenges": [],
                    "future_improvements": [],
                    "published": True,
                    "created_at": datetime.now(timezone.utc).isoformat(),
                    "updated_at": datetime.now(timezone.utc).isoformat(),
                }
                res.append(item)
            return res
        except Exception as e:
            logger.error("Failed to load static fallback projects: %s", e)
            return []

    def find_all_certificates(self) -> List[Dict[str, Any]]:
        """Retrieve all certificates from MongoDB, or fallback to static list."""
        client = self._get_client()
        if client is None:
            return self._get_fallback_certificates()
        try:
            col = client[self.db_name]["certificates"]
            certs = list(col.find({}).sort("order", pymongo.ASCENDING))
            if not certs:
                return self._get_fallback_certificates()
            return certs
        except PyMongoError as err:
            logger.warning("find_all_certificates failed: %s. Using static fallback.", type(err).__name__)
            return self._get_fallback_certificates()

    def _get_fallback_certificates(self) -> List[Dict[str, Any]]:
        """Safe fallback to local static certifications defined in data/projects.py."""
        try:
            from data.projects import CERTIFICATIONS
            return CERTIFICATIONS
        except Exception as e:
            logger.error("Failed to load static fallback certificates: %s", e)
            return []

