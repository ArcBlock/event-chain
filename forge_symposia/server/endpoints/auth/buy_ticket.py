import logging
import uuid

from forge_sdk import did as forge_did, utils as forge_utils, protos as forge_protos

from forge_symposia.server import protos, utils
from forge_symposia.server.app import forge
from forge_symposia.server.endpoints.lib import auth_component

logger = logging.getLogger('server-auth-buy-ticket')


def get_handler(**args):
    address = args.get('user_did').lstrip(forge_did.PREFIX)
    event_address = args.get('request').args.get('event_address')

    pk = forge_utils.multibase_b58decode(args.get('user_pk'))
    acquire_asset_tx, _ = forge.rpc.build_acquire_asset_tx(
            to=event_address,
            spec_datas=[{"id": str(uuid.uuid4())}],
            type_url='ec:s:general_ticket',
            proto_lib=protos)

    tx = forge_utils.build_unsigned_tx(itx=forge_utils.encode_to_any(
            'fg:t:acquire_asset', acquire_asset_tx
    ),
            chain_id=forge.config.chain_id,
            address=address,
            pk=pk)

    return {
        'request_type': 'signature',
        'workflow': 'buy-ticket',
        'tx': tx,
        'description': 'Confirm Purchase of Ticket',
    }


def post_handler(**args):
    wallet_res = args.get('wallet_res')
    token = args.get('token')
    tx = wallet_res.get_origin_tx()
    tx.signature = wallet_res.get_signature()
    parsed_tx=forge_utils.parse_to_proto(tx.itx.value,
                               forge_protos.AcquireAssetTx)
    ticket_address = parsed_tx.specs[0].address

    res = forge.rpc.send_tx(tx)
    if res.hash:
        utils.mark_token_status(token, 'succeed')
        return {'status': 0,
                'ticket':ticket_address,
                'hash': res.hash,
                'tx': forge_utils.multibase_b58encode(
                        tx.SerializeToString())}
    else:
        utils.mark_token_status(token, 'error')
        return {'error': f"Oops, error code: {res.code}"}


buy_ticket = auth_component.create('buy_ticket',
                                   get_handler,
                                   post_handler)
