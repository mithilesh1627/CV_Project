"""
Comprehensive unit and integration test suite for the MongoDB-backed Project CMS.
Tests all 16 required CMS scenarios using deterministic mocks and in-memory repository tests.
Zero external network calls required.
"""

from unittest.mock import MagicMock, patch
import pytest
from app import create_app
from models.project import Project, slugify
from repositories.project_repository import ProjectRepository
from services.project_service import ProjectService


@pytest.fixture
def app():
    """Create test application configured for testing."""
    test_app = create_app("testing")
    return test_app


@pytest.fixture
def client(app):
    """Test client."""
    return app.test_client()


@pytest.fixture
def mock_repo():
    """In-memory mock ProjectRepository for deterministic unit tests."""
    repo = ProjectRepository(mongo_uri="", db_name="test_db")
    # In-memory store
    store = {}

    def mock_find_all(published_only=True):
        items = list(store.values())
        if published_only:
            items = [p for p in items if p.get("published", True)]
        items.sort(key=lambda x: (x.get("featured_order", 0), x.get("created_at", "")))
        return items

    def mock_find_featured(limit=6):
        items = [p for p in store.values() if p.get("published", True) and p.get("featured", False)]
        items.sort(key=lambda x: x.get("featured_order", 0))
        return items[:limit]

    def mock_find_by_slug(slug):
        return store.get(slug)

    def mock_insert(doc):
        slug = doc["slug"]
        if slug in store:
            raise RuntimeError(f"Duplicate key error for slug: {slug}")
        store[slug] = doc
        return True

    def mock_update(slug, doc):
        if slug not in store:
            return False
        store[slug].update(doc)
        return True

    def mock_delete(slug):
        if slug in store:
            del store[slug]
            return True
        return False

    def mock_set_published(slug, status):
        if slug in store:
            store[slug]["published"] = status
            return True
        return False

    def mock_count():
        return len(store)

    repo.find_all = MagicMock(side_effect=mock_find_all)
    repo.find_featured = MagicMock(side_effect=mock_find_featured)
    repo.find_by_slug = MagicMock(side_effect=mock_find_by_slug)
    repo.insert = MagicMock(side_effect=mock_insert)
    repo.update = MagicMock(side_effect=mock_update)
    repo.delete = MagicMock(side_effect=mock_delete)
    repo.set_published = MagicMock(side_effect=mock_set_published)
    repo.count = MagicMock(side_effect=mock_count)
    repo.is_connected = MagicMock(return_value=True)

    return repo


@pytest.fixture
def service(mock_repo):
    """ProjectService wired with in-memory mock repository."""
    return ProjectService(repository=mock_repo)


# =============================================================================
# 1. Homepage & Projects Public Rendering Tests
# =============================================================================

