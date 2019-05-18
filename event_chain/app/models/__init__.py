from event_chain.app.models.admin import *
from event_chain.app.models.event import *
from event_chain.app.models.states import *
from event_chain.app.models.ticket import *
from event_chain.app.models import sql
from event_chain.app.models.admin import *
from event_chain.app.models.states import *
from event_chain.app.models.mobile import *


class TransactionInfo:
    def __init__(self, state):
        self.height = state.height
        self.hash = state.hash
        self.tx = state.tx
        self.time = state.time


def get_event_factory(address):
    state = forge_rpc.get_single_asset_state(address)
    return EventState(state)
