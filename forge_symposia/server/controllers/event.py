import json
import logging
from datetime import datetime

import requests
from forge_sdk import utils as forge_utils

from forge_symposia.server import protos, utils
from forge_symposia.server.controllers import lib
from forge_symposia.server.forge import forge

logger = logging.getLogger('controller-event')


def parse_date(str_date):
    logger.debug(str_date)
    data = str_date.split('/')
    return datetime(
            int(data[0]),
            int(data[1]),
            int(data[2]),
    )


def list_events():
    res = requests.get(
            utils.server_url('/events?where={"moniker":"general_event"}'))

    addr_list = [factory.get('address') for factory in res.json().get("_items")]

    events = [lib.get_response_event(addr) for addr in addr_list]
    res = [vars(e) for e in events if e.num_created < e.limit]
    return res


def create_event_general(wallet, token=None, **kwargs):
    template = json.dumps({
        'id': '{{ id }}',
        'title': kwargs.get('title'),
        'start_time': kwargs.get('start_time'),
        'end_time': kwargs.get('end_time'),
        'location': kwargs.get('location'),
        'img_url': kwargs.get('img_url')
    })

    if not forge.rpc.is_template_match_asset(template,
                                             utils.get_proto('GeneralTicket')):
        return

    factory = forge.rpc.build_asset_factory(
            allowed_spec_args=['id'],
            asset_name='GeneralTicket',
            template=template,
            type_url='ec:s:event_info',
            data_value=protos.EventInfo(details=kwargs.get('details'),
                                        consume_asset_tx=lib.gen_consume_tx(
                                            wallet,
                                            token)),
            **kwargs,
    )

    res, event_address = forge.rpc.create_asset_factory('general_event',
                                                        factory,
                                                        wallet,
                                                        token)
    if forge_utils.is_response_ok(res):
        logger.debug(f'Event hash was received: {res.hash}')
        logger.info(f'Event address: {event_address}')
        return event_address
    else:
        logger.error(f'Event hash was not generated.')
        return None

