import arrow

from bdd.db_connection import session, AccessToken, to_dict


class OAuthAuthenticationToken(object):
	"""
	Helper for OAuth authentification.
	"""
	def __init__(self, token):
		"""
		:param str token:
		"""
		self.token = token
		self._model = session.query(AccessToken).filter(AccessToken.token == token).first()
		if self._model is None:
			raise ValueError(f'Cannot find token {self.token}')

	def is_valid(self):
		"""
		:rtype: bool
		"""
		if hasattr(self._model, 'is_enable') and self._model.is_enable:
			return True

		return False

	def is_valid_token(self):
		"""
		:rtype: bool
		"""
		if self._model and self.is_valid():
			if hasattr(self._model, 'app_id'):
				# app_id = self._model.app_id

				# app = APIOAuthApplicationModel.objects(id=app_id).first()
				# TODO Check app availability + enabled

				return True

		return False

	def get_token_infos(self):
		if self._model and self.is_valid():
			return {
				'token': self._model.token,
				'expiration_date': arrow.get(self._model.expiration_date).isoformat()
			}

	def validate_user_access(self, kwargs):
		user_connected = session.query(AccessToken).filter(AccessToken.token == self.token).first()
		user_connected = to_dict(user_connected)
		if int(user_connected['id_user']) != int(kwargs['user_id']):
			return False
		return True

	def has_scopes(self, required_scopes=[]):
		"""
		:rtype: bool
		"""
		if not required_scopes or len(required_scopes) <= 0:
			return True

		for scope in required_scopes:
			if not self._model.has_scope(scope):
				return False

		return True
