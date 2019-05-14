# flake8: noqa

from event_chain.application.models import sql
from event_chain.application.models.admin import *
from event_chain.application.models.states import *


def get_event_factory(address):
    state = forge_rpc.get_single_asset_state(address)
    return EventState(state)
