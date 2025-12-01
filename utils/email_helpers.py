import logging
from flask_mail import Message
from app import mail  # Import the mail object from app.py
from threading import Thread
from flask import current_app

def _send_async_email(app, msg):
    """
    Helper function to send email in a background thread.
    This prevents the API from waiting for the email to be sent.
    """
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            logging.error(f"Failed to send email: {e}", exc_info=True)

def send_email(to, subject, html_body):
    """
    A helper function to send emails with pre-rendered HTML content in the background.
    
    :param to: The recipient's email address (e.g., 'buyer@example.com').
    :param subject: The email subject line.
    :param html_body: The complete HTML content of the email as a string.
    :return: None. The email is sent in a background thread.
    """
    app = current_app._get_current_object()
    msg = Message(subject, recipients=[to])
    msg.html = html_body
    
    # Send the email in a background thread so the API call returns immediately
    thread = Thread(target=_send_async_email, args=[app, msg])
    thread.start()
    
    logging.info(f"Email sending process started for subject '{subject}' to {to}")