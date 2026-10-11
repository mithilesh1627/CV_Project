import logging
import smtplib
from email.message import EmailMessage
import requests
from flask import current_app
from repositories.inquiry_repository import InquiryRepository

logger = logging.getLogger(__name__)

def sanitize_header(value: str) -> str:
    """Remove newline characters to prevent email header injection."""
    if not value:
        return ""
    return value.replace("\r", "").replace("\n", "").strip()

def send_contact_emails(name: str, sender_email: str, message: str, ip_address: str = "") -> tuple[bool, str]:
    """
    Safely persist visitor inquiry to MongoDB Atlas and dispatch notification emails.
    Supports Resend HTTP API (port 443) to avoid cloud SMTP port restrictions,
    with graceful fallback to database persistence if SMTP is blocked.
    """
    clean_name = sanitize_header(name)
    clean_sender_email = sanitize_header(sender_email)

    # 1. Testing mode bypass (zero external network/SMTP calls)
    if current_app.config.get("TESTING"):
        logger.info("Email dispatch simulated in testing mode.")
        return True, "Email dispatch simulated in testing mode."

    # 2. Persist Inquiry into MongoDB Atlas (Guarantees zero lost messages)
    mongo_uri = current_app.config.get("MONGODB_URI", "")
    db_name = current_app.config.get("MONGODB_DATABASE", "portfolio")
    saved_to_db = False
    if mongo_uri:
        try:
            inquiry_repo = InquiryRepository(mongo_uri=mongo_uri, db_name=db_name)
            saved_to_db, _ = inquiry_repo.save_inquiry(clean_name, clean_sender_email, message, ip_address)
        except Exception as exc:
            logger.warning("Could not persist inquiry to MongoDB: %s", exc)

    # 3. Check for Resend HTTP API (Port 443 - Never blocked on cloud providers)
    resend_key = current_app.config.get("RESEND_API_KEY", "").strip()
    receiver_email = current_app.config.get("EMAIL_RECEIVER") or current_app.config.get("EMAIL_USER")

    if resend_key and receiver_email:
        try:
            resp = requests.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {resend_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "from": "Portfolio Contact <onboarding@resend.dev>",
                    "to": [receiver_email],
                    "reply_to": clean_sender_email,
                    "subject": f"Portfolio Inquiry from {clean_name}",
                    "text": f"Name: {clean_name}\nEmail: {clean_sender_email}\n\nMessage:\n{message}",
                },
                timeout=5
            )
            if resp.status_code in (200, 201):
                logger.info("Email dispatched successfully via Resend API.")
                return True, "Your message has been sent successfully!"
            else:
                logger.warning("Resend API rejected email dispatch: %s", resp.text)
        except Exception as exc:
            logger.warning("Resend API dispatch failed: %s", exc)

    # 4. Attempt SMTP (Gmail / Custom SMTP)
    smtp_server = current_app.config.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = current_app.config.get("SMTP_PORT", 465)
    smtp_user = current_app.config.get("EMAIL_USER")
    smtp_pass = current_app.config.get("EMAIL_PASS")

    email_sent = False
    if smtp_user and smtp_pass and receiver_email:
        try:
            # Fast timeout to avoid hanging requests when cloud host blocks outbound SMTP
            with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=3) as server:
                server.login(smtp_user, smtp_pass)

                # 1. Message to Site Owner
                owner_msg = EmailMessage()
                owner_msg["Subject"] = f"Portfolio Inquiry from {clean_name}"
                owner_msg["From"] = smtp_user
                owner_msg["To"] = receiver_email
                owner_msg["Reply-To"] = clean_sender_email
                owner_msg.set_content(
                    f"You received a new message from your portfolio contact form:\n\n"
                    f"Name: {clean_name}\n"
                    f"Email: {clean_sender_email}\n\n"
                    f"Message:\n{message}\n"
                )
                server.send_message(owner_msg)

                # 2. Automated Confirmation Message to Visitor
                confirm_msg = EmailMessage()
                confirm_msg["Subject"] = "Thank you for reaching out — Mithilesh Chaurasiya"
                confirm_msg["From"] = smtp_user
                confirm_msg["To"] = clean_sender_email
                confirm_msg.set_content(
                    f"Dear {clean_name},\n\n"
                    f"Thank you for contacting me through my portfolio (https://mithileshchaurasiya.me/).\n\n"
                    f"I have received your message and will review it promptly. If your inquiry is time-sensitive, "
                    f"feel free to connect with me directly on LinkedIn:\n"
                    f"https://www.linkedin.com/in/mithileshchaurasiya/\n\n"
                    f"Best regards,\n"
                    f"Mithilesh Chaurasiya\n"
                    f"AI / ML / MLOps Engineer\n"
                )
                server.send_message(confirm_msg)
                email_sent = True
                logger.info("Email dispatched successfully via SMTP.")
        except Exception as exc:
            logger.warning("SMTP email dispatch failed (likely host port restriction): %s", exc)

    # 5. Final Result Evaluation
    if email_sent or saved_to_db:
        return True, "Your message has been sent successfully!"

    return False, "Unable to record message at this time. Please reach out directly on LinkedIn or GitHub."
