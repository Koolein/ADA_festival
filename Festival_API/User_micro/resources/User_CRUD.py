from flask_restful import Resource, reqparse
from daos.User_dao import UserDAO

parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help='Username cannot be blank')
parser.add_argument('email', type=str, required=True, help='Email cannot be blank')

class UserListResource(Resource):
    def get(self):
        dao = UserDAO()
        return [vars(u) for u in dao.db.query(dao.db.query(dao.db.query.__self__.__class__).all() )], 200

    def post(self):
        args = parser.parse_args()
        dao = UserDAO()
        user = dao.create(args['username'], args['email'])
        return vars(user), 201

class UserResource(Resource):
    def get(self, user_id):
        dao = UserDAO()
        user = dao.get(user_id)
        return vars(user), 200 if user else 404

    def put(self, user_id):
        args = parser.parse_args()
        dao = UserDAO()
        user = dao.update(user_id, **args)
        return vars(user), 200

    def delete(self, user_id):
        dao = UserDAO()
        dao.delete(user_id)
        return '', 204