import smtplib
from flask import Blueprint, request, render_template, flash, redirect, url_for
import requests
import os
from dotenv import load_dotenv

load_dotenv()

routes = Blueprint("routes", __name__)

@routes.route('/contact', methods=["GET", "POST"])
def send_email():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]
        recaptcha_response = request.form["g-recaptcha-response"]

        # Verify reCAPTCHA
        data = {
            'secret': os.getenv("RECAPTCHA_SECRET_KEY"),
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if result['success']:
            smtp_server = "smtp.gmail.com"
            sender_email = os.getenv("EMAIL_USER")
            receiver_email = os.getenv("EMAIL_RECEIVER")
            password = os.getenv("EMAIL_PASS")

            subject = f"Portfolio Contact Form - {name}"
            body = f"From: {name} <{email}>\n\n{message}"
            full_email = f"Subject: {subject}\n\n{body}"

            try:
                with smtplib.SMTP_SSL(smtp_server, 465) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, full_email)

                    # Send confirmation email to user
                    confirmation_subject = "Thank You for Contacting Mithilesh"
                    confirmation_body = (
                        f"Dear {name},\n\n"
                        "Thank you for reaching out through Mithilesh Chaurasiya's portfolio website. "
                        "Your message has been received, and he will get back to you at the earliest convenience.\n\n"
                        "Best regards,\n"
                        "BihariJarvis\n"
                        "Assistant to Mithilesh Chaurasiya"
                    )
                    confirmation_email = f"Subject: {confirmation_subject}\n\n{confirmation_body}"
                    server.sendmail(sender_email, email, confirmation_email)

                return render_template("contact.html", success=True,
                                       recaptcha_site_key=os.getenv("RECAPTCHA_SITE_KEY"))
            except Exception as e:
                flash("❌ Something went wrong while sending the email. Please try again.")
                print(e)
                return redirect(url_for("routes.send_email"))
        else:
            flash("⚠️ reCAPTCHA validation failed. Try again.")
            return redirect(url_for("routes.send_email"))

    return render_template("contact.html", success=False,
                           recaptcha_site_key=os.getenv("RECAPTCHA_SITE_KEY"))
