from flask_restplus import Namespace, Resource, fields

oauth_ns = Namespace('oauth', description='Oauth API Functions')

@oauth_ns.route('/user')
@oauth_ns.doc()
class OauthUserResource(Resource):
    def get(self):
        return {}

@oauth_ns.route('/authorize')
@oauth_ns.doc()
class OauthAuthorizeResource(Resource):
    def post(self):
        return {}

@oauth_ns.route('/token')
@oauth_ns.doc()
class OauthAuthorizeResource(Resource):
    def post(self):
        return {}

@oauth_ns.route('/revoke')
@oauth_ns.doc()
class OauthAuthorizeResource(Resource):
    def delete(self):
        return {}