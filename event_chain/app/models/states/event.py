import json

from event_chain.app.models.states.forge_states import \
    AssetFactoryState
from event_chain import protos
from forge_sdk import protos as forge_protos, rpc as forge_rpc, utils as forge_utils
import logging

logger = logging.getLogger('state-event')


class EventState(AssetFactoryState):
    def __init__(self, state):
        super().__init__(state)
        template = json.loads(self.template)
        self.title = template.get('title')
        self.start_time = template.get('start_time')
        self.end_time = template.get('end_time')
        self.location = template.get('location')
        self.img_url = template.get('img_url')

        event_info = forge_utils.parse_to_proto(self.data.value,
                                                protos.EventInfo)
        self.details = event_info.details
        self.consume_tx = forge_utils.parse_to_proto(event_info.consume_asset_tx,
                                                     forge_protos.Transaction)


