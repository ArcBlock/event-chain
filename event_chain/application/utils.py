import logging

from event_chain import protos

logger = logging.getLogger('ec-util')


def get_proto(name):
    try:
        proto = getattr(protos, name)
        return proto
    except Exception:
        logger.error(f'proto {name} does not exist in protos.')
        return None
