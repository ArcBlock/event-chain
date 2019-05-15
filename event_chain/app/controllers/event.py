import logging
from datetime import datetime

from event_chain.app import models
import json

from forge_sdk import rpc as forge_rpc, utils as forge_utils
from event_chain.app import utils


logger = logging.getLogger('controller-event')


def parse_date(str_date):
    logger.debug(str_date)
    data = str_date.split('/')
    return datetime(
        int(data[0]),
        int(data[1]),
        int(data[2]),
    )


def create_event_general(wallet, token=None, **kwargs):
    template = json.dumps({
        'id': '{{ id }}',
        'title': kwargs.get('title'),
        'start_time': kwargs.get('start_time'),
        'end_time': kwargs.get('end_time'),
        'location': kwargs.get('location'),
        'img_url': kwargs.get('img_url')
    })

    if not forge_rpc.is_template_match_asset(template,
                                       utils.get_proto('GeneralTicket')):
        return

    factory = forge_rpc.build_asset_factory(
            allowed_spec_args=['id'],
            asset_name='GeneralTicket',
            template=template,
            type_url='ec:s:string',
            data_value=kwargs.get('details'),
            **kwargs,
    )

    res, event_address = forge_rpc.create_asset_factory('general_event', factory,
                                                  wallet,
                                                  token)
    if forge_utils.is_response_ok(res):
        logger.debug(f'Event hash was received: {res.hash}')
        logger.info(f'Event address: {event_address}')
        return event_address
    else:
        logger.error(f'Event hash was not generated.')
        return None


def verify_event_address(event_address):
    try:
        state = models.get_event_factory(event_address)
    except Exception:
        logger.error('exception in verifying event_address ')
        raise TypeError("{} is not an event address.".format(event_address))
    if not state:
        logger.error('Event {} does not exist.'.format(event_address))
        raise ValueError('Event {} does not exist'.format(event_address))


def get_tx_info(hash):
    info = forge_rpc.get_single_tx_info(hash)
    if info:
        return models.TransactionInfo(info)
