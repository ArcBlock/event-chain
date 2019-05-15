import json

from event_chain.application.models.states.forge_states import \
    AssetFactoryState


class EventState(AssetFactoryState):
    def __init__(self, state):
        super().__init__(state)
        template = json.loads(self.template)
        self.title = template.get('title')
        self.start_time = template.get('start_time')
        self.end_time = template.get('end_time')
        self.location = template.get('location')
        self.img_url = template.get('img_url')
