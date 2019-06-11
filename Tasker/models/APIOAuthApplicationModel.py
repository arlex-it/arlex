import re

from Tasker.models.AbstractModel import AbstractModel

class APIOAuthApplicationModel(AbstractModel):
    meta = {'collection': 'APIOAuthApplication'}

    @property
    def theme_(self):
        if hasattr(self, 'theme'):
            return self.theme

    def is_enabled(self):
        """
        Return whether an OAuthApplication is enabled or not

        :return: True if this app is enabled
        :rtype: bool
        """
        print(self.get('enabled'))

        return self.get('enabled') is True

    @property
    def allowed_redirect_URI(self):
        if hasattr(self, 'allowedRedirectURI'):
            return self.allowedRedirectURI

        return []

    def redirect_uri_allowed(self, redirect_uri):
        """
        Validate if the request redirect_uri is allowed
        :param redirect_uri: Redirect URI to validate
        :return: True if the redirect URI is allowed
        :rtype: bool
        """

        return redirect_uri in self.allowed_redirect_URI

    def can_use_grant_type(self, grant_type):
        """
        Check if app can use a specific grant type.

        :rtype: bool
        """
        if (hasattr(self, 'allowedGrantType')
                and self.allowedGrantType
                and grant_type in self.allowedGrantType):
            return True

        return False

    def can_use_scope(self, scope):
        """
        Check if app can use a specific scope.
        :rtype: bool
        """
        if not hasattr(self, 'allowedScope') or not self.allowedScope:
            return True

        for app_scope in self.allowedScope:
            pattern = re.compile(app_scope)
            if pattern.match(scope):
                return True

        return False