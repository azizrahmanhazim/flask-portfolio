import os
from flask import Flask, render_template, request, redirect, url_for
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Securely Load Email Credentials
EMAIL_ADDRESS = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")  # Ensure this template exists

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form["name"]
        sender_email = request.form["email"]
        message = request.form["message"]

        # Email Content
        email_content = f"Name: {name}\nEmail: {sender_email}\n\nMessage:\n{message}"

        msg = EmailMessage()
        msg.set_content(email_content)
        msg["Subject"] = f"New Contact Form Submission from {name}"
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS  # Send email to yourself

        try:
            # Connect to SMTP Server and Send Email
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)

            return redirect(url_for('contact', success="True"))  # Redirect to avoid resubmission
        except Exception as e:
            print(f"Email Error: {e}")  # Log error
            return redirect(url_for('contact', success="False"))

    success = request.args.get("success")
    return render_template("contact.html", success=success)


if __name__ == "__main__":
    app.run(debug=True)
