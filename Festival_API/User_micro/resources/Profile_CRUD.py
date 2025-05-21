from flask_restful import Resource, reqparse
from daos.Profile_dao import ProfileDAO

parser = reqparse.RequestParser()
parser.add_argument('user_id', type=int, required=True)
parser.add_argument('bio', type=str)
parser.add_argument('contact', type=str)

class ProfileListResource(Resource):
    def get(self):
        dao = ProfileDAO()
        return [vars(p) for p in dao.db.query(p for p in dao.db.query.__self__.__class__).all()], 200

    def post(self):
        args = parser.parse_args()
        dao = ProfileDAO()
        profile = dao.create(args['user_id'], args.get('bio'), args.get('contact'))
        return vars(profile), 201

class ProfileResource(Resource):
    def get(self, profile_id):
        dao = ProfileDAO()
        profile = dao.get(profile_id)
        return vars(profile), 200 if profile else 404

    def put(self, profile_id):
        args = parser.parse_args()
        dao = ProfileDAO()
        profile = dao.update(profile_id, **{k:v for k,v in args.items() if v is not None})
        return vars(profile), 200

    def delete(self, profile_id):
        dao = ProfileDAO()
        dao.delete(profile_id)
        return '', 204