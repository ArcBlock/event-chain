import json

from flask import jsonify, request
from forge_sdk import did as forge_did, protos as forge_protos, \
    utils as forge_utils

from forge_symposia.server import controllers, utils
from forge_symposia.server.endpoints.lib import auth_component
from forge_symposia.server.forge import forge


def get_handler(**args):
    event_address = args.get('request').args.get('event_address')
    event_factory = controllers.get_event_state(event_address)

    return {
        'request_type': 'asset',
        'description': 'Please select a ticket for event.',
        'workflow': 'use-ticket',
        'target': event_factory.title,
    }


def post_handler(**args):
    wallet_res = args.get('wallet_res')
    asset_address = wallet_res.get_asset_address()
    ticket = controllers.get_ticket_state(asset_address)

    new_tx = controllers.update_tx_multisig(
            tx=forge_utils.parse_to_proto(
                    forge_utils.multibase_b58decode(ticket.consume_tx),
                    forge_protos.ConsumeAssetTx),
            signer=wallet_res.get_address(),
            pk=wallet_res.get_user_pk(),
            data=forge_utils.encode_to_any(
                    'fg:x:address',
                    asset_address,
            )
    )

    utils.mark_token_status(args, 'succeed')
    params = {'status': 0,
              'tx': new_tx,
              'url': utils.server_url(
                      f'/api/did/consume_asset/consume?_t_={token}&ticket_address={ticket.address}'),
              'description': 'Confirm to use the ticket.',
              'action': 'responseAuth',
              'workflow': 'use-ticket',
              }
    return json.dumps(utils.send_did_request(request_type='signature',
                                             **params,
                                             **args.get('app_params')))


consume_ticket = auth_component.create('consume_ticket',
                                       get_handler,
                                       post_handler)


@consume_ticket.route('/status', methods=['POST'])
def consume():
    wallet_res = forge_did.WalletResponse(request.get_json())
    tx = controllers.build_consume_ticket_tx(
            wallet_res.get_origin_tx(),
            wallet_res.get_signature(),
    )
    res = forge.rpc.send(tx)

    base58_tx = forge_utils.multibase_b58encode(tx.SerializeToString())
    if res.hash:
        return jsonify({'hash': hash,
                        'tx': base58_tx,
                        'ticket': request.args.get('ticket_address')})
    else:
        return jsonify({'error': 'Your ticket might have been '
                                 'checked out before. '
                                 'Please wait and try again.'})
