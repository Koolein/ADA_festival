from flask import jsonify, Request
from google.cloud import pubsub_v1
import json

publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path("de2024-collin", "deletion-events")

def cancel_ticket(request: Request):
    try:
        data = request.get_json()
        ticket_id = data['ticket_id']

        message = json.dumps({"ticket_id": ticket_id}).encode("utf-8")
        future = publisher.publish(topic_path, message)
        message_id = future.result()

        return jsonify({"status": "cancellation requested", "message_id": message_id}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
