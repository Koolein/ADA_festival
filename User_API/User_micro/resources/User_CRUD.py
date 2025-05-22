from datetime import datetime

from flask import jsonify, request, Blueprint

from daos.User_dao import UserDAO
from db import Session

bp = Blueprint('user', __name__)


class User_CRUD:
    @staticmethod
    @bp.route('/users', methods=['POST'])
    def create():
        body = request.get_json()
        session = Session()
        id = body.get('id')
        username = body.get('username')
        email = body.get('email')
        existing_user = session.query(UserDAO).filter(
            (UserDAO.username == username) | (UserDAO.email == email)
        ).first()

        if existing_user:
            session.close()
            return jsonify({'message': 'A user with that username or email already exists'}), 403

        user = UserDAO(
            id=id,
            username=username,
            email=email,
            hashed_password=body['hashed_password'],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            phone=body.get('phone'),
            preferred=body.get('preferred', 'SMS')  # Default to SMS if not provided
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        session.close()
        return jsonify({'user_id': user.id}), 201

    @staticmethod
    @bp.route('/users', methods=['GET'])
    def list():
        session = Session()
        users = session.query(UserDAO).all()
        result = [
            {
                'id': u.id,
                'username': u.username,
                'email': u.email,
                'created_at': u.created_at.isoformat(),
                'updated_at': u.updated_at.isoformat() if u.updated_at else None,
                'phone': u.phone,
                'preferred': u.preferred
            } for u in users
        ]
        session.close()
        return jsonify({"results": result}), 200

    @staticmethod
    @bp.route('/users/<int:u_id>', methods=['GET'])
    def get(u_id):
        session = Session()
        user = session.query(UserDAO).filter(UserDAO.id == u_id).first()
        if not user:
            session.close()
            return jsonify({'message': f'There is no user with id {u_id}'}), 404

        payload = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat() if user.updated_at else None
        }
        session.close()
        return jsonify(payload), 200

    @staticmethod
    @bp.route('/users/<int:u_id>', methods=['PUT'])
    def update(u_id):
        body = request.get_json()
        session = Session()
        user = session.query(UserDAO).filter(UserDAO.id == u_id).first()
        if not user:
            session.close()
            return jsonify({'message': f'There is no user with id {u_id}'}), 404

        if 'username' in body:
            user.username = body['username']
        if 'email' in body:
            user.email = body['email']
        if 'hashed_password' in body:
            user.hashed_password = body['hashed_password']

        user.updated_at = datetime.utcnow()

        session.commit()
        session.refresh(user)
        session.close()
        return jsonify({'message': 'User updated'}), 200

    @staticmethod
    @bp.route('/users/<int:u_id>', methods=['DELETE'])
    def delete(u_id):
        session = Session()
        deleted = session.query(UserDAO).filter(UserDAO.id == u_id).delete()
        session.commit()
        session.close()
        if deleted == 0:
            return jsonify({'message': f'There is no user with id {u_id}'}), 404
        return jsonify({'message': 'User deleted'}), 200
