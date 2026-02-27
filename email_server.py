"""
email_server.py — Resugo Gmail SMTP sender API
Run with: python email_server.py
Listens on: http://localhost:5001  (5000 is blocked on Mac by AirPlay)
"""

import os
import smtplib
import ssl
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ── CORS: allow all origins so the React dev server can call this ─────────────
CORS(app, resources={r"/*": {
    "origins": "*",
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

GMAIL_ADDRESS      = os.getenv("GMAIL_ADDRESS", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")

# ─────────────────────────────────────────────────────────────────────────────

def send_gmail(
    to_email: str,
    subject: str,
    body: str,
    from_name: str = "Resugo",
    resume_base64: str = None,
    resume_filename: str = "Resume.pdf"
) -> dict:
    """Send a real email via Gmail SMTP, optionally attaching a resume PDF."""

    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        return {
            "success": False,
            "error": "Gmail credentials not configured. Add GMAIL_ADDRESS and GMAIL_APP_PASSWORD to your .env file."
        }

    try:
        msg = MIMEMultipart("mixed")
        msg["Subject"] = subject
        msg["From"]    = f"{from_name} <{GMAIL_ADDRESS}>"
        msg["To"]      = to_email

        body_part = MIMEMultipart("alternative")
        body_part.attach(MIMEText(body, "plain"))
        msg.attach(body_part)

        if resume_base64:
            try:
                pdf_bytes  = base64.b64decode(resume_base64)
                attachment = MIMEApplication(pdf_bytes, _subtype="pdf")
                attachment.add_header("Content-Disposition", "attachment", filename=resume_filename)
                msg.attach(attachment)
                print(f"   📎 Attached: {resume_filename} ({len(pdf_bytes):,} bytes)")
            except Exception as ae:
                print(f"   ⚠️  Attachment failed (email still sent): {ae}")

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, to_email, msg.as_string())

        print(f"   ✅ Sent → {to_email}")
        return {"success": True, "to": to_email, "attachment": bool(resume_base64)}

    except smtplib.SMTPAuthenticationError:
        return {"success": False, "error": "Gmail auth failed — use an App Password, not your Gmail password. See: https://myaccount.google.com/apppasswords"}
    except smtplib.SMTPRecipientsRefused:
        return {"success": False, "error": f"Recipient address refused: {to_email}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ── Handle preflight OPTIONS requests explicitly ───────────────────────────────
@app.before_request
def handle_preflight():
    if request.method == "OPTIONS":
        from flask import Response
        res = Response()
        res.headers["Access-Control-Allow-Origin"]  = "*"
        res.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        res.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        return res, 204


@app.route("/health", methods=["GET"])
def health():
    configured = bool(GMAIL_ADDRESS and GMAIL_APP_PASSWORD)
    return jsonify({
        "status":           "ok",
        "gmail_configured": configured,
        "sender":           GMAIL_ADDRESS if configured else "not set"
    })


@app.route("/send-email", methods=["POST", "OPTIONS"])
def send_email():
    data = request.get_json(silent=True) or {}

    to_email        = (data.get("to") or "").strip()
    subject         = (data.get("subject") or "").strip()
    body            = (data.get("body") or "").strip()
    from_name       = (data.get("from_name") or "Resugo").strip()
    resume_base64   = data.get("resume_base64")
    resume_filename = data.get("resume_filename") or "Resume.pdf"

    if not to_email: return jsonify({"success": False, "error": "Missing 'to'"}), 400
    if not subject:  return jsonify({"success": False, "error": "Missing 'subject'"}), 400
    if not body:     return jsonify({"success": False, "error": "Missing 'body'"}), 400

    result = send_gmail(to_email, subject, body, from_name, resume_base64, resume_filename)
    return jsonify(result), (200 if result["success"] else 500)


@app.route("/send-bulk", methods=["POST", "OPTIONS"])
def send_bulk():
    data            = request.get_json(silent=True) or {}
    emails          = data.get("emails", [])
    resume_base64   = data.get("resume_base64")
    resume_filename = data.get("resume_filename") or "Resume.pdf"

    if not emails:
        return jsonify({"success": False, "error": "No emails provided"}), 400

    results = []
    for em in emails:
        r = send_gmail(
            to_email        = em.get("to", ""),
            subject         = em.get("subject", ""),
            body            = em.get("body", ""),
            from_name       = em.get("from_name", "Resugo"),
            resume_base64   = resume_base64,
            resume_filename = resume_filename,
        )
        r["to"] = em.get("to", "")
        results.append(r)

    sent   = sum(1 for r in results if r["success"])
    failed = len(results) - sent
    return jsonify({"success": failed == 0, "sent": sent, "failed": failed, "results": results})


if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 5001))   # 5001 avoids Mac AirPlay conflict on 5000
    print()
    print("  ╔══════════════════════════════════════╗")
    print("  ║       Resugo  —  Email Server        ║")
    print("  ╚══════════════════════════════════════╝")
    print(f"  Sender  : {GMAIL_ADDRESS or '⚠️  not set'}")
    print(f"  Running : http://localhost:{PORT}")
    print(f"  Health  : http://localhost:{PORT}/health")
    print()

    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        print("  ⚠️  Gmail not configured! Add to .env:")
        print("      GMAIL_ADDRESS=you@gmail.com")
        print("      GMAIL_APP_PASSWORD=xxxx xxxx xxxx xxxx")
        print("      (get one at https://myaccount.google.com/apppasswords)")
        print()

    app.run(host="0.0.0.0", port=PORT, debug=False)
