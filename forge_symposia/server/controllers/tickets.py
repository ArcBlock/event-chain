from forge_symposia.server import models
from forge_symposia.server.forge import forge
from forge_symposia.server.controllers import lib
from forge_sdk import protos as forge_protos, utils as forge_utils
import requests
from forge_symposia.server import utils


def list_user_tickets(user_address):
    assets = requests.get(utils.server_url('/events?where={"owner":"' +user_address+'"}')).json().get('_items')
    tickets = [lib.get_ticket_state(a.get('address')) for a in assets if _is_general_ticket(a.get('address'))]

    return [vars(ticket) for ticket in tickets]


def _is_general_ticket(address):
    state = forge.rpc.get_single_asset_state(address)
    return state and state.data.type_url == 'ec:s:general_ticket'

# TODO: move to sdk
def update_tx_multisig(tx, signer, pk, signature=None, data=None):
    multisig = forge_protos.Multisig(
            signer=signer,
            signature=signature,
            data=data,
            pk=pk,
    )
    params = {
        'from': getattr(tx, 'from'),
        'nonce': tx.nonce,
        'signature': tx.signature,
        'chain_id': tx.chain_id,
        'signatures': [multisig],
        'itx': tx.itx,
        'pk': tx.pk,
    }
    new_tx = forge_protos.Transaction(**params)
    return new_tx

def build_consume_ticket_tx(origin_tx, signature):
    old_multisig = origin_tx.signatures[0]
    new_multisig = forge_protos.Multisig(
            signer=old_multisig.signer,
            pk=old_multisig.pk,
            signature=signature,
            data=old_multisig.data
    )
    new_tx = origin_tx.__deepcopy__()
    forge_utils.add_multisigs(new_tx, [new_multisig])
    return new_tx
