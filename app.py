import os
from datetime import datetime, timezone
from flask import Flask, render_template, request, redirect
from config import config_by_name
from routes.main import main_bp
from routes.contact import contact_bp
from routes.admin_projects import admin_bp

def create_app(config_name: str | None = None) -> Flask:
    """Application factory for the portfolio Flask application."""
    if not config_name:
        env_mode = os.getenv("FLASK_ENV", "production" if os.getenv("RENDER") else "development")
        config_name = env_mode.lower()

    app = Flask(__name__)
    config_class = config_by_name.get(config_name, config_by_name["production"])
    app.config.from_object(config_class)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(contact_bp)
    app.register_blueprint(admin_bp)

    # Canonical hostname redirect (www -> apex domain)
    @app.before_request
    def redirect_www():
        if request.host.startswith("www.mithileshchaurasiya.me"):
            url = request.url.replace("www.mithileshchaurasiya.me", "mithileshchaurasiya.me", 1)
            return redirect(url, code=301)

    # Global template context
    @app.context_processor
    def inject_global_template_data():
        return {
            "current_year": datetime.now(timezone.utc).year,
            "canonical_base_url": "https://mithileshchaurasiya.me",
            "recaptcha_site_key": app.config.get("RECAPTCHA_SITE_KEY", ""),
        }

    # Security headers
    @app.after_request
    def set_security_headers(response):
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
        return response

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("404.html", title="Page Not Found — Mithilesh Chaurasiya"), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template("404.html", title="Server Error — Mithilesh Chaurasiya"), 500

    return app

# WSGI application instance for Gunicorn / Render
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
