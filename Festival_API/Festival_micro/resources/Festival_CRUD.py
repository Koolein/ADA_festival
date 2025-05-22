from datetime import datetime

from flask import jsonify, request, Blueprint

from daos.Festival_dao import FestivalDAO
from db import Session
from constant import FestivalStatus

bp = Blueprint('festival', __name__)

from db import Session


class Festival_CRUD:
    @staticmethod
    @bp.route('/festivals', methods=['POST'])
    def create():
        body = request.get_json()
        session = Session()
        f_id = body.get('id')
        existing = session.query(FestivalDAO).filter(FestivalDAO.id == int(f_id)).first()
        if existing:
            session.close()
            return jsonify({'message': f'There is already a festival with id {f_id}'}), 403
        # construct and persist new Festival
        fest = FestivalDAO(
            id=int(body['id']),
            name=body['name'],
            start_date=datetime.fromisoformat(body['start_date']),
            end_date=datetime.fromisoformat(body['end_date'])
        )
        session.add(fest)
        session.commit()
        session.refresh(fest)
        session.close()
        return jsonify({'festival_id': fest.id}), 200

    @staticmethod
    @bp.route('/festivals', methods=['GET'])
    def list():
        session = Session()
        festivals = session.query(FestivalDAO).all()
        result = [
            {
                'id': f.id,
                'name': f.name,
                'start_date': f.start_date.isoformat(),
                'end_date': f.end_date.isoformat()
            } for f in festivals
        ]
        session.close()
        return jsonify({"festival": result}), 200

    @staticmethod
    @bp.route('/festivals/<int:f_id>', methods=['GET'])
    def get(f_id):
        session = Session()
        fest = session.query(FestivalDAO).filter(FestivalDAO.id == int(f_id)).first()
        if not fest:
            session.close()
            return jsonify({'message': f'There is no festival with id {f_id}'}), 404
        payload = {
            'id': fest.id,
            'name': fest.name,
            'start_date': fest.start_date.isoformat(),
            'end_date': fest.end_date.isoformat()
        }
        session.close()
        return jsonify(payload), 200

    @staticmethod
    @bp.route('/festivals/<int:f_id>', methods=['PUT'])
    def update(f_id):
        body = request.get_json()
        session = Session()
        fest = session.query(FestivalDAO).filter(FestivalDAO.id == int(f_id)).first()
        if not fest:
            session.close()
            return jsonify({'message': f'There is no festival with id {f_id}'}), 404
        # update provided fields
        if 'name' in body:
            fest.name = body['name']
        if 'start_date' in body:
            fest.start_date = datetime.fromisoformat(body['start_date'])
        if 'end_date' in body:
            fest.end_date = datetime.fromisoformat(body['end_date'])
        if 'status' in body:
            try:
                # this converts the incoming string to your enum member
                new_status = FestivalStatus(body['status'])
            except ValueError:
                session.close()
                return jsonify({
                    'message': f"Invalid status '{body['status']}'.  "
                            f"Allowed: {[s.value for s in FestivalStatus]}"
                }), 400
            fest.status = new_status  # SQLAlchemy Enum column will store new_status.value
            
        session.commit()
        session.refresh(fest)
        session.close()
        return jsonify({'message': 'Festival updated'}), 200

    @staticmethod
    @bp.route('/festivals/<int:f_id>', methods=['DELETE'])
    def delete(f_id):
        session = Session()
        deleted = session.query(FestivalDAO).filter(FestivalDAO.id == int(f_id)).delete()
        session.commit()
        session.close()
        if deleted == 0:
            return jsonify({'message': f'There is no festival with id {f_id}'}), 404
        return jsonify({'message': 'Festival deleted'}), 200
