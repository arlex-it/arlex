from Tasker.API.core.authentication.About import APICoreAuthenticationAbout
from Tasker.API.core.authentication.GetAuthorize import APICoreAuthenticationGetAuthorize
from Tasker.API.core.authentication.PostAuthorize import APICoreAuthentificationPostAuthorize
from Tasker.API.core.authentication.PostToken import APICoreAuthenticationPostToken

def register_oauth_routes(blueprint):

    @blueprint.route("/oauth/authorize")
    def oauth_authorize():
        return APICoreAuthenticationGetAuthorize().dispatch_request(blueprint)

    blueprint.add_url_rule('/oauth/authorize', methods=['POST'], view_func=APICoreAuthentificationPostAuthorize().as_view('APICoreAuthenticationPostAuthorize'))
    blueprint.add_url_rule('/oauth/token', methods=['POST'], view_func=APICoreAuthenticationPostToken().as_view('APICoreAuthenticationPostToken'))
    blueprint.add_url_rule('/oauth/about', methods=['GET'], view_func=APICoreAuthenticationAbout().as_view('APICoreAuthenticationAbout'))
