import logging

import requests
from eve import Eve
from flask import g, jsonify, make_response, request
from flask_jwt_extended import (JWTManager, get_jwt_identity, jwt_required)
from flask_sqlalchemy import SQLAlchemy
from forge_sdk import did as forge_did, protos as forge_protos

from forge_symposia.server import controllers
from forge_symposia.server import env
from forge_symposia.server import utils
from forge_symposia.server.forge import forge

from eve_sqlalchemy.validation import ValidatorSQL
from eve_sqlalchemy import SQL
from forge_symposia.server.models import Base, init_db
import pathlib
import os


app = Eve(validator=ValidatorSQL, data=SQL)
jwt = JWTManager(app)
forge_rpc = forge.rpc
db = app.data.driver
Base.metadata.bind = db.engine
db.Model = Base


def register_blueprints(application):
    from forge_symposia.server import endpoints as ep
    application.register_blueprint(ep.login)
    application.register_blueprint(ep.checkin)
    application.register_blueprint(ep.buy_ticket)
    application.register_blueprint(ep.consume_ticket)


@app.before_request
def before_request():
    g.logger = logging.getLogger('app')
    g.logger.setLevel(level=logging.DEBUG)

@app.route("/api/session", methods=['GET', 'POST'])
@jwt_required
def session():
    did = get_jwt_identity()
    user = controllers.get_user(did)
    if user:
        return jsonify(user={
            'email': user.email,
            'mobile': user.mobile,
            'did': user.did,
            'name': user.name,
        })
    else:
        return '{}'


@app.route("/api/payments", methods=['GET'])
@jwt_required
def payments():
    did = get_jwt_identity()
    res = forge_rpc.list_transactions(
            address_filter=forge_protos.AddressFilter(
                    sender=did.lstrip(forge_did.PREFIX),
                    receiver=env.APP_ADDR),
            type_filter=forge_protos.TypeFilter(types=['transfer']))
    if len(res.transactions) > 0:
        tx = next(tx for tx in res.transactions if tx.code == 0)
        if tx and tx.hash:
            return jsonify(hash=tx.hash)
    return make_response()


@app.route("/api/list_events", methods=['GET'])
def list_event():
    all_events = controllers.list_events()
    return jsonify(all_events)


@app.route("/api/detail/<address>", methods=['GET'])
def event_detail(address):
    event = controllers.get_response_event(address)
    return jsonify(vars(event))


@app.route("/api/user/<address>", methods=['GET'])
def user(address):
    type = request.args.get('type')
    if not type:
        return jsonify(error='Must provide a type parameter'), 400
    elif type == 'tickets':
        tickets = controllers.list_user_tickets(address)
        return jsonify(tickets)
    else:
        return jsonify(
                error=f"Server does not support '{type}'"), 400


@app.route("/api/list_tickets/<user_address>", methods=['GET'])
def list_tickets(user_address):
    user_address=user_address.lstrip(forge_did.PREFIX)
    tickets = controllers.list_user_tickets(user_address)
    res= utils.chunks(tickets, 3)
    return jsonify(res)


@app.route("/api/swap", methods=['POST'])
def swap():
    try:
        res = requests.post("http://localhost:8807/swap")
    except Exception:
        g.logger.error("Fail to connect to localhost:8807")
        return jsonify(error="no response from 8807/swap")
    id = res.json().get('id')
    if not id:
        g.logger.errorf("Response does not have a [id] field.")
    url = f"http://localhost:8807/swap/{id}"
    g.logger.debug(f'swap url: {url}')
    res = requests.get(url)
    return res


sql_db = init_db(app)

if __name__ == '__main__':
    register_blueprints(app)
    app.run(host='0.0.0.0', debug=True, threaded=True)
