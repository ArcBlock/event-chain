import logging
import json
import logging
import uuid

from flask import Blueprint
from flask import Response
from flask import request
from flask import url_for
from forge_sdk import rpc as forge_rpc, utils as forge_utils

from event_chain import protos
from event_chain.app import controllers
from event_chain.app import models
from event_chain.app import utils

logger = logging.getLogger('apis-lib')


def parse_wallet_from_request(request):
    pk = request.args.get('userPk')
    did = request.args.get('userDid')
    logger.debug(f'userDid: {did}')

    return models.UserInfo(pk=pk, did=did)


def parse_request_get(request, name):
    logger.debug(f"Receives get request for {name}")
    user_info = parse_wallet_from_request(request)
    return user_info


def parse_request_post(request, name):
    logger.debug(f"Receives post request for {name}")
    try:
        req_data = request.get_data(as_text=True)
        logger.debug("Receives data from wallet {}".format(req_data))
        wallet_response = models.WalletResponse(json.loads(req_data))
    except Exception as e:
        logger.error(e, exc_info=True)
    return wallet_response


def ok(data):
    js = json.dumps(data)
    logger.debug('success response: {}'.format(str(js)))
    return Response(js, status=200, mimetype='application/json')

def error(msg):
    error = json.dumps({'error': msg})
    return Response(error, status=400, mimetype='application/json')