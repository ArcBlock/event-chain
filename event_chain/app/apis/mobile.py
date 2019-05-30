import logging
import uuid

from flask import Blueprint
from flask import request
from flask import url_for
from forge_sdk import rpc as forge_rpc, utils as forge_utils

from event_chain import protos
from event_chain.app import controllers
from event_chain.app import models
from event_chain.app import utils
from event_chain.app.apis import lib

logger = logging.getLogger('api-mobile')

api_mobile = Blueprint(
        'api_mobile',
        __name__
)


@api_mobile.route(
        "/buy-ticket/<event_address>",
        methods=['GET', 'POST'],
)
def buy_ticket(event_address):
    try:
        if request.method == 'GET':

            wallet = lib.parse_request_get(request,'buy-ticket')

            acquire_asset_tx, _ = forge_rpc.build_acquire_asset_tx(
                    to=event_address,
                    spec_datas=[{"id": str(uuid.uuid4())}],
                    type_url='ec:s:general_ticket',
                    proto_lib=protos)

            unsigned_tx = forge_rpc.build_unsigned_tx(
                    forge_utils.encode_to_any('fg:t:acquire_asset',
                                              acquire_asset_tx), wallet, 2)

            did_request_params = {
                'did': wallet.did,
                'tx': unsigned_tx,
                'url': url_for('api_mobile.buy_ticket',
                               event_address=event_address),
            }
            response = controllers.require_sig_buy_ticket(**did_request_params)

            logger.debug(f'did auth response: {response}')
            return response

        elif request.method == 'POST':
            wallet_res = lib.parse_request_post(request, 'mobile-buy-ticket')
            if not wallet_res:
                return lib.error("Error in parsing wallet data.")

            participant_state = models.get_participant_state(
                    wallet_res.get_address())
            if not participant_state:
                return lib.error(
                        f"user {wallet_res.get_address()} doesn't exist.")

            ticket_address, tx_hash = controllers.buy_ticket_mobile(
                    wallet_res.get_origin_tx(),
                    wallet_res.get_signature(),
            )
            tx = wallet_res.get_origin_tx().__deepcopy__()
            tx.signature = wallet_res.get_signature()

            if ticket_address and tx_hash:
                logger.info(f"Ticket {ticket_address} is bought successfully.")

                return lib.ok({'ticket': ticket_address,
                               'hash': tx_hash,
                               'tx': utils.base58_encode_tx(tx)})
            else:
                return lib.error('Whoops. Something is wrong :(')
    except Exception as e:
        logger.error(e, exc_info=True)
        return lib.error('Exception in buying ticket.')


@api_mobile.route("/poke", methods=['GET', 'POST'])
def poke():
    try:
        if request.method == 'GET':

            account = lib.parse_request_get(request, 'mobile-poke')

            did_request_params = {
                'did': account.did,
                'tx': controllers.gen_poke_tx(account.address, account.pk),
                'url': url_for('api_mobile.poke'),
            }

            return controllers.require_sig_poke(**did_request_params)

        elif request.method == 'POST':

            wallet_res = lib.parse_request_post(request, 'mobile-poke')

            if not wallet_res:
                return lib.error("Error in parsing wallet data.")

            hash = controllers.send_poke_tx(wallet_res.get_origin_tx(),
                                            wallet_res.get_signature())
            if hash:
                return lib.ok({'hash': hash,
                               'tx': utils.base58_encode_tx(
                                       controllers.gen_poke_tx(
                                               wallet_res.get_address(),
                                               wallet_res.get_user_pk()))})

            else:
                return lib.error('Whoops! All rewards are taken.'
                                 ' Please try again tomorrow.')
    except Exception as e:
        logger.error(e, exc_info=True)
        return lib.error('Whoops! All rewards are taken.'
                         ' Please try again tomorrow.')


@api_mobile.route(
        "/require-asset/<event_address>", methods=['GET', 'POST'])
def require_asset(event_address):
    try:
        event = models.get_event_factory(event_address)

        if request.method == 'GET':
            lib.parse_request_get(request, 'require-asset')
            params = {
                'url': url_for(
                        'api_mobile.require_asset',
                        event_address=event_address),
                'target': event.title,
            }
            response = controllers.require_asset_consume(**params)
            return response

        if request.method == 'POST':
            wallet_res = lib.parse_request_post(request, 'require-asset')

            if not wallet_res:
                return lib.error("Error in parsing wallet data.")

            asset_address = wallet_res.get_asset_address()
            if not asset_address:
                return lib.error("Please provide an asset address.")

            new_tx = utils.update_tx_multisig(
                    tx=event.consume_tx,
                    signer=wallet_res.get_address(),
                    pk=wallet_res.get_user_pk(),
                    data=forge_utils.encode_to_any(
                            'fg:x:address',
                            asset_address,
                    )
            )

            params = {
                'did': wallet_res.get_address(),
                'tx': new_tx,
                'url': url_for('api_mobile.consume',
                               ticket_address=asset_address),
            }
            return controllers.require_sig_consume(**params)

    except Exception as e:
        logger.error(e, exc_info=True)
        return lib.error("Exception in requesting asset.")


@api_mobile.route(
        "/consume/<ticket_address>", methods=['POST'],
)
def consume(ticket_address):
    try:
        if request.method == 'POST':
            wallet_res = lib.parse_request_post(request, 'consume-asset')

            if not wallet_res:
                return lib.error("Error in parsing wallet data.")

            hash = controllers.consume_ticket_mobile(
                    wallet_res.get_origin_tx(),
                    wallet_res.get_signature(),
                    ticket_address,
            )
            base58_tx = utils.base58_encode_tx(
                    controllers.build_cosnume_ticket_mobile_tx(
                            wallet_res.get_origin_tx(),
                            wallet_res.get_signature()))
            if hash:
                return lib.ok({'hash': hash,
                               'tx': base58_tx})
            else:
                return lib.error('Your ticket might have been '
                                 'checked out before. '
                                 'Please wait and try again.')
    except Exception as e:
        logger.error(e, exc_info=True)
        return lib.error("Exception in consuming ticket.")
