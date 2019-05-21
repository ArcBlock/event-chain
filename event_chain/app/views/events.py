import logging

import requests
from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from forge_sdk import utils as forge_utils

from event_chain.app import controllers
from event_chain.app import models
from event_chain.app import utils
from event_chain.app.forms.event import EventForm
from event_chain.app.models import sql
from event_chain.config import config
from event_chain.config.config import APP_ADDR
from event_chain.config.config import APP_PK
from event_chain.config.config import ARC
from event_chain.config.config import SERVER_ADDRESS

events = Blueprint(
        'events',
        __name__,
        template_folder='templates',
)

logger = logging.getLogger('view-event')


def to_price(biguint):
    return forge_utils.unit_to_token(forge_utils.biguint_to_int(biguint))


@events.route("/all", methods=['GET', 'POST'])
def all():
    def list_events():
        asset_factories = sql.AssetState.query.filter_by(
                moniker='general_event').all()
        addr_list = [factory.address for factory in asset_factories]
        event_states = []
        for addr in addr_list:
            state = models.get_event_factory(addr)
            if state:
                event_states.append(state)
        return event_states

    all_events = list_events()
    event_lists = utils.chunks(all_events, 3)

    return render_template(
            'events/event_list.html', event_lists=event_lists,
            session=session, number=len(all_events), to_price=to_price
    )


@events.route("/detail/<address>", methods=['GET', 'POST'])
def detail(address):
    error = utils.verify_event(address)
    if error:
        return error
    forge_web = 'http://{0}:{1}/node/explorer/txs/'.format(
            config.app_host, config.forge_port
    )

    event = models.get_event_factory(address)
    host = models.get_participant_state(event.owner)
    form = EventForm()
    if is_loggedin():
        url = gen_mobile_url(address)
        consume_url = gen_consume_url(address)

        txs = controllers.list_acquire_asset_txs(address)
        num_txs = len(txs)
        tx_lists = utils.chunks(txs, 3)
        logger.debug('forgeweb:{}'.format(forge_web))
        return render_template(
                'events/event_details.html', **locals(),
                to_display_time=utils.to_display_time,
                shorten_hash=utils.shorten_hash,
                to_short_time=utils.to_short_time,
                to_price=to_price
        )
    return redirect(url_for('admin.login'))


@events.route("/create", methods=['GET', 'POST'])
def create():
    if not session.get('user'):
        return redirect(url_for('admin.login'))
    utils.refresh_token()
    form = EventForm()
    if form.validate_on_submit():
        if request.method == "POST":
            event_address = controllers.create_event_general(
                    user=session.get('user'),
                    title=form.title.data,
                    limit=form.total.data,
                    description=form.description.data,
                    start_time=form.start_time.data.strftime("%a, %b %d, %Y"),
                    end_time=form.end_time.data.strftime("%a, %b %d, %Y"),
                    price=form.ticket_price.data,
                    location=form.location.data,
                    img_url=form.img_url.data,
                    details=form.details.data,
                    wallet=session.get('user').get_wallet(),
                    token=session.get('user').token,
            )
            if event_address:
                logger.info(f'Event {event_address} has been created.')

            else:
                logger.error(f'Error in creating event.')
            return redirect(url_for('events.all'))
    else:
        logger.error(form.errors)
        utils.flash_errors(form)
    return render_template('events/event_create.html', form=form)


def is_loggedin():
    if session.get('user'):
        return True
    else:
        return redirect('/login')


def gen_consume_url(event_address):
    url = SERVER_ADDRESS + url_for(
            'api_mobile.require_asset', event_address=event_address),
    return utils.gen_did_url(url, 'RequestAuth')


def gen_mobile_url(event_address):
    params = {
        'appPk': APP_PK,
        'appDid': 'did:abt:' + APP_ADDR,
        'action': 'requestAuth',
        'url': SERVER_ADDRESS + url_for(
                'api_mobile.buy_ticket', event_address=event_address),
    }
    r = requests.Request('GET', ARC, params=params).prepare()
    return r.url
