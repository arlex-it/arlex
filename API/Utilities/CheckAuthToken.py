from bdd.db_connection import session, User, Token
import datetime
from uuid import uuid4

class CheckAuthToken:

	def check_user(request=None):
		data = request.json
		if 'access_token' not in data or 'refresh_token' not in data:
			return False
		check_user = session.query(Token) \
			.join(User, User.id == Token.id_user) \
			.filter(Token.access_token == data['access_token'])\
			.first()
		# check access_token correspond to user
		if check_user is None:
			return False
		print(check_user.expiration_date)
		# if access_token is expired then generate new tokens
		if check_user.expiration_date < datetime.datetime.now():
			new_access_token = uuid4().hex[:35]
		return True
