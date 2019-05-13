
from forge_sdk import protos, utils as forge_utils

from event_chain.application.models.states.forge_states.asset_state import AssetState


class AssetFactoryState(AssetState):
    def __init__(self, asset_state):
        super().__init__(asset_state)

        state = forge_utils.parse_to_proto(asset_state.data.value,
                                           protos.AssetFactoryState)
        self.description = state.description
        self.limit = state.limit
        self.price = state.price
        self.template = state.template
        self.allowed_spec_args = state.allowed_spec_args
        self.asset_name = state.asset_name
        self.attributes = state.attributes
        self.num_created = state.num_created
        self.data = state.data
