import logging
import json
import logging
from enum import Enum
from time import sleep

import base58
import event_chain.protos as protos
import requests
from event_chain.config.config import APP_ADDR
from event_chain.config.config import APP_PK
from event_chain.config.config import APP_SK
from event_chain.config.config import ARC
from flask import flash
from flask import Response
from flask import session
from google.protobuf.any_pb2 import Any
from google.protobuf.timestamp_pb2 import Timestamp

from forge_sdk import utils as forge_utils
from event_chain import protos

logger = logging.getLogger('ec-util')


def get_proto(name):
    try:
        proto = getattr(protos, name)
        return proto
    except Exception:
        logger.error(f'proto {name} does not exist in protos.')
        return None


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(
                "Error in the {} field - {}".format(
                    getattr(form, field).label.text,
                    error), 'error',
            )

def gen_did_url(url, action):
    params = {
        'appPk': APP_PK,
        'appDid': 'did:abt:' + APP_ADDR,
        'action': action,
        'url': url,
    }
    r = requests.Request('GET', ARC, params=params).prepare()
    logger.debug(
        "callback url for DID call. {}".format(
            url,
        ),
    )
    return r.url
