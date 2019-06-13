import json
import logging
from datetime import datetime

from forge_sdk import protos as forge_protos, utils as forge_utils

from forge_symposia.server import models
from forge_symposia.server import protos, utils
from forge_symposia.server.app import forge
from forge_symposia.server.controllers import lib

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
    addr_list = [factory.address for factory in
                 models.DBAssetState.query.filter_by(
                         moniker='general_event').all()]

    events = [lib.get_response_event(addr) for addr in addr_list]
    res=[vars(e) for e in events if e.num_created < e.limit]
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
                                        consume_asset_tx=lib.gen_consume_tx(wallet,
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

# def verify_event_address(event_address):
#     try:
#         state = models.get_event_factory(event_address)
#     except Exception:
#         logger.error('exception in verifying event_address ')
#         raise TypeError("{} is not an event address.".format(event_address))
#     if not state:
#         logger.error('Event {} does not exist.'.format(event_address))
#         raise ValueError('Event {} does not exist'.format(event_address))


# def list_acquire_asset_txs(event_address):
#     tx_infos = [get_tx_info(h.hash) for h in sql.AcquireAssetTx.query.all()]
#
#     event_txs = []
#
#     for tx_info in tx_infos:
#         itx = forge_utils.parse_to_proto(tx_info.tx.itx.value,
#                                          forge_protos.AcquireAssetTx)
#         if itx.to == event_address:
#             event_txs.append(tx_info)
#     return event_txs


# def get_tx_info(hash):
#     info = forge_rpc.get_single_tx_info(hash)
#     if info:
#         return models.TransactionInfo(info)