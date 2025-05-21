import functions_framework
import logging
from flask import jsonify, Request
from google.cloud import firestore, bigquery
from google.cloud.firestore_v1.base_query import FieldFilter


@functions_framework.http
def festival_change(request: Request):
    request_json = request.get_json(silent=True)

    if not request_json:
        return jsonify({"error": "Missing request body"}), 400

    # Initialize clients
    bq_client = bigquery.Client()
    db = firestore.Client()

    user_ids = set()

    if 'festival_id' in request_json:
        festival_id = request_json['festival_id']
        logging.info(f"Received festival_id: {festival_id}")

        query = """
            SELECT id
            FROM `de2024-collin.festivaldb.sessions`
            WHERE festival_id = @festival_id
        """

        job_config = bigquery.QueryJobConfig(
            query_parameters=[bigquery.ScalarQueryParameter("festival_id", "INT64", festival_id)]
        )

        session_ids = set()
        try:
            query_job = bq_client.query(query, job_config=job_config)
            for row in query_job:
                session_ids.add(row.id)
        except Exception as e:
            logging.error(f"BigQuery error: {e}")
            return jsonify({"error": "BigQuery query failed"}), 500

        if not session_ids:
            logging.info("No session IDs found for the given festival_id.")
            return jsonify({"users": []}), 200

        for session_id in session_ids:
            session_id = int(session_id)

            try:
                tickets = db.collection("tickets")
                query = tickets.where(filter=FieldFilter("session_id", "==", session_id))
                docs = query.stream()

                for doc in docs:
                    data = doc.to_dict()
                    
                    if "user_id" in data:
                        user_ids.add(data["user_id"])

            except Exception as e:
                logging.error(f"Firestore query error: {e}")
                return jsonify({"error": "Firestore query failed"}), 500


    elif 'session_id' in request_json:
        session_id = request_json['session_id']
        logging.info(f"Received session_id: {session_id}")
        session_id = int(session_id)

        try:
            tickets = db.collection("tickets")
            query = tickets.where(filter=FieldFilter("session_id", "==", session_id))
            docs = query.stream()

            for doc in docs:
                data = doc.to_dict()
                
                if "user_id" in data:
                    user_ids.add(data["user_id"])

        except Exception as e:
            logging.error(f"Firestore query error: {e}")
            return jsonify({"error": "Firestore query failed"}), 500

    else:
        return jsonify({"error": "Missing festival_id or session_id"}), 400

    logging.info(f"Found users: {list(user_ids)}")
    return jsonify({"users": list(user_ids)}), 200
