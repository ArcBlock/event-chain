import logging
import secrets
import urllib.parse

from flask import Blueprint
from flask import jsonify, request
from forge_sdk import did as forge_did
from forge_sdk import utils as forge_utils

from forge_symposia.server import env
from forge_symposia.server import utils
from forge_symposia.server.app import forge

logger = logging.getLogger('auth-lib')


def create(operation,
           get_handler,
           post_handler):
    bp = Blueprint(f'auth-component-{operation}', __name__,
                   url_prefix=f'/api/did/{operation}')

    @bp.route('/auth', methods=['GET', 'POST'])
    def auth():
        token = request.args.get('_t_')
        app_params = {
            'action': 'responseAuth',
            'chain_host': env.CHAIN_HOST,
            'app_addr': env.APP_ADDR,
            'app_pk': env.APP_PK,
            'app_sk': env.APP_SK,
            'chain_id': forge.config.chain_id,
            'chain_version': forge.rpc.get_chain_info().info.version,
            'token_symbol': forge.config.symbol,
            'decimals': forge.config.decimal,
        }

        if request.method == 'GET':
            user_did = request.args.get('userDid')
            app_params['user_did'] = user_did
            app_params['url'] = utils.server_url(
                    f'/api/did/{operation}/auth?_t_={token}')
            user_pk = request.args.get('userPk')
            utils.mark_token_status(token, 'scanned')

            user_params = get_handler(token=token,
                                      user_did=user_did,
                                      user_pk=user_pk,
                                      request=request)

            return utils.send_did_request(**app_params, **user_params)

        if request.method == 'POST':
            wallet_res = forge_did.WalletResponse(request.get_json())
            response_data = post_handler(token=token,
                                         wallet_res=wallet_res,
                                         app_params=app_params)
            logger.debug(jsonify(response_data))
            return jsonify(response_data)

    @bp.route('/token', methods=['GET'])
    def token():
        event_address = request.args.get('event_address')
        return get_token(operation, event_address)

    @bp.route('/status', methods=['GET'])
    def status():
        return check_status()

    @bp.route('/timeout', methods=['GET'])
    def timeout():
        return token_timeout()

    return bp


def get_token(endpoint, event_address):
    token = secrets.token_hex(8)
    utils.mark_token_status(token, 'created')

    default = utils.server_url(f'/api/did/{endpoint}/auth?_t_={token}')

    url = forge_utils.did_url(
            url=default if not event_address else urllib.parse.quote(utils.server_url(
                f'/api/did/{endpoint}/auth'
                f'?_t_={token}&event_address={event_address}')),
            action='requestAuth',
            app_pk=forge_utils.multibase_b58encode(env.APP_PK),
            app_addr=env.APP_ADDR)

    return jsonify(token=token, url=url)


def check_status():
    token = utils.check_token_status(request.args.get('_t_'))
    if not token:
        return jsonify(error="Token does not exist.")
    elif token.session_token:
        return jsonify(token=token.token,
                       status=token.status,
                       sessionToken=token.session_token)
    else:
        return jsonify(token=token.token,
                       status=token.status)


def token_timeout():
    token = request.args.get('_t_')
    utils.mark_token_status(token, 'expired')
    return jsonify(msg="Token has been marked as expired.")
