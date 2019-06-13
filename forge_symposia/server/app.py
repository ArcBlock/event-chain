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

app = Eve()
jwt = JWTManager(app)
sql_db = SQLAlchemy(app)
forge_rpc = forge.rpc


def register_blueprints(application):
    from forge_symposia.server import endpoints as ep
    application.register_blueprint(ep.login)
    application.register_blueprint(ep.checkin)
    application.register_blueprint(ep.payment)


@app.before_request
def before_request():
    g.logger = logging.getLogger('app')
    g.logger.setLevel(level=logging.DEBUG)


@app.route("/api/session", methods=['GET', 'POST'])
@jwt_required
def session():
    did = get_jwt_identity()
    res = requests.get(url=utils.server_url(f'/user/{did}'))
    if res.status_code == 200:
        data = res.json()
        return jsonify(user={
            'email': data.get('email'),
            'mobile': data.get('mobile', ''),
            'did': data.get('did'),
            'name': data.get('name'),
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


@app.route("/list_events", methods=['GET'])
def list_event():
    all_events = controllers.list_events()
    # event_lists = utils.chunks(all_events, 3)

    return jsonify(all_events)


@app.route("/detail/<address>", methods=['GET'])
def event_detail(address):
    event = controllers.get_response_event(address)
    return jsonify(vars(event))


@app.route("/user/<address>", methods=['GET'])
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


if __name__ == '__main__':
    register_blueprints(app)
    app.run(host='0.0.0.0', debug=True)
