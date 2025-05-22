from datetime import datetime

from flask import jsonify, request, Blueprint

from daos.Profile_dao import ProfileDAO
from db import Session

bp = Blueprint('profile', __name__)


class Profile_CRUD:
    @staticmethod
    @bp.route('/profiles', methods=['POST'])
    def create():
        body = request.get_json()
        session = Session()

        # Ensure only one profile per user
        user_id = body.get('user_id')
        existing = session.query(ProfileDAO).filter(ProfileDAO.user_id == user_id).first()
        if existing:
            session.close()
            return jsonify({'message': f'Profile for user_id {user_id} already exists'}), 403

        profile = ProfileDAO(
            user_id=user_id,
            first_name=body['first_name'],
            last_name=body['last_name'],
            bio=body.get('bio'),
            avatar_url=body.get('avatar_url'),
            created_at=datetime.utcnow()
        )

        session.add(profile)
        session.commit()
        session.refresh(profile)
        session.close()
        return jsonify({'profile_id': profile.id}), 200

    @staticmethod
    @bp.route('/profiles', methods=['GET'])
    def list():
        session = Session()
        profiles = session.query(ProfileDAO).all()
        result = [
            {
                'id': p.id,
                'user_id': p.user_id,
                'first_name': p.first_name,
                'last_name': p.last_name,
                'bio': p.bio,
                'avatar_url': p.avatar_url,
                'created_at': p.created_at.isoformat(),
                'updated_at': p.updated_at.isoformat() if p.updated_at else None
            } for p in profiles
        ]
        session.close()
        return jsonify({'results': result}), 200

    @staticmethod
    @bp.route('/profiles/<int:p_id>', methods=['GET'])
    def get(p_id):
        session = Session()
        profile = session.query(ProfileDAO).filter(ProfileDAO.id == p_id).first()
        if not profile:
            session.close()
            return jsonify({'message': f'Profile with id {p_id} not found'}), 404

        payload = {
            'id': profile.id,
            'user_id': profile.user_id,
            'first_name': profile.first_name,
            'last_name': profile.last_name,
            'bio': profile.bio,
            'avatar_url': profile.avatar_url,
            'created_at': profile.created_at.isoformat(),
            'updated_at': profile.updated_at.isoformat() if profile.updated_at else None
        }
        session.close()
        return jsonify(payload), 200

    @staticmethod
    @bp.route('/profiles/<int:p_id>', methods=['PUT'])
    def update(p_id):
        body = request.get_json()
        session = Session()
        profile = session.query(ProfileDAO).filter(ProfileDAO.id == p_id).first()
        if not profile:
            session.close()
            return jsonify({'message': f'Profile with id {p_id} not found'}), 404

        if 'first_name' in body:
            profile.first_name = body['first_name']
        if 'last_name' in body:
            profile.last_name = body['last_name']
        if 'bio' in body:
            profile.bio = body['bio']
        if 'avatar_url' in body:
            profile.avatar_url = body['avatar_url']

        profile.updated_at = datetime.utcnow()

        session.commit()
        session.refresh(profile)
        session.close()
        return jsonify({'message': 'Profile updated'}), 200

    @staticmethod
    @bp.route('/profiles/<int:p_id>', methods=['DELETE'])
    def delete(p_id):
        session = Session()
        deleted = session.query(ProfileDAO).filter(ProfileDAO.id == p_id).delete()
        session.commit()
        session.close()
        if deleted == 0:
            return jsonify({'message': f'Profile with id {p_id} not found'}), 404
        return jsonify({'message': 'Profile deleted'}), 200
