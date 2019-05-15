import event_chain.protos as protos
from event_chain.app import utils

from forge_sdk import utils as forge_utils


class ParticipantAccountState:

    def __init__(self, state):
        self.balance = state.balance
        self.nonce = state.nonce
        self.num_txs = state.num_txs
        self.address = state.address
        self.pk = state.pk
        self.type = state.type
        self.moniker = state.moniker
        self.issuer = state.issuer
        self.context = state.context
        self.migrated_to = state.migrated_to
        self.migrated_from = state.migrated_from
        self.num_assets = state.num_assets
        self.stake = state.stake
        self.pinned_files = state.pinned_files

        self.display_balance = forge_utils.bytes_to_int(
            self.balance.value) / 1e16
