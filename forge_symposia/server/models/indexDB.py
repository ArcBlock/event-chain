from sqlalchemy import ARRAY, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AssetState(Base):
    __tablename__ = 'asset_state'
    address = Column(String(64), primary_key=True)
    owner = Column(String(40), nullable=False)
    genesis_time = Column(String(64), nullable=False)
    moniker = Column(String(64), nullable=False)


class Tx(Base):
    __tablename__ = 'tx'
    hash = Column(String(64), primary_key=True)
    sender = Column(String(40), nullable=False)
    time = Column(String(64), nullable=False)
    type = Column(String(20), nullable=False)
    code = Column(Integer, nullable=False)

    def __repr__(self):
        return f'<Tx {self.hash}>'


class AcquireAssetTx(Base):
    __tablename__ = 'acquire_asset'
    hash = Column(String(64), primary_key=True)
    sender = Column(String(40), nullable=False)
    receiver = Column(String(40), nullable=False)
    time = Column(String(64), nullable=False)
    code = Column(Integer, nullable=False)
    assets = Column(ARRAY(String), nullable=False)

    def __repr__(self):
        return f'<Tx {self.hash}>'
