from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    app.app_context().push()
    db.init_app(app)
    db.create_all()
    return db


class DBUser(db.Model):
    __bind_key__ = "app_db"
    __tablename__ = 'ec_user'
    did = db.Column(db.String(64), primary_key=True)
    mobile = db.Column(db.String(30), nullable=True)
    name = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(30), nullable=True)

    def __init__(self, did, name, email, mobile=None):
        self.did = did
        self.mobile = mobile
        self.name = name
        self.email = email


class DBToken(db.Model):
    __bind_key__ = "app_db"
    __tablename__ = 'ec_token'
    token = db.Column(db.String(20), primary_key=True)
    status = db.Column(db.String(10), primary_key=False)
    session_token = db.Column(db.String(20), primary_key=False)
