from flask_jwt_extended import (
    create_access_token
)

from forge_symposia.server import models
from forge_symposia.server import utils
from forge_symposia.server.app import sql_db
from forge_symposia.server.endpoints.lib import auth_component


def get_handler(**args):
    return {
        'request_type': 'profile',
        'workflow': 'get-profile',
        'items':["fullName", "email"],
    }


def get_exist_user(did):
    return models.DBUser.query.filter_by(did=did).first()


def create_or_update_user(did, name, email):
    user = get_exist_user(did)
    if user:
        user.name = name
        user.email = email
    else:
        new_user = models.DBUser(did=did, name=name, email=email)
        sql_db.session.add(new_user)

    sql_db.session.commit()


def post_handler(**args):
    wallet_res = args.get('wallet_res')
    did = wallet_res.get_did()

    create_or_update_user(did=did,
                          name=wallet_res.requested_claim.get(
                                'fullName'),
                          email=wallet_res.requested_claim.get(
                                  'email'))

    session_token = create_access_token(identity=did)

    utils.mark_token_status(args.get('token'), 'succeed', session_token)

    return {'status': 0}

login = auth_component.create('login', get_handler, post_handler)