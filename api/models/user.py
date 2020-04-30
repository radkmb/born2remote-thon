import json
from api.database import db, ma

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(50), nullable=False, unique=True)
	password = db.Column(db.String(255), nullable=False)

	# current_identityの内容を定義
	def __str__(self):
		strData = json.dumps({'id': self.id, 'name': self.name})
		return strData

	# ユーザーの名前を使って、ユーザー情報を取る。ログイン認証用
	def getUserListByName():
		user_list = db.session.query(User).all()
		username_table = {u.name: u for u in user_list}
		if user_list == None:
			return []
		else:
			return username_table

	# ユーザーのIDを使って、ユーザー情報を取る。ログイン認証用
	def getUserListByID():
		user_list = db.session.query(User).all()
		userid_table = {u.id: u for u in user_list}
		if user_list == None:
			return []
		else:
			return userid_table

	def registUser(user):
		record = User(
			name = user['name'],
			password = user['password']
		)
		db.session.add(record)
		db.session.commit()

		return user
