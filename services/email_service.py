import logging
import smtplib
from email.message import EmailMessage
from flask import current_app

logger = logging.getLogger(__name__)

def sanitize_header(value: str) -> str:
    """Remove newline characters to prevent email header injection."""
    if not value:
        return ""
    return value.replace("\r", "").replace("\n", "").strip()

def send_contact_emails(name: str, sender_email: str, message: str) -> tuple[bool, str]:
    """
    Safely send contact form submission and an automated confirmation reply.
    Uses Python standard library EmailMessage to prevent header injection.
    """
    clean_name = sanitize_header(name)
    clean_sender_email = sanitize_header(sender_email)
    
    # Testing mode bypass (zero external network/SMTP calls)
    if current_app.config.get("TESTING"):
        logger.info("Email dispatch simulated in testing mode.")
        return True, "Email dispatch simulated in testing mode."

    # Retrieve configuration from current_app
    smtp_server = current_app.config.get("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = current_app.config.get("SMTP_PORT", 465)
    smtp_user = current_app.config.get("EMAIL_USER")
    smtp_pass = current_app.config.get("EMAIL_PASS")
    receiver_email = current_app.config.get("EMAIL_RECEIVER") or smtp_user

    # If credentials are not configured, log locally and return simulated success
    if not smtp_user or not smtp_pass or not receiver_email:
        logger.warning(
            "SMTP credentials not fully configured (EMAIL_USER / EMAIL_PASS / EMAIL_RECEIVER). "
            "Logging contact submission locally:\nFrom: %s <%s>\nMessage:\n%s",
            clean_name, clean_sender_email, message
        )
        return True, "Message recorded locally (SMTP credentials pending configuration)."

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port, timeout=10) as server:
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

        return True, "Your message has been sent successfully!"
    except smtplib.SMTPAuthenticationError:
        logger.error("SMTP Authentication failed. Verify EMAIL_USER and EMAIL_PASS.")
        return False, "Email service authentication failed. Please contact via LinkedIn or GitHub."
    except Exception as exc:
        logger.error("Unexpected error sending contact email: %s", exc, exc_info=True)
        return False, "An error occurred while sending your message. Please try again or reach out on LinkedIn."
