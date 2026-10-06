import logging
import requests
from flask import current_app

logger = logging.getLogger(__name__)

GOOGLE_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"

def verify_recaptcha(response_token: str, remote_ip: str | None = None) -> tuple[bool, str]:
    """
    Server-side verification of Google reCAPTCHA v2 token.
    
    Returns:
        (is_valid, user_friendly_message)
    """
    # 1. Testing mode bypass (zero external network calls)
    if current_app.config.get("TESTING"):
        return True, "reCAPTCHA verified (testing mode)."

    secret_key = current_app.config.get("RECAPTCHA_SECRET_KEY")
    site_key = current_app.config.get("RECAPTCHA_SITE_KEY")

    # 2. Check if reCAPTCHA is configured
    if not secret_key or not site_key:
        if current_app.config.get("DEBUG") or current_app.config.get("ENV") == "development":
            logger.info("reCAPTCHA keys not configured; bypassing in development mode.")
            return True, "reCAPTCHA bypassed in development."
        logger.warning("reCAPTCHA keys missing in production environment.")
        return False, "Security verification service is unconfigured. Please contact via direct email or LinkedIn."

    # 3. Check for presence of client response token
    if not response_token:
        return False, "Please complete the 'I'm not a robot' verification checkbox."

    # 4. Verify with Google API
    payload = {
        "secret": secret_key,
        "response": response_token,
    }
    if remote_ip:
        payload["remoteip"] = remote_ip

    try:
        resp = requests.post(GOOGLE_VERIFY_URL, data=payload, timeout=5)
        resp.raise_for_status()
        data = resp.json()

        if data.get("success"):
            return True, "reCAPTCHA verified successfully."
        
        # Log safe error codes from Google without exposing secret key
        error_codes = data.get("error-codes", [])
        logger.warning("Google reCAPTCHA verification rejected. Error codes: %s", error_codes)
        
        # Provide clean, non-leaking user feedback
        if "timeout-or-duplicate" in error_codes:
            return False, "Verification timed out or already used. Please check the reCAPTCHA box again."
        
        return False, "reCAPTCHA validation failed. Please check the verification box and try again."

    except requests.RequestException as e:
        logger.error("Failed to reach Google reCAPTCHA verification service: %s", e)
        return False, "Unable to verify security challenge at this time. Please try again in a few moments."
