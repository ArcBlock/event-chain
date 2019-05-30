import requests
from forge_sdk import rpc as forge_rpc, utils as forge_utils, protos as forge_protos
import json
from time import sleep
import logging


user = forge_rpc.create_wallet(moniker='tester', passphrase='abcd1234').wallet

event = 'zjdrUJQS4g889fJY5UGRvKqCdFktUCXVUAfd'

buy_url = f'http://localhost:5000/api/mobile/buy-ticket/{event}'
require_asset_url = f'http://localhost:5000/api/mobile/require-asset/{event}'
get_request_params = {
        'userPk': forge_utils.multibase_b58encode(user.pk),
        'userDid': 'did:abt:' + user.address,
    }
sleep(5)


def buy_ticket_get():
    r = requests.get(url=buy_url, params=get_request_params)
    return r.json()


def buy_ticket_post(middle_user_info):
    origin = get_origin(middle_user_info)
    tx = forge_utils.parse_to_proto(forge_utils.multibase_b58decode(origin),
                                    forge_protos.Transaction)

    signature = forge_rpc.sign_tx(user, tx)

    data = send_back_signature(middle_user_info, user.address, signature)
    r = requests.post(url=buy_url, data=json.dumps(data))
    return r.json()


def get_origin(request):
    decoded = forge_utils.multibase_b64decode(request).decode()
    origin = json.loads(decoded).get('requestedClaims')[0].get('origin')
    return origin


def send_back_signature(middle_req, did, signature=None):
    origin = get_origin(middle_req)
    signature=forge_utils.multibase_b58encode(signature) if signature else None

    requested_claim = {'did': did,
                       'origin': origin,
                       'sig': signature,
                       }

    user_info = {
        'requestedClaims': [requested_claim],
        'iss': 'did:abt:' + user.address,
    }
    data = {
        'userPk': forge_utils.multibase_b58encode(user.pk),
        'userInfo': 'placeholder.' + forge_utils.multibase_b64encode(
            json.dumps(user_info)) + '.placeholder'
    }
    return data


def send_require_asset_get():
    r = requests.get(url=require_asset_url, params=get_request_params)
    return r.json()


def send_require_asset_post(middle_user_info, ticket):
    data = send_back_signature(middle_user_info, ticket)
    r = requests.post(url=require_asset_url, data=json.dumps(data))
    return r.json()


def consume_asset(middle_user_info,ticket_address):

    consume_url = f'http://localhost:5000/api/mobile/consume/{ticket_address}'

    origin = get_origin(middle_user_info)
    tx = forge_utils.parse_to_proto(forge_utils.multibase_b58decode(origin),
                                    forge_protos.Transaction)
    signature = forge_rpc.sign_tx(user, tx)

    data = send_back_signature(middle_user_info, user.address, signature)
    r = requests.post(url=consume_url, data=json.dumps(data))
    return r.json()



if __name__ == '__main__':
    res = buy_ticket_get()
    middle = res.get('authInfo').split('.')[1]
    logging.info('success: buy ticket get')

    res = buy_ticket_post(middle)
    ticket_address = res.get('ticket')
    logging.info('success: buy ticket post')

    sleep(5)

    res = send_require_asset_get()
    middle = res.get('authInfo').split('.')[1]
    logging.info('success: require asset get')

    res = send_require_asset_post(middle, ticket_address)
    middle = res.get('authInfo').split('.')[1]
    logging.info('success: require asset post')

    res = consume_asset(middle, ticket_address)
    logging.info('success: consume asset post')

    print(res)

