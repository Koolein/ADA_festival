import functions_framework
import logging
from flask import jsonify
from mail_function import send_mail
from sms_client import send_sms

@functions_framework.http
def route_requests(request):
    request_json = request.get_json(silent=False)

    logging.info(f"Raw data: {request.data}")
    logging.info(f"Headers: {dict(request.headers)}")

    if not request_json or "messages" not in request_json:
        return "Invalid input", 400

    messages = request_json["messages"]
    print(messages)

    email_recipients = [msg["recipient"] for msg in messages if msg["type"] == "email"]
    sms_recipients = [msg["recipient"] for msg in messages if msg["type"] == "sms"]

    logging.info(f"Email recipients: {email_recipients}")
    print(f"Email_recipients: {email_recipients}")
    logging.info(f"SMS recipients: {sms_recipients}")
    print(f"SMS recipients: {sms_recipients}")

    # Send only if non-empty
    if email_recipients:
        send_mail(email_recipients)
        logging.info(f"sent to {email_recipients}")
        print(f"sent to {email_recipients}")

    else:
        logging.info("No email recipients to send to.")
        print("No email recipients to send to.")


    if sms_recipients:
        send_sms(sms_recipients)
        logging.info(f"sent to {sms_recipients}")
        print(f"sent to {sms_recipients}")
    else:
        logging.info("No SMS recipients to send to.")
        print("No SMS recipients to send to.")

    logging.info("Notifications processed")
    print("Notifications processed")
    return jsonify({"status": "Notifications processed"}), 200