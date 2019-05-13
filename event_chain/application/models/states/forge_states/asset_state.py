class AssetState:
    def __init__(self, asset_state):
        self.address = asset_state.address
        self.owner = asset_state.owner
        self.moniker = asset_state.moniker
        self.readonly = asset_state.readonly
        self.transferrable = asset_state.transferrable
        self.ttl = asset_state.ttl
        self.consumed_time = asset_state.consumed_time
        self.issuer = asset_state.issuer
        self.context = asset_state.context
        self.stake = asset_state.stake
        self.data = asset_state.data
