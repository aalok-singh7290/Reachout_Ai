"""
email_server.py — Real Gmail SMTP email sender API
Run with: python email_server.py
Listens on: http://localhost:5000
"""

import os
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow React frontend to call this API

# ─── Gmail credentials ────────────────────────────────────────────────────────
# Set these in your .env file:
#   GMAIL_ADDRESS=youremail@gmail.com
#   GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx   ← 16-char App Password (NOT your Gmail password)
#
# How to get an App Password:
#   1. Go to https://myaccount.google.com/security
#   2. Enable 2-Step Verification
#   3. Search "App passwords" → generate one for "Mail"
#   4. Copy the 16-character password into your .env
# ─────────────────────────────────────────────────────────────────────────────

GMAIL_ADDRESS     = os.getenv("GMAIL_ADDRESS", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")


def send_gmail(to_email: str, subject: str, body: str, from_name: str = "ReachOut AI") -> dict:
    """Send a real email via Gmail SMTP using an App Password."""

    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        return {
            "success": False,
            "error": "Gmail credentials not configured. Set GMAIL_ADDRESS and GMAIL_APP_PASSWORD in your .env file."
        }

    try:
        # Build the email
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"]    = f"{from_name} <{GMAIL_ADDRESS}>"
        msg["To"]      = to_email

        # Plain-text body
        part = MIMEText(body, "plain")
        msg.attach(part)

        # Send via Gmail SMTP (port 465, SSL)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, to_email, msg.as_string())

        print(f"✅ Email sent to {to_email} | Subject: {subject}")
        return {"success": True, "to": to_email}

    except smtplib.SMTPAuthenticationError:
        return {
            "success": False,
            "error": "Gmail authentication failed. Make sure you're using an App Password, not your regular Gmail password."
        }
    except smtplib.SMTPRecipientsRefused:
        return {
            "success": False,
            "error": f"Recipient email address refused: {to_email}"
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/health", methods=["GET"])
def health():
    """Health check — lets the frontend know the server is running."""
    configured = bool(GMAIL_ADDRESS and GMAIL_APP_PASSWORD)
    return jsonify({
        "status": "ok",
        "gmail_configured": configured,
        "sender": GMAIL_ADDRESS if configured else "not set"
    })


@app.route("/send-email", methods=["POST"])
def send_email():
    """
    POST /send-email
    Body (JSON):
    {
        "to":      "hr@company.com",
        "subject": "Senior Engineer – Alex Kumar",
        "body":    "Hi Sarah, ...",
        "from_name": "Alex Kumar"   (optional)
    }
    """
    data = request.get_json()

    if not data:
        return jsonify({"success": False, "error": "No JSON body received"}), 400

    to_email  = data.get("to", "").strip()
    subject   = data.get("subject", "").strip()
    body      = data.get("body", "").strip()
    from_name = data.get("from_name", "ReachOut AI").strip()

    # Basic validation
    if not to_email:
        return jsonify({"success": False, "error": "Missing 'to' email address"}), 400
    if not subject:
        return jsonify({"success": False, "error": "Missing email subject"}), 400
    if not body:
        return jsonify({"success": False, "error": "Missing email body"}), 400

    result = send_gmail(to_email, subject, body, from_name)

    status_code = 200 if result["success"] else 500
    return jsonify(result), status_code


@app.route("/send-bulk", methods=["POST"])
def send_bulk():
    """
    POST /send-bulk
    Body (JSON):
    {
        "emails": [
            { "to": "...", "subject": "...", "body": "...", "from_name": "..." },
            ...
        ]
    }
    Returns per-email results.
    """
    data = request.get_json()
    emails = data.get("emails", [])

    if not emails:
        return jsonify({"success": False, "error": "No emails provided"}), 400

    results = []
    for email in emails:
        result = send_gmail(
            to_email  = email.get("to", ""),
            subject   = email.get("subject", ""),
            body      = email.get("body", ""),
            from_name = email.get("from_name", "ReachOut AI")
        )
        result["to"] = email.get("to", "")
        results.append(result)

    sent_count   = sum(1 for r in results if r["success"])
    failed_count = len(results) - sent_count

    return jsonify({
        "success": failed_count == 0,
        "sent": sent_count,
        "failed": failed_count,
        "results": results
    })


if __name__ == "__main__":
    print("=" * 55)
    print("  Resugo — Email API Server")
    print("=" * 55)
    print(f"  Sender : {GMAIL_ADDRESS or '⚠️  Not configured'}")
    print(f"  Port   : 5000")
    print(f"  Health : http://localhost:5000/health")
    print("=" * 55)

    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        print("\n  ⚠️  WARNING: Gmail credentials not set!")
        print("  Add to your .env file:")
        print("    GMAIL_ADDRESS=youremail@gmail.com")
        print("    GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx\n")

    app.run(host="0.0.0.0", port=5000, debug=False)
