from flask_restplus import Namespace, Resource, fields

users_ns = Namespace('users', description='User API Functions')

@users_ns.doc()
class UserResource(Resource):
    def get(self, id):
        api.abort(403)

    def patch(self, id):
        api.abort(403)
    
    def post(self):
        api.abort(403)

users_ns.add_resource(UserResource, '/', methods=['POST'])
users_ns.add_resource(UserResource, '/<id>', methods=['GET', 'PATCH'])