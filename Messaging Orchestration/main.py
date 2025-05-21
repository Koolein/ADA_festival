import functions_framework
import logging
from flask import jsonify, Request
from google.cloud import firestore, bigquery
from google.cloud.firestore_v1.base_query import FieldFilter
from google.auth.transport.requests import Request as GoogleAuthRequest
from google.auth import default
import requests

# Global clients
db = firestore.Client()
bq_client = bigquery.Client()

# Config
route_url = "https://us-central1-de2024-collin.cloudfunctions.net/route_requests"


def get_session_ids_for_festival(festival_id: int) -> set:
    query = """
        SELECT id
        FROM `de2024-collin.festivaldb.sessions`
        WHERE festival_id = @festival_id
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("festival_id", "INT64", festival_id)
        ]
    )

    try:
        query_job = bq_client.query(query, job_config=job_config)
        return {row.id for row in query_job}
    except Exception as e:
        logging.error(f"BigQuery error: {e}")
        raise


def get_user_ids_for_session(session_id: int) -> set:
    try:
        tickets_ref = db.collection("tickets")
        query = tickets_ref.where(filter=FieldFilter("session_id", "==", session_id))
        return {doc.to_dict().get("user_id") for doc in query.stream() if doc.to_dict().get("user_id")}
    except Exception as e:
        logging.error(f"Firestore error for session {session_id}: {e}")
        raise


def get_all_user_ids(session_ids: set) -> set:
    user_ids = set()
    for session_id in session_ids:
        user_ids.update(get_user_ids_for_session(session_id))
    return user_ids


def build_messages(user_ids: set) -> list:
    messages = []

    for user_id in user_ids:
        try:
            user_ref = db.collection("users").document(str(user_id))
            user_doc = user_ref.get()

            if not user_doc.exists:
                continue

            user_data = user_doc.to_dict()

            if user_data.get("email"):
                messages.append({
                    "type": "email",
                    "recipient": user_data["email"]
                })

            if user_data.get("prefers_sms") and user_data.get("phone"):
                messages.append({
                    "type": "sms",
                    "recipient": user_data["phone"]
                })

        except Exception as e:
            logging.warning(f"Error fetching preferences for user {user_id}: {e}")
            continue

    return messages


def send_messages_to_route(messages: list, user_ids: set):
    try:
        credentials, _ = default()
        credentials.refresh(GoogleAuthRequest())
        token = credentials.token

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        payload = {
            "users": list(user_ids),
            "messages": messages
        }

        response = requests.post(route_url, headers=headers, json=payload)
        response.raise_for_status()
        logging.info("Successfully sent messages to route endpoint.")

    except Exception as e:
        logging.error(f"Failed to send messages: {e}")


@functions_framework.http
def festival_change(request: Request):
    request_json = request.get_json(silent=True)

    if not request_json:
        return jsonify({"error": "Missing request body"}), 400

    try:
        if "festival_id" in request_json:
            festival_id = int(request_json["festival_id"])
            session_ids = get_session_ids_for_festival(festival_id)
        elif "session_id" in request_json:
            session_ids = {int(request_json["session_id"])}
        else:
            return jsonify({"error": "Missing festival_id or session_id"}), 400

        if not session_ids:
            return jsonify({"users": [], "messages": []}), 200

        user_ids = get_all_user_ids(session_ids)
        messages = build_messages(user_ids)
        send_messages_to_route(messages, user_ids)

        return jsonify({"users": list(user_ids), "messages": messages}), 200

    except Exception as e:
        logging.error(f"Internal error: {e}")
        return jsonify({"error": "Internal server error"}), 500