def test_homepage_loads_and_retrieves_projects(client):
    """1 & 2: Homepage loads successfully and retrieves projects dynamically."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Mithilesh Chaurasiya" in response.data
    assert b"AI Engineer" in response.data


def test_projects_render_dynamically_with_modal_ids(client):
    """3 & 4: Projects render dynamically and modal IDs match slugs (e.g. modal-designkaro)."""
    response = client.get("/projects_certifications")
    assert response.status_code == 200
    assert b"Projects &amp; Certifications" in response.data
    # Check that stable modal ID based on slug is generated
    assert b'id="modal-designkaro"' in response.data or b'id="modal-smart-traffic"' in response.data
    assert b'openModal(\'modal-' in response.data


def test_missing_optional_fields_do_not_break_rendering(client, service):
    """5: Missing optional fields (no challenges, no demo, etc.) do not break rendering."""
    minimal_data = {
        "title": "Minimalist System",
        "slug": "minimalist-system",
        "description": "A project with almost no optional metadata.",
    }
    project = service.create_project(minimal_data)
    assert project.slug == "minimalist-system"
    assert project.tech_items == []
    assert project.challenges == []
    assert project.future_improvements == []

    # Verify Project model handles None/missing safely
    doc = project.to_doc()
    assert doc["github_url"] == ""
    assert doc["live_url"] == ""


# =============================================================================
# 2. Project Service & Repository CRUD Logic Tests
# =============================================================================

def test_project_lookup_by_slug(service):
    """6: Project lookup by slug works correctly."""
    service.create_project({
        "title": "Kafka Log Aggregator",
        "slug": "kafka-logs",
        "description": "High throughput distributed log pipeline."
    })
    found = service.get_project("kafka-logs")
    assert found is not None
    assert found.title == "Kafka Log Aggregator"
    assert found.modal_id == "modal-kafka-logs"

    # Non-existent slug returns None
    assert service.get_project("non-existent-slug") is None


def test_duplicate_slug_handling(service):
    """7: Duplicate slug is rejected."""
    p1 = service.create_project({"title": "RoleIQ Crawler", "slug": "role-iq"})
    assert p1.slug == "role-iq"

    # Duplicate slug is rejected
    with pytest.raises(ValueError) as exc:
        service.create_project({"title": "RoleIQ Crawler 2", "slug": "role-iq"})
    assert "already in use" in str(exc.value)


def test_project_creation_and_tech_mapping(service):
    """8: Project creation works and tech icons map safely to Devicon CSS classes without raw HTML."""
    created = service.create_project({
        "title": "Clinical Vision Classifier",
        "slug": "clinical-vision",
        "subtitle": "Medical Diagnostic System",
        "technologies": ["Python", "PyTorch", "OpenCV", "MongoDB", "CustomTool"],
        "features": ["Feature 1", "Feature 2"],
        "published": True
    })
    assert created.title == "Clinical Vision Classifier"
    assert len(created.tech_items) == 5
    # Python maps to devicon-python-plain
    assert any(t["name"] == "Python" and t["icon"] == "devicon-python-plain" for t in created.tech_items)
    # PyTorch maps to devicon-pytorch-original
    assert any(t["name"] == "PyTorch" and t["icon"] == "devicon-pytorch-original" for t in created.tech_items)
    # Unknown tech safely falls back to fas fa-code
    assert any(t["name"] == "CustomTool" and t["icon"] == "fas fa-code" for t in created.tech_items)


def test_project_update(service):
    """9: Project update works."""
    service.create_project({"title": "Original Title", "slug": "orig-proj", "description": "Old description"})
    updated = service.update_project("orig-proj", {"title": "Updated Title", "description": "New description"})
    assert updated.title == "Updated Title"
    assert updated.description == "New description"


def test_project_deletion(service):
    """10: Project deletion works."""
    service.create_project({"title": "Temporary Project", "slug": "temp-proj"})
    assert service.get_project("temp-proj") is not None
    deleted = service.delete_project("temp-proj")
    assert deleted is True
    assert service.get_project("temp-proj") is None


def test_publish_unpublish(service):
    """11: Publish/unpublish toggling works."""
    service.create_project({"title": "Draft Project", "slug": "draft-proj", "published": True})
    assert service.get_project("draft-proj").published is True

    service.toggle_publish("draft-proj")
    assert service.get_project("draft-proj").published is False

    # Draft should not be returned in published_only queries
    published_list = service.get_projects(published_only=True)
    assert not any(p.slug == "draft-proj" for p in published_list)


def test_featured_project_ordering(service):
    """12: Featured project ordering works according to featured_order."""
    service.create_project({"title": "Project C", "slug": "proj-c", "featured": True, "featured_order": 30})
    service.create_project({"title": "Project A", "slug": "proj-a", "featured": True, "featured_order": 10})
    service.create_project({"title": "Project B", "slug": "proj-b", "featured": True, "featured_order": 20})

    featured = service.get_featured_projects(limit=5)
    slugs = [p.slug for p in featured]
    assert slugs == ["proj-a", "proj-b", "proj-c"]


def test_invalid_project_input_is_rejected(service):
    """15: Invalid project input (missing title, invalid URLs) is rejected with clear validation errors."""
    with pytest.raises(ValueError) as exc:
        service.create_project({"title": "", "github_url": "not-a-valid-url"})
    assert "title is required" in str(exc.value).lower()
    assert "github url is invalid" in str(exc.value).lower()


# =============================================================================
# 3. Admin Authentication & Route Protection Tests
# =============================================================================

def test_admin_routes_require_authentication(client):
    """13: Admin routes reject unauthenticated access and redirect to login."""
    res = client.get("/admin/projects", follow_redirects=False)
    assert res.status_code == 302
    assert "/admin/login" in res.headers["Location"]

    res_new = client.get("/admin/projects/new", follow_redirects=False)
    assert res_new.status_code == 302
    assert "/admin/login" in res_new.headers["Location"]


def test_admin_login_and_logout(client):
    """Verify administrator sign in and sign out."""
    # GET login page
    res_get = client.get("/admin/login")
    assert res_get.status_code == 200
    assert b"Admin Sign In" in res_get.data

    with client.session_transaction() as sess:
        csrf_token = sess["csrf_token"]

    # Valid login credentials
    res_post = client.post("/admin/login", data={
        "csrf_token": csrf_token,
        "username": "admin",
        "password": "testadmin123"
    }, follow_redirects=True)
    assert res_post.status_code == 200
    assert b"Portfolio Project CMS" in res_post.data

    # Logout
    res_logout = client.get("/admin/logout", follow_redirects=True)
    assert res_logout.status_code == 200
    assert b"Signed out successfully" in res_logout.data


def test_admin_csrf_protection(client):
    """14: Admin state-changing actions reject submissions with missing or invalid CSRF token."""
    # Sign in as admin first
    with client.session_transaction() as sess:
        sess["admin_logged_in"] = True
        sess["admin_user"] = "admin"
        sess["csrf_token"] = "valid-token-123"

    # Attempt POST /admin/projects/new with missing or invalid CSRF
    res = client.post("/admin/projects/new", data={
        "csrf_token": "invalid-hacker-token",
        "title": "Hacked Project"
    }, follow_redirects=True)

    assert b"Invalid security token" in res.data


# =============================================================================
# 4. MongoDB Graceful Failure Handling Tests
# =============================================================================

def test_mongodb_failure_handled_gracefully(client):
    """16: MongoDB failure is handled gracefully without crashing or leaking stack traces."""
    with patch("pymongo.MongoClient") as mock_mongo:
        from pymongo.errors import ServerSelectionTimeoutError
        mock_mongo.side_effect = ServerSelectionTimeoutError("Simulated MongoDB cluster timeout")

        # Public routes must continue returning 200 using local fallback
        res_home = client.get("/")
        assert res_home.status_code == 200
        assert b"Mithilesh Chaurasiya" in res_home.data
        assert b"Traceback" not in res_home.data

        res_projects = client.get("/projects_certifications")
        assert res_projects.status_code == 200
        assert b"Smart Traffic Management System" in res_projects.data
        assert b"DesignKaro" in res_projects.data
        assert b"Traceback" not in res_projects.data
