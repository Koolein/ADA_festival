from flask import Flask
from flask_restful import Api
from resources.User_CRUD import UserListResource, UserResource
from resources.Profile_CRUD import ProfileListResource, ProfileResource

app = Flask(__name__)
api = Api(app)

# User endpoints
api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')

# Profile endpoints
api.add_resource(ProfileListResource, '/profiles')
api.add_resource(ProfileResource, '/profiles/<int:profile_id>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)