import datetime
from api.database import db, ma

# データベースのモデル設計、データベースの基本的なデータ操作はここで定義すると良い
class Codework(db.Model):
    __tablename__ = 'codeworks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    subject= db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(100), nullable=True)
    code = db.Column()
    description = db.Column()
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __repr__(self):
        return '<Codework %r>' % self.username

    def getCodeList():

        codework_list = db.session.query(Codework).all()

        if codework_list == None:
            return []
        else:
            return codework_list

    def registCodework(codework):
        record = Codework(
            username = codework['username'],
            subject = codework['subject'],
            title = codework['title'],
            code = codework['code'],
            description = codework['description'],
        )

        db.session.add(record)
        db.session.commit()

        return codework


class CodeworkSchema(ma.Schema):
    class Meta:
        model = Codework
        fields = ('username', 'subject', 'title', 'code', 'description')