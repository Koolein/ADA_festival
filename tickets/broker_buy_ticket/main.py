from flask import Flask, request, jsonify
from google.cloud import pubsub_v1
import json

app = Flask(__name__)
publisher = pubsub_v1.PublisherClient()
project_id = "de2024-collin"
topic_id = "payment-events"
topic_path = publisher.topic_path(project_id, topic_id)

@app.route('/buy-ticket', methods=['POST'])
def buy_ticket():
    data = request.json
    if not all(k in data for k in ("session_id", "user_id", "ticket_type")):
        return jsonify({"error": "Missing required fields"}), 400

    publisher.publish(topic_path, json.dumps(data).encode("utf-8"))
    return jsonify({"message": "Ticket request submitted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
