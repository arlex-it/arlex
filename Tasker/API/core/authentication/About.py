from flask.views import MethodView

from Tasker.API.core.HTTPReponse import HTTPResponse



class APICoreAuthenticationAbout(MethodView):
    print("oauth")
    #@require_authentication('private')
    def get(self, **kwargs):
        print("tata")
        if 'oauth_token' in kwargs:
            context = {
                "token": kwargs['oauth_token']
            }

            return HTTPResponse(200, context).get_response()
