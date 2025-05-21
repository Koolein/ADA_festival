import functions_framework
import logging
from flask import jsonify, Request as FlaskRequest
from google.cloud import firestore, bigquery
from google.cloud.firestore_v1.base_query import FieldFilter
from google.auth.transport.requests import Request as GoogleAuthRequest
from google.auth import default
import requests
from typing import Set, List

# Global clients
db = firestore.Client()
bq_client = bigquery.Client()

# Config
route_url = "https://us-central1-de2024-collin.cloudfunctions.net/route_requests"


def get_session_ids_for_festival(festival_id: int) -> Set[int]:
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
        session_ids = {row.id for row in query_job}
        logging.info(f"Found session IDs for festival {festival_id}: {session_ids}")
        return session_ids
    except Exception as e:
        logging.error(f"BigQuery error in get_session_ids_for_festival: {e}")
        raise


def get_user_ids_for_session(session_id: int) -> Set[int]:
    try:
        tickets_ref = db.collection("tickets")
        query = tickets_ref.where(filter=FieldFilter("session_id", "==", session_id))
        user_ids = {doc.to_dict().get("user_id") for doc in query.stream() if doc.to_dict().get("user_id")}
        logging.info(f"Found user IDs for session {session_id}: {user_ids}")
        return user_ids
    except Exception as e:
        logging.error(f"Firestore error for session {session_id}: {e}")
        raise


def get_all_user_ids(session_ids: Set[int]) -> Set[int]:
    user_ids = set()
    for session_id in session_ids:
        user_ids.update(get_user_ids_for_session(session_id))
    logging.info(f"Aggregated user IDs from sessions: {user_ids}")
    return user_ids


def build_messages(user_ids: Set[int]) -> List[dict]:
    if not user_ids:
        logging.info("No user IDs provided to build_messages")
        return []

    messages = []
    user_ids_list = list(user_ids)

    query = """
        SELECT id, email, phone, preferred
        FROM `de2024-collin.userdb.users`
        WHERE id IN UNNEST(@user_ids)
    """

    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ArrayQueryParameter("user_ids", "INT64", user_ids_list)
        ]
    )

    try:
        query_job = bq_client.query(query, job_config=job_config)
        for row in query_job:
            preferred = row.preferred.lower() if row.preferred else None
            if preferred == "email" and row.email:
                messages.append({
                    "type": "email",
                    "recipient": row.email
                })
            elif preferred == "sms" and row.phone:
                messages.append({
                    "type": "sms",
                    "recipient": row.phone
                })
            else:
                logging.warning(f"User {row.id} has unsupported preferred contact method: {row.preferred}")
        logging.info(f"Built messages: {messages}")
    except Exception as e:
        logging.error(f"BigQuery error while building messages: {e}")
        raise

    return messages


def send_messages_to_route(messages: List[dict], user_ids: Set[int]):
    try:
        credentials, _ = default()
        if not credentials.valid or credentials.expired:
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
        raise


@functions_framework.http
def festival_change(request: FlaskRequest):
    logging.info("Received festival_change request")
    request_json = request.get_json(silent=True)

    if not request_json:
        logging.warning("Missing request body")
        return jsonify({"error": "Missing request body"}), 400

    try:
        if "festival_id" in request_json:
            festival_id = int(request_json["festival_id"])
            logging.info(f"Processing festival_id: {festival_id}")
            session_ids = get_session_ids_for_festival(festival_id)
        elif "session_id" in request_json:
            session_ids = {int(request_json["session_id"])}
            logging.info(f"Processing session_id: {session_ids}")
        else:
            logging.warning("Missing festival_id or session_id in request")
            return jsonify({"error": "Missing festival_id or session_id"}), 400

        if not session_ids:
            logging.info("No session IDs found, returning empty user list")
            return jsonify({"users": [], "messages": []}), 200

        user_ids = get_all_user_ids(session_ids)
        messages = build_messages(user_ids)
        send_messages_to_route(messages, user_ids)

        logging.info(f"Response prepared with users: {user_ids} and messages: {messages}")
        return jsonify({"users": list(user_ids), "messages": messages}), 200

    except Exception as e:
        logging.error(f"Internal error in festival_change: {e}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500
