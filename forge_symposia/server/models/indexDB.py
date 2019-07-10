from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class DBAssetState(Base):
    __tablename__ = 'asset_state'
    address = Column(String(64), primary_key=True)
    owner = Column(String(40), nullable=False)
    genesis_time = Column(String(64), nullable=False)
    moniker = Column(String(64), nullable=False)
