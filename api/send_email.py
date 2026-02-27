"""
api/send_email.py — Resugo Email API (Vercel Serverless Function)

Vercel automatically serves this at:
  GET  /api/send_email  →  health check
  POST /api/send_email  →  send email with optional resume attachment

Environment variables (set in Vercel dashboard → Project → Settings → Environment Variables):
  GMAIL_ADDRESS       = youremail@gmail.com
  GMAIL_APP_PASSWORD  = xxxx xxxx xxxx xxxx
"""

import os
import json
import smtplib
import ssl
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from http.server import BaseHTTPRequestHandler

# ── Read credentials from Vercel environment variables ────────────────────────
GMAIL_ADDRESS      = os.environ.get("GMAIL_ADDRESS", "")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")


def cors_headers():
    return {
        "Access-Control-Allow-Origin":  "*",
        "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Content-Type":                 "application/json",
    }


def send_gmail(to_email, subject, body, from_name="Resugo",
               resume_base64=None, resume_filename="Resume.pdf"):
    """Core Gmail SMTP sender — same logic works locally and on Vercel."""

    if not GMAIL_ADDRESS or not GMAIL_APP_PASSWORD:
        return {
            "success": False,
            "error":   "Gmail not configured. Add GMAIL_ADDRESS and GMAIL_APP_PASSWORD in Vercel → Settings → Environment Variables."
        }

    try:
        msg = MIMEMultipart("mixed")
        msg["Subject"] = subject
        msg["From"]    = f"{from_name} <{GMAIL_ADDRESS}>"
        msg["To"]      = to_email

        # Email body
        body_part = MIMEMultipart("alternative")
        body_part.attach(MIMEText(body, "plain"))
        msg.attach(body_part)

        # Resume PDF attachment
        if resume_base64:
            try:
                pdf_bytes  = base64.b64decode(resume_base64)
                attachment = MIMEApplication(pdf_bytes, _subtype="pdf")
                attachment.add_header("Content-Disposition", "attachment",
                                      filename=resume_filename)
                msg.attach(attachment)
            except Exception as ae:
                print(f"Attachment error (email still sent): {ae}")

        # Send via Gmail SMTP SSL
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, to_email, msg.as_string())

        return {"success": True, "to": to_email, "attachment": bool(resume_base64)}

    except smtplib.SMTPAuthenticationError:
        return {"success": False,
                "error": "Gmail auth failed. Use an App Password from https://myaccount.google.com/apppasswords"}
    except smtplib.SMTPRecipientsRefused:
        return {"success": False, "error": f"Recipient refused: {to_email}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


class handler(BaseHTTPRequestHandler):
    """Vercel calls this class for every request to /api/send_email"""

    def _send(self, status, data):
        body = json.dumps(data).encode()
        self.send_response(status)
        for k, v in cors_headers().items():
            self.send_header(k, v)
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

    # ── OPTIONS preflight (browser CORS check) ────────────────────────────────
    def do_OPTIONS(self):
        self._send(204, {})

    # ── GET /api/send_email  →  health check ──────────────────────────────────
    def do_GET(self):
        configured = bool(GMAIL_ADDRESS and GMAIL_APP_PASSWORD)
        self._send(200, {
            "status":           "ok",
            "gmail_configured": configured,
            "sender":           GMAIL_ADDRESS if configured else "not set",
        })

    # ── POST /api/send_email  →  send one email ───────────────────────────────
    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", 0))
            raw    = self.rfile.read(length)
            data   = json.loads(raw) if raw else {}
        except Exception:
            self._send(400, {"success": False, "error": "Invalid JSON body"})
            return

        path = self.path.split("?")[0].rstrip("/")

        # ── POST /api/send_email  (single) ────────────────────────────────────
        if path in ("/api/send_email", "/api/send_email/"):
            to_email        = (data.get("to") or "").strip()
            subject         = (data.get("subject") or "").strip()
            body_text       = (data.get("body") or "").strip()
            from_name       = (data.get("from_name") or "Resugo").strip()
            resume_base64   =  data.get("resume_base64")
            resume_filename =  data.get("resume_filename") or "Resume.pdf"

            if not to_email:
                self._send(400, {"success": False, "error": "Missing 'to'"}); return
            if not subject:
                self._send(400, {"success": False, "error": "Missing 'subject'"}); return
            if not body_text:
                self._send(400, {"success": False, "error": "Missing 'body'"}); return

            result = send_gmail(to_email, subject, body_text, from_name,
                                resume_base64, resume_filename)
            self._send(200 if result["success"] else 500, result)

        # ── POST /api/send_email/bulk  (batch) ────────────────────────────────
        elif path in ("/api/send_email/bulk",):
            emails          = data.get("emails", [])
            resume_base64   = data.get("resume_base64")
            resume_filename = data.get("resume_filename") or "Resume.pdf"

            if not emails:
                self._send(400, {"success": False, "error": "No emails provided"}); return

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
            self._send(200, {"success": failed == 0, "sent": sent,
                             "failed": failed, "results": results})
        else:
            self._send(404, {"error": "Not found"})

    def log_message(self, format, *args):
        print(f"[Resugo API] {format % args}")
