from flask import Blueprint, request, jsonify
from app.services.auth import token_required
from app.utils.exceptions import BadRequestsError
from app.config import Config
import smtplib
from email.mime.text import MIMEText

email_bp = Blueprint('email', __name__)

@email_bp.route("/send_email", methods=["POST"])
@token_required
def send_email():
    data = request.get_json()
    if not data:
        raise BadRequestsError("Invalid or missing JSON data")

    required_fields=["name", "email", "message"]
    if not all(field in data for field in required_fields):
        raise BadRequestsError("Missing required fields: name, email, message")

    """
        Send a mail from a specific email server to others mails services
        :param smtp_server: email server
        :param origin_mail: email from send mail
        :param app_password: password for app from email server
        :param destiny_mail: email to receive mail
        :param subject: objective of the mail
        :param message: body of mail
        :return:
        """
    origin_mail = Config.ORIGIN_MAIL
    destiny_mail = Config.ORIGIN_MAIL
    smtp_server = Config.SMTP_SERVER
    app_password = Config.APP_GMAIL_PASSWORD
    body = f"Message from: {data['name']} <{data['email']}>\n\n{data['message']}"
    msg = MIMEText(body)
    msg["Subject"] = "New message from your portfolio"
    msg["From"] = origin_mail
    msg["To"] = destiny_mail

    # Establece la codificación
    msg.set_charset("utf-8")

    with smtplib.SMTP(smtp_server) as connection:
        # To init te security protocols
        connection.starttls()
        connection.login(user=origin_mail, password=app_password)
        connection.sendmail(from_addr=origin_mail,
                            to_addrs=destiny_mail,
                            msg=msg.as_string())

    return jsonify({"message": "message sent"}), 200
