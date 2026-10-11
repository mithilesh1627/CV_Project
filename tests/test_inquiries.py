"""
Unit and integration tests for InquiryRepository, Resilient Email Dispatch, and Admin Inquiries.
"""

from unittest.mock import patch, MagicMock
import pytest
from bson import ObjectId
from repositories.inquiry_repository import InquiryRepository
from services.email_service import send_contact_emails


class MockInquiriesCollection:
    """Mock MongoDB collection for testing without an active cluster."""

    def __init__(self):
        self.docs = []

    def insert_one(self, doc):
        doc_copy = doc.copy()
        new_id = ObjectId()
        doc_copy["_id"] = new_id
        self.docs.append(doc_copy)
        res = MagicMock()
        res.inserted_id = new_id
        return res

    def find(self):
        class MockCursor:
            def __init__(self, items):
                self.items = items

            def sort(self, field, direction):
                return self

            def skip(self, n):
                return self

            def limit(self, n):
                return self

            def __iter__(self):
                return iter(self.items)

        return MockCursor(self.docs)

    def count_documents(self, query):
        count = 0
        for d in self.docs:
            if "read" in query and d.get("read") == query["read"]:
                count += 1
        return count

    def update_one(self, query, update):
        res = MagicMock()
        res.modified_count = 0
        target_id = query.get("_id")
        for d in self.docs:
            if d.get("_id") == target_id:
                if "$set" in update:
                    d.update(update["$set"])
                res.modified_count = 1
                break
        return res

    def delete_one(self, query):
        res = MagicMock()
        res.deleted_count = 0
        target_id = query.get("_id")
        for i, d in enumerate(self.docs):
            if d.get("_id") == target_id:
                del self.docs[i]
                res.deleted_count = 1
                break
        return res


def test_inquiry_repository_offline_fallback():
    """Verify InquiryRepository gracefully handles missing mongo_uri."""
    repo = InquiryRepository(mongo_uri="")
    assert repo.get_collection() is None
    success, inq_id = repo.save_inquiry("Test", "test@example.com", "Hello")
    assert success is False
    assert inq_id is None
    assert repo.get_inquiries() == []
    assert repo.get_unread_count() == 0
    assert repo.mark_as_read("507f1f77bcf86cd799439011") is False
    assert repo.delete_inquiry("507f1f77bcf86cd799439011") is False


def test_inquiry_repository_crud():
    """Verify InquiryRepository save, read, mark_as_read, and delete."""
    mock_col = MockInquiriesCollection()
    repo = InquiryRepository(mongo_uri="mongodb://localhost:27017")
    repo.get_collection = lambda: mock_col

    # 1. Save
    success, inq_id = repo.save_inquiry("Alice", "alice@example.com", "Interested in MLOps role", "127.0.0.1")
    assert success is True
    assert inq_id is not None
    assert repo.get_unread_count() == 1

    # 2. Get
    inquiries = repo.get_inquiries()
    assert len(inquiries) == 1
    assert inquiries[0]["name"] == "Alice"
    assert inquiries[0]["email"] == "alice@example.com"
    assert inquiries[0]["read"] is False

    # 3. Mark as read
    marked = repo.mark_as_read(inq_id)
    assert marked is True
    assert repo.get_unread_count() == 0

    # 4. Delete
    deleted = repo.delete_inquiry(inq_id)
    assert deleted is True
    assert len(repo.get_inquiries()) == 0


def test_resilient_email_service_fallback_to_db(app):
    """
    Test that when host blocks SMTP (raising timeout/connection error),
    send_contact_emails still returns True because the message is safely saved in MongoDB.
    """
    mock_col = MockInquiriesCollection()
    with app.app_context():
        app.config["TESTING"] = False
        app.config["MONGODB_URI"] = "mongodb+srv://mock"
        app.config["EMAIL_USER"] = "sender@example.com"
        app.config["EMAIL_PASS"] = "password"
        app.config["EMAIL_RECEIVER"] = "owner@example.com"

        with patch("services.email_service.InquiryRepository.get_collection", return_value=mock_col):
            with patch("smtplib.SMTP_SSL", side_effect=TimeoutError("Port 465 blocked by cloud host")):
                success, msg = send_contact_emails("John Doe", "john@example.com", "Great portfolio!")
                assert success is True
                assert "sent successfully" in msg
                # Verify inquiry is preserved in MongoDB
                assert len(mock_col.docs) == 1
                assert mock_col.docs[0]["name"] == "John Doe"


def test_admin_inquiries_routes_require_auth(client):
    """Test that /admin/inquiries requires admin authentication."""
    res = client.get("/admin/inquiries", follow_redirects=False)
    assert res.status_code == 302
    assert "/admin/login" in res.headers["Location"]


def test_admin_inquiries_authenticated_view(client):
    """Test authenticated admin can view inquiries list."""
    # Authenticate admin
    with client.session_transaction() as sess:
        sess["admin_logged_in"] = True

    mock_col = MockInquiriesCollection()
    mock_col.insert_one({"name": "Recruiter Bob", "email": "bob@corp.com", "message": "Job offer", "read": False})

    with patch("routes.admin_projects.InquiryRepository.get_collection", return_value=mock_col):
        res = client.get("/admin/inquiries")
        assert res.status_code == 200
        assert b"Contact Inquiries" in res.data
        assert b"Recruiter Bob" in res.data
        assert b"bob@corp.com" in res.data
