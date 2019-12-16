from bdd.db_connection import session, User, Token
from API.Utilities.HttpResponse import *
from sqlalchemy import select


class CheckAuthToken:

	def check_user(request=None):
		data = request.json
		if 'access_token' not in data or 'refresh_token' not in data:
			return False
		check_user = session.query(Token) \
			.join(User, User.id == Token.id_user) \
			.filter(Token.access_token == data['access_token'])\
			.first()
		if check_user is None:
			return False
		return True
