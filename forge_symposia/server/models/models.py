import json

from forge_sdk import protos as forge_protos, utils as forge_utils

from forge_symposia.server import protos
from forge_symposia.server.app import sql_db as db


class DBTx(db.Model):
    __tablename__ = 'tx'
    hash = db.Column(db.String(64), primary_key=True)
    sender = db.Column(db.String(40), nullable=False)
    time = db.Column(db.String(64), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    code = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Tx {self.hash}>'


class DBAcquireAssetTx(db.Model):
    __tablename__ = 'acquire_asset'
    hash = db.Column(db.String(64), primary_key=True)
    sender = db.Column(db.String(40), nullable=False)
    time = db.Column(db.String(64), nullable=False)
    code = db.Column(db.Integer, nullable=False)
    assets = db.Column(db.ARRAY(db.String), nullable=False)

    def __repr__(self):
        return f'<Tx {self.hash}>'


class DBUser(db.Model):
    __tablename__='ec_user'
    did=db.Column(db.String(64), primary_key=True)
    mobile=db.Column(db.String(30), nullable=True)
    name=db.Column(db.String(20), nullable=True)
    email=db.Column(db.String(30), nullable=True)

    def __init__(self, did, name, email, mobile=None):
        self.did = did
        self.mobile = mobile
        self.name = name
        self.email = email


class DBToken(db.Model):
    __tablename__ = 'ec_token'
    token=db.Column(db.String(20), primary_key=True)
    status=db.Column(db.String(10), primary_key=False)
    session_token=db.Column(db.String(20), primary_key=False)



