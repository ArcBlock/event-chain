import requests
from forge_sdk import utils as forge_utils, protos as forge_protos, ForgeConn
import json
from time import sleep
import logging

forge= ForgeConn('127.0.0.1:27210')
forge_rpc = forge.rpc


user = forge_rpc.create_wallet(moniker='tester', passphrase='abcd1234').wallet

event = 'zjdkjCT3sS7LfpqhzTTSxKtAZfAogbeSWKAB'

buy_url = f'http://10.1.10.176:5000/api/did/buy-ticket/auth/event_address={event}&_t_=123'
require_asset_url = f'http://10.1.10.176:5000/api/mobile/require-asset/{event}'
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

    consume_url = f'http://10.1.10.177:5000/api/mobile/consume/{ticket_address}'

    origin = get_origin(middle_user_info)
    tx = forge_utils.parse_to_proto(forge_utils.multibase_b58decode(origin),
                                    forge_protos.Transaction)
    signature = forge_rpc.sign_tx(user, tx)

    data = send_back_signature(middle_user_info, user.address, signature)
    r = requests.post(url=consume_url, data=json.dumps(data))
    return r.json()


def full_flow():
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


if __name__ == '__main__':
    res ={"appPk": "zFzpKEjhxDDjk8e3adCy3hoaR6ToyL3UzWtF4z8BYtPgc", "authInfo": "eyJhbGciOiAiRWQyNTUxOSIsICJ0eXAiOiAiSldUIn0.eyJpc3MiOiAiZGlkOmFidDp6MWdLOWplTnk0d2pOTkFBTjFBMmFuWG1VRGpKYUpDdmdHdSIsICJpYXQiOiAxNTYyMTI3OTQ0LCAibmJmIjogMTU2MjEyNzk0NCwgImV4cCI6IDE1NjIxMjk3NDQsICJ1cmwiOiAiaHR0cDovLzEwLjEuMTAuMTc2OjUwMDAvYXBpL2RpZC9jb25zdW1lX3RpY2tldC9jb25zdW1lP190Xz00NzNmYTBhMjMwYjNmMmExJnRpY2tldF9hZGRyZXNzPXpqZHRqcTM2b2JoWTFQMUhQVjMyd0h2dzFFeEtRRDVGeXNkbiIsICJhY3Rpb24iOiAicmVzcG9uc2VBdXRoIiwgImFwcEluZm8iOiB7ImNoYWluSG9zdCI6ICJodHRwOi8vMTAuMS4xMC4xNzY6ODIxMS9hcGkiLCAiY2hhaW5JZCI6ICJmb3JnZSIsICJjaGFpblZlcnNpb24iOiAiMC4yOC4wIiwgImNoYWluX3Rva2VuIjogIlRCQSIsICJkZWNpbWFscyI6IG51bGwsICJkZXNjcmlwdGlvbiI6ICJmb3JnZS1weXRob24tYXBwIiwgImljb24iOiAiaHR0cDovL2V2ZW50Y2hhaW4uYXJjYmxvY2suY286NTAwMC9zdGF0aWMvaW1hZ2VzL2V2ZW50Y2hhaW5faF8yLnBuZyIsICJuYW1lIjogImZvcmdlLXB5dGhvbi1hcHAiLCAic3VidGl0bGUiOiAiVGhpcyBpcyBhIGRlY2VudHJhbGl6ZWQgYXBwbGljYXRpb24ifSwgInJlcXVlc3RlZENsYWltcyI6IFt7InR5cGUiOiAic2lnbmF0dXJlIiwgImRhdGEiOiAiekZESmNLRUpHUFM5WEVGQWZ4cDdYd0Q0UUoyNjVMUmNkTU1aOG1zNUZETVdFIiwgIm1ldGEiOiB7ImRlc2NyaXB0aW9uIjogIkNvbmZpcm0gdG8gdXNlIHRoZSB0aWNrZXQuIn0sICJtZXRob2QiOiAic2hhMyIsICJvcmlnaW4iOiAiekpCSkNXV3pTWVpTVkh5MkVYaXY4dWk1NzM5R0x2QnU3OTVORmdadnhtVFhHWnF0UExyRVlzRkU0YlpNbml3aFBtM0UzQkI5eE45akVVd2tEeWFrYWI5M1R0SFBGWk44Y2FxQll4OFIyOFVyTm90MXZ2Y0ZuVDhOQU13RlVvTXpXWm16dFVGb1cxbVl3aEwyU0ZRZ25ZTlFoVDlIQ0xlR3JrS3ZaOUdxc0hLNTVqNFAxVEZuOTJ5ZURYNWllcENGY1ZpNHZYdTNERlNFM3ZaeVljeUI0bUs3RVVHNFlYeUhvS3Bua05tUVg1cUhxQXlOUGNkczNiZGNWQmtVa0F3bmJVWldzeTJxb0Q2bWNWYTQxaXBab3podnVYTUNHZHM2YlBydVJyRDZNNTdEdTlnWmF5bkJ6SDFYRm5MeVdHNER3QkhGTnFjaG85aDY0QnhCTUpkaDZCR005dXUyWVZjZlJhOGlRZkFobnpKNEZIWE45NHk1TENCejhjb3J5eFl0UW1Fc0pWbkRGNTdMTDR3clVZWGlrSFRwcXlIZDl4VGJMNnc1M1BpaHFTTVpGZUxNZXVhdVB2TENiWDF6azVFcTdyMmhqb0RRcFEifV0sICJ3b3JrZmxvdyI6IHsiZGVzY3JpcHRpb24iOiAidXNlLXRpY2tldCJ9fQ.ZWHCAM3ERqfzocBSssnV3VPiqnWhGy2jjjDMSWDPZwZIsuCvWPnHBLyJxpuRaEnukVaTzTJCflBr0YemN1YPAg"}
    middle = res.get('authInfo').split('.')[1]

    send_require_asset_post(middle, ticket_address)
    logging.info('success: require asset post')

