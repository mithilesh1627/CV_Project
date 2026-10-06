from unittest.mock import patch
import pytest
from app import create_app
from services.recaptcha_service import verify_recaptcha

@pytest.fixture
def app():
    app = create_app("testing")
    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_home_page(client):
    """Test the home page loads with 200 OK and expected title."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Mithilesh Chaurasiya" in response.data
    assert b"AI Engineer" in response.data

def test_academic_technical_page(client):
    """Test the academic & technical page loads with verified Infosys and NIT Agartala details."""
    response = client.get("/academic_technical")
    assert response.status_code == 200
    assert b"Infosys Ltd." in response.data
    assert b"National Institute of Technology, Agartala" in response.data
    assert b"Technical Skills" in response.data

def test_projects_certifications_page(client):
    """Test the projects & certifications page renders all verified projects and certificates."""
    response = client.get("/projects_certifications")
    assert response.status_code == 200
    assert b"Smart Traffic Management System" in response.data
    assert b"AgenticOps (AgentIQ)" in response.data
    assert b"DesignKaro" in response.data
    assert b"Accenture" in response.data

def test_contact_page_get(client):
    """Test GET /contact renders form successfully."""
    response = client.get("/contact")
    assert response.status_code == 200
    assert b"contact-form" in response.data

def test_robots_txt(client):
    """Test robots.txt returns 200 and valid text/plain content."""
    response = client.get("/robots.txt")
    assert response.status_code == 200
    assert response.content_type.startswith("text/plain")
    assert b"User-agent: *" in response.data
    assert b"Sitemap:" in response.data

def test_sitemap_xml(client):
    """Test sitemap.xml returns 200 and XML content."""
    response = client.get("/sitemap.xml")
    assert response.status_code == 200
    assert response.content_type.startswith("application/xml")
    assert b"<urlset" in response.data
    assert b"https://mithileshchaurasiya.me/" in response.data

def test_404_error_page(client):
    """Test requesting a non-existent route returns 404 with custom error page."""
    response = client.get("/this-route-does-not-exist-xyz")
    assert response.status_code == 404
    assert b"Page Not Found" in response.data

def test_security_headers(client):
    """Test HTTP response security headers are set."""
    response = client.get("/")
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "SAMEORIGIN"
    assert "strict-origin-when-cross-origin" in response.headers.get("Referrer-Policy", "")

def test_canonical_www_redirect(client):
    """Test that www.mithileshchaurasiya.me is permanently 301 redirected to apex domain."""
    response = client.get("/", headers={"Host": "www.mithileshchaurasiya.me"})
    assert response.status_code == 301
    assert "mithileshchaurasiya.me" in response.headers.get("Location", "")
    assert not response.headers.get("Location", "").startswith("http://www.")

def test_contact_form_csrf_rejection(client):
    """Test POST /contact without CSRF token is rejected with redirect."""
    response = client.post(
        "/contact",
        data={"name": "Alice", "email": "alice@example.com", "message": "Hello there"},
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b"Security validation failed" in response.data

def test_contact_form_honeypot_rejection(client):
    """Test bot filling honeypot field is intercepted without error or email dispatch."""
    client.get("/contact")
    with client.session_transaction() as sess:
        csrf_token = sess["csrf_token"]

    response = client.post(
        "/contact",
        data={
            "csrf_token": csrf_token,
            "website_url_hp": "http://spambot.com",
            "name": "Spambot",
            "email": "spam@example.com",
            "message": "Buy cheap stuff"
        }
    )
    assert response.status_code == 200
    assert (b"Thank you" in response.data or b"Message sent" in response.data or b"Message Received" in response.data)

def test_contact_form_valid_submission(client):
    """Test valid contact form submission with CSRF token in testing mode."""
    client.get("/contact")
    with client.session_transaction() as sess:
        csrf_token = sess["csrf_token"]

    response = client.post(
        "/contact",
        data={
            "csrf_token": csrf_token,
            "name": "Jane Recruiter",
            "email": "jane@techcorp.com",
            "message": "We reviewed your computer vision and MLOps work and would like to schedule an interview."
        }
    )
    assert response.status_code == 200
    assert (b"Thank you" in response.data or b"Message sent" in response.data or b"Message Received" in response.data)

def test_recaptcha_service_unit_testing_bypass(app):
    """Verify that in testing mode, recaptcha_service bypasses network calls immediately."""
    with app.app_context():
        valid, msg = verify_recaptcha("mock-token")
        assert valid is True
        assert "testing mode" in msg

def test_recaptcha_service_mocked_google_api(app):
    """Verify recaptcha_service properly handles Google API response when not in test mode."""
    with app.app_context():
        # Temporarily toggle off TESTING in context
        app.config["TESTING"] = False
        app.config["RECAPTCHA_SECRET_KEY"] = "mock-secret"
        app.config["RECAPTCHA_SITE_KEY"] = "mock-site"

        # 1. Missing token returns False without network call
        valid, msg = verify_recaptcha("")
        assert valid is False
        assert "Please complete" in msg

        # 2. Mock successful Google response
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {"success": True}

            valid, msg = verify_recaptcha("valid-user-token")
            assert valid is True
            assert mock_post.called

        # 3. Mock failed Google response
        with patch("requests.post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                "success": False,
                "error-codes": ["invalid-input-response"]
            }

            valid, msg = verify_recaptcha("invalid-token")
            assert valid is False
            assert "validation failed" in msg

def test_static_resume_download(client):
    """Test static resume PDF exists and is downloadable."""
    response = client.get("/static/CV_Mithilesh.pdf")
    assert response.status_code == 200
    assert response.content_type == "application/pdf"
