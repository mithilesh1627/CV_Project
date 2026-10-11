import os
from dotenv import load_dotenv
from werkzeug.security import generate_password_hash

# Load environment variables from .env file if present
load_dotenv()

class Config:
    """Base application configuration."""
    SECRET_KEY = os.getenv("SECRET_KEY", "mithilesh-portfolio-dev-secret-key-2026-audit")

    # reCAPTCHA configuration
    RECAPTCHA_SITE_KEY = os.getenv("RECAPTCHA_SITE_KEY", "")
    RECAPTCHA_SECRET_KEY = os.getenv("RECAPTCHA_SECRET_KEY", "")

    # Email configuration
    EMAIL_USER = os.getenv("EMAIL_USER", "")
    EMAIL_PASS = os.getenv("EMAIL_PASS", "")
    EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER", "")
    SMTP_SERVER = "smtp.gmail.com"
    SMTP_PORT = 465

    # MongoDB Project CMS configuration
    MONGODB_URI = os.getenv("MONGODB_URI", "")
    MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "portfolio")

    # Admin CMS Authentication
    ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin").strip().strip("'\"")
    _raw_admin_hash = os.getenv("ADMIN_PASSWORD_HASH", "").strip().strip("'\"")
    _raw_admin_pass = os.getenv("ADMIN_PASSWORD", "").strip().strip("'\"")

    if _raw_admin_hash:
        if "$" in _raw_admin_hash:
            ADMIN_PASSWORD_HASH = _raw_admin_hash
        else:
            ADMIN_PASSWORD_HASH = generate_password_hash(_raw_admin_hash)
    elif _raw_admin_pass:
        ADMIN_PASSWORD_HASH = generate_password_hash(_raw_admin_pass)
    else:
        ADMIN_PASSWORD_HASH = generate_password_hash("admin123")

    # Security settings
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max payload

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    """Testing configuration."""
    DEBUG = False
    TESTING = True
    WTF_CSRF_ENABLED = False
    SECRET_KEY = "test-secret-key"
    MONGODB_URI = ""
    MONGODB_DATABASE = "portfolio_testing"
    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD_HASH = generate_password_hash("testadmin123")

config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
