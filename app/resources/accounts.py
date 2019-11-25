from flask_restplus import Namespace, Resource, fields

accounts_ns = Namespace('accounts', description='Account API Functions')

@accounts_ns.route('/')
@accounts_ns.doc()
class AccountResource(Resource):
    def get(self, id):
        return {}
    
    def put(self, id):
        return {}
    
    def post(self):
        return {}

    def delete(self, id):
        return {}

@accounts_ns.doc()
class AccountPositionListResource(Resource):
    def get(self, id):
        return {}

@accounts_ns.doc()
class AccountPositionResource(Resource):
    def put(self, id, position_id):
        return {}

    def post(self, id):
        return {}
    
    def delete(self, id, position_id):
        return {}

accounts_ns.add_resource(AccountResource, '/', methods=['POST'])
accounts_ns.add_resource(AccountResource, '/<id>', methods=['GET', 'PUT', 'DELETE'])
accounts_ns.add_resource(AccountPositionListResource, '/<id>/positions', methods=['GET'])
accounts_ns.add_resource(AccountPositionResource, '/<id>/positions', methods=['POST'])
accounts_ns.add_resource(AccountPositionResource, '/<id>/positions/<position_id>', methods=['GET', 'PUT', 'DELETE'])