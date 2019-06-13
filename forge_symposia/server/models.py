import json

from forge_sdk import protos as forge_protos, utils as forge_utils

from forge_symposia.server import protos
from forge_symposia.server.app import sql_db as db


class DBAssetState(db.Model):
    __tablename__ = 'asset_state'
    address = db.Column(db.String(64), primary_key=True)
    owner = db.Column(db.String(40), nullable=False)
    genesis_time = db.Column(db.String(64), nullable=False)
    moniker = db.Column(db.String(64), nullable=False)

    def __repr__(self):
        return f'<Asset {self.address}>'


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


class ForgeAssetState:
    def __init__(self, asset_state):
        self.address = asset_state.address
        self.owner = asset_state.owner
        self.moniker = asset_state.moniker
        self.parent = asset_state.parent
        self.readonly = asset_state.readonly
        self.transferrable = asset_state.transferrable
        self.ttl = asset_state.ttl
        self.consumed_time = asset_state.consumed_time
        self.issuer = asset_state.issuer
        self.context = asset_state.context
        self.stake = asset_state.stake
        self.data = asset_state.data


class ForgeAssetFactoryState(ForgeAssetState):
    def __init__(self, asset_state):
        super().__init__(asset_state)

        state = forge_utils.parse_to_proto(asset_state.data.value,
                                           forge_protos.AssetFactoryState)
        self.description = state.description
        self.limit = state.limit
        self.price = state.price
        self.template = state.template
        self.allowed_spec_args = state.allowed_spec_args
        self.asset_name = state.asset_name
        self.attributes = state.attributes
        self.num_created = state.num_created
        self.data = state.data


class EventState(ForgeAssetFactoryState):
    def __init__(self, state):
        super().__init__(state)
        template = json.loads(self.template)
        self.title = template.get('title')
        self.start_time = template.get('start_time')
        self.end_time = template.get('end_time')
        self.location = template.get('location')
        self.img_url = template.get('img_url')

        event_info = forge_utils.parse_to_proto(self.data.value,
                                                protos.EventInfo)
        self.details = event_info.details
        self.consume_tx = forge_utils.parse_to_proto(
                event_info.consume_asset_tx,
                forge_protos.Transaction)


class ResponseEvent:
    def __init__(self, event_state):
        self.num_created = event_state.num_created
        self.title = event_state.title
        self.start_time = event_state.start_time
        self.end_time = event_state.end_time
        self.location = event_state.location
        self.img_url = event_state.img_url
        self.details = event_state.details
        self.price = forge_utils.from_unit(
            forge_utils.biguint_to_int(event_state.price))
        self.address = event_state.address
        self.issuer = event_state.issuer
        self.limit = event_state.limit
        self.description = event_state.description


class TicketState:
    def __init__(self, ticket_state, event_state):
        self.title = ticket_state.title
        self.start_time = ticket_state.start_time
        self.end_time = ticket_state.end_time
        self.location = ticket_state.location
        self.img_url = ticket_state.img_url
        self.address = ticket_state.address
        self.issuer = ticket_state.issuer

        self.price = forge_utils.from_unit(
            forge_utils.biguint_to_int(event_state.price))
