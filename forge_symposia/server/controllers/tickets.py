from forge_symposia.server import models
from forge_symposia.server.forge import forge
from forge_symposia.server.controllers import lib


def list_user_tickets(user_address):
    assets = models.DBAssetState.query.filter_by(owner=user_address).all()
    tickets = [lib.get_ticket_state(a.address) for a in assets if _is_general_ticket(a.address)]

    return [vars(ticket) for ticket in tickets]


def _is_general_ticket(address):
    state = forge.rpc.get_single_asset_state(address)
    return state and state.data.type_url == 'ec:s:general_ticket'
