# flake8: noqa




def get_event_factory(address):
    state = forge_rpc.get_single_asset_state(address)
    return EventState(state)
