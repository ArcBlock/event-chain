from event_chain.app import db


class AssetState(db.Model):
    __tablename__ = 'asset_state'
    address = db.Column(db.String(64), primary_key=True)
    owner = db.Column(db.String(40), nullable=False)
    genesis_time = db.Column(db.String(64), nullable=False)
    moniker = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'<Asset {self.address}>'


class Tx(db.Model):
    __tablename__ = 'tx'
    hash = db.Column(db.String(64), primary_key=True)
    sender = db.Column(db.String(40), nullable=False)
    time = db.Column(db.String(64), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    code = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Tx {self.hash}>'


class AcquireAssetTx(db.Model):
    __tablename__ = 'acquire_asset'
    hash = db.Column(db.String(64), primary_key=True)
    sender = db.Column(db.String(40), nullable=False)
    time = db.Column(db.String(64), nullable=False)
    code = db.Column(db.Integer, nullable=False)
    assets = db.Column(db.ARRAY(db.String), nullable=False)

    def __repr__(self):
        return f'<Tx {self.hash}>'
