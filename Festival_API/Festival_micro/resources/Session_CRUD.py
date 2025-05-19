from datetime import datetime

from flask import jsonify, request, Blueprint

from daos.Festival_dao import FestivalDAO
from daos.Session_dao import SessionDAO
from db import Session
from constant import SessionStatus
bp = Blueprint('Session', __name__)

from db import Session

class Session_CRUD:
    @staticmethod
    @bp.route('/festivals/<int:f_id>/sessions', methods=['POST'])
    def create(f_id):
        body = request.get_json()
        session = Session()
        fest = session.query(FestivalDAO).filter(FestivalDAO.id == int(f_id)).first()
        if not fest:
            session.close()
            return jsonify({'message': f'There is no festival with id {f_id}'}), 404
        new_sess = SessionDAO(
            festival_id=int(f_id),
            title=body['title'],
            start_time=datetime.fromisoformat(body['start_time']),
            end_time=datetime.fromisoformat(body['end_time'])
        )
        session.add(new_sess)
        session.commit()
        session.refresh(new_sess)
        session.close()
        return jsonify({'session_id': new_sess.id}), 201

    @staticmethod
    @bp.route('/festivals/<int:f_id>/sessions', methods=['GET'])
    def list(f_id):
        session = Session()
        sessions = session.query(SessionDAO).filter(SessionDAO.festival_id == int(f_id)).all()
        result = [
            {
                'id': s.id,
                'festival_id': s.festival_id,
                'title': s.title,
                'start_time': s.start_time.isoformat(),
                'end_time': s.end_time.isoformat()
            } for s in sessions
        ]
        session.close()
        return jsonify(result), 200

    @staticmethod
    @bp.route('/sessions/<int:s_id>', methods=['GET'])
    def get(s_id):
        session = Session()
        sess = session.query(SessionDAO).filter(SessionDAO.id == int(s_id)).first()
        if not sess:
            session.close()
            return jsonify({'message': f'There is no session with id {s_id}'}), 404
        payload = {
            'id': sess.id,
            'festival_id': sess.festival_id,
            'title': sess.title,
            'start_time': sess.start_time.isoformat(),
            'end_time': sess.end_time.isoformat()
        }
        session.close()
        return jsonify(payload), 200

    @staticmethod
    @bp.route('/sessions/<int:s_id>', methods=['PUT'])
    def update(s_id):
        body = request.get_json()
        session = Session()
        sess = session.query(SessionDAO).filter(SessionDAO.id == int(s_id)).first()
        if not sess:
            session.close()
            return jsonify({'message': f'There is no session with id {s_id}'}), 404
        if 'title' in body:
            sess.title = body['title']
        if 'start_time' in body:
            sess.start_time = datetime.fromisoformat(body['start_time'])
        if 'end_time' in body:
            sess.end_time = datetime.fromisoformat(body['end_time'])
        if 'status' in body:
            try:
                new_status = SessionStatus(body['status'])
            except ValueError:
                session.close()
                return jsonify({
                    'message': f"Invalid status '{body['status']}'.  "
                            f"Allowed: {[s.value for s in SessionStatus]}"
                }), 400
            session.status = new_status
        session.commit()
        session.refresh(sess)
        session.close()
        return jsonify({'message': 'Session updated'}), 200

    @staticmethod
    @bp.route('/sessions/<int:s_id>', methods=['DELETE'])
    def delete(s_id):
        session = Session()
        deleted = session.query(SessionDAO).filter(SessionDAO.id == int(s_id)).delete()
        session.commit()
        session.close()
        if deleted == 0:
            return jsonify({'message': f'There is no session with id {s_id}'}), 404
        return jsonify({'message': 'Session deleted'}), 200
