import os
import re
import secrets
import time
from flask import Blueprint, request, render_template, flash, redirect, url_for, session, current_app
from services.email_service import send_contact_emails
from services.recaptcha_service import verify_recaptcha

contact_bp = Blueprint("contact", __name__)

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def get_or_create_csrf_token() -> str:
    """Generate or retrieve a session-bound CSRF token."""
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)
    return session["csrf_token"]

@contact_bp.route("/contact", methods=["GET", "POST"])
def contact():
    recaptcha_site_key = current_app.config.get("RECAPTCHA_SITE_KEY", "")
    csrf_token = get_or_create_csrf_token()

    if request.method == "POST":
        # 1. CSRF Token Validation
        submitted_csrf = request.form.get("csrf_token", "")
        if not submitted_csrf or submitted_csrf != session.get("csrf_token"):
            flash("Security validation failed (invalid CSRF token). Please refresh and try again.", "error")
            return redirect(url_for("contact.contact"))

        # 2. Honeypot check (Bot detection)
        honeypot = request.form.get("website_url_hp", "").strip()
        if honeypot:
            # Bot filled out the invisible honeypot field. Silently discard.
            return render_template(
                "contact.html",
                title="Contact — Mithilesh Chaurasiya",
                success=True,
                recaptcha_site_key=recaptcha_site_key,
                csrf_token=csrf_token,
            )

        # 3. Rate limiting / Rapid submission check
        last_submission = session.get("last_submission_time", 0)
        current_time = time.time()
        if current_time - last_submission < 8:
            flash("Please wait a few seconds before submitting another message.", "warning")
            return redirect(url_for("contact.contact"))

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        message = request.form.get("message", "").strip()

        # 4. Input Validation
        if not name or len(name) < 2 or len(name) > 100:
            flash("Please enter a valid name (between 2 and 100 characters).", "error")
            return redirect(url_for("contact.contact"))

        if not email or not EMAIL_REGEX.match(email) or len(email) > 120:
            flash("Please provide a valid email address.", "error")
            return redirect(url_for("contact.contact"))

        if not message or len(message) < 5 or len(message) > 5000:
            flash("Message must be between 5 and 5,000 characters.", "error")
            return redirect(url_for("contact.contact"))

        # 5. reCAPTCHA Verification (server-side via recaptcha_service)
        recaptcha_response = request.form.get("g-recaptcha-response", "")
        captcha_valid, captcha_msg = verify_recaptcha(recaptcha_response, request.remote_addr)
        if not captcha_valid:
            flash(captcha_msg, "error")
            return redirect(url_for("contact.contact"))

        # 6. Send Emails
        success, feedback = send_contact_emails(name, email, message)
        session["last_submission_time"] = current_time

        # Refresh CSRF token for the next submission
        session["csrf_token"] = secrets.token_hex(32)

        if success:
            return render_template(
                "contact.html",
                title="Contact — Mithilesh Chaurasiya",
                success=True,
                recaptcha_site_key=recaptcha_site_key,
                csrf_token=session["csrf_token"],
            )
        else:
            flash(feedback, "error")
            return redirect(url_for("contact.contact"))

    return render_template(
        "contact.html",
        title="Contact — Mithilesh Chaurasiya",
        success=False,
        recaptcha_site_key=recaptcha_site_key,
        csrf_token=csrf_token,
    )
