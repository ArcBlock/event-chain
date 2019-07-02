import logging

from forge_sdk import did as forge_did

from forge_symposia.server import env
from forge_symposia.server import protos
from forge_symposia.server import models

logger = logging.getLogger('utils')


def mark_token_status(token, status, session_token=None):
    from forge_symposia.server.app import sql_db as db
    new_token = models.DBToken(token=token,
                               status=status,
                               session_token=session_token)
    if not status == 'created':
        db.session.delete(models.DBToken.query.filter_by(token=token).first())
    db.session.add(new_token)
    db.session.commit()

def check_token_status(token):
    return models.DBToken.query.filter_by(token=token).first()

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
