import logging

import requests
from forge_sdk import did as forge_did

from forge_symposia.server import env
from forge_symposia.server import protos

logger = logging.getLogger('utils')


def mark_token_status(token, status=None, sessionToken=None):
    endpoint = server_url('/token')
    if status == 'created':
        return requests.post(url=endpoint,
                             data={'token': token,
                                   'status': 'created'})
    else:
        response = requests.get(url=f'{endpoint}/{token}')
        if not status:
            return response
        else:
            info = response.json()
            if not sessionToken:
                return requests.patch(url=f'{endpoint}/{info.get("_id")}',
                                      data={'status': status},
                                      headers={'If-Match': info.get('_etag')})
            else:
                return requests.patch(url=f'{endpoint}/{info.get("_id")}',
                                      data={'status': status,
                                            'sessionToken': sessionToken},
                                      headers={'If-Match': info.get('_etag')})


def server_url(endpoint):
    return env.SERVER_HOST + endpoint


def send_did_request(request_type, **kwargs):
    if request_type == "profile":
        return forge_did.require_profile(**kwargs)
    elif request_type == "signature":
        return forge_did.require_sig(**kwargs)
    elif request_type == "asset":
        return forge_did.require_asset(**kwargs)


def get_proto(name):
    try:
        proto = getattr(protos, name)
        return proto
    except Exception:
        logger.error(f'proto {name} does not exist in protos.')
        return None

def chunks(l, n):
    return [l[i:i + n] for i in range(0, len(l), n)]
