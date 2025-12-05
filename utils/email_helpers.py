import smtplib
import logging
from threading import Thread
from flask import current_app
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def _send_async_email(app, to_email, subject, html_body):
    """
    Sends email using standard Python smtplib (Bypassing Flask-Mail).
    This mimics the logic of the test script that worked for you.
    """
    with app.app_context():
        try:
            # 1. Load credentials directly from the active Flask config
            smtp_server = current_app.config.get('MAIL_SERVER')
            smtp_port = current_app.config.get('MAIL_PORT')
            api_key = current_app.config.get('MAIL_USERNAME')
            secret_key = current_app.config.get('MAIL_PASSWORD')
            sender = current_app.config.get('MAIL_DEFAULT_SENDER')

            # 2. Construct the email object
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = to_email

            # Attach the HTML body
            part = MIMEText(html_body, 'html')
            msg.attach(part)

            # 3. Connect to Mailjet and Send
            # We use the exact sequence that worked in your test script
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(api_key, secret_key)
            server.sendmail(sender, to_email, msg.as_string())
            server.quit()

            logging.info(f"Email successfully sent to {to_email} via Mailjet")

        except Exception as e:
            logging.error(f"Failed to send email: {e}", exc_info=True)

def send_email(to, subject, html_body):
    """
    Main entry point. Starts the background thread.
    """
    app = current_app._get_current_object()
    
    # Start thread
    thread = Thread(target=_send_async_email, args=[app, to, subject, html_body])
    thread.start()
    
    logging.info(f"Async email task started for: {to}")