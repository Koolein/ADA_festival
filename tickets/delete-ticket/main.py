import base64
import json
from google.cloud import firestore, bigquery

def delete_ticket(event, context):
    try:
        data = json.loads(base64.b64decode(event['data']).decode('utf-8'))
        ticket_id = data['ticket_id']

        db = firestore.Client()
        ticket_ref = db.collection('tickets').document(ticket_id)
        ticket = ticket_ref.get()

        if not ticket.exists:
            print(f" Ticket {ticket_id} not found.")
            return

        ticket_data = ticket.to_dict()
        session_id = ticket_data['session_id']

        # 1. Mark ticket as cancelled
        ticket_ref.update({
            'status': 'cancelled'
        })
        print(f" Ticket {ticket_id} marked as cancelled.")

        # 2. Update big Query
        client = bigquery.Client()

        query = f"""
        UPDATE `de2024-collin.festivaldb.sessions`
        SET issued = GREATEST(issued - 1, 0)
        WHERE id = {session_id}
        """
        client.query(query).result()

    except Exception as e:
        print(f" Error cancelling ticket: {e}")
