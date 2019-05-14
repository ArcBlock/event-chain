import json
import logging

from forge_sdk import rpc, utils as forge_utils

from event_chain.application import utils

logger = logging.getLogger('ec-controller')


def create_event_general(wallet, token=None, **kwargs):
    template = json.dumps({
        'id': '{{ id }}',
        'title': kwargs.get('title'),
        'start_time': kwargs.get('start_time'),
        'end_time': kwargs.get('end_time'),
        'location': kwargs.get('location'),
        'img_url': kwargs.get('img_url')
    })

    if not rpc.is_template_match_asset(template,
                                       utils.get_proto('GeneralTicket')):
        return

    factory = rpc.build_asset_factory(
            allowed_spec_args=['id'],
            asset_name='GeneralTicket',
            template=template,
            type_url='ec:s:string',
            data_value=kwargs.get('details'),
            **kwargs,
    )

    res, event_address = rpc.create_asset_factory('general_event', factory, wallet,
                                                  token)
    if forge_utils.is_response_ok(res):
        logger.debug(f'Event hash was received: {res.hash}')
        logger.info(f'Event address: {event_address}')
        return event_address
    else:
        logger.error(f'Event hash was not generated.')
        return None
