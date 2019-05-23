import logging

from forge_sdk import rpc as forge_rpc
from forge_sdk import utils as forge_utils, protos as forge_protos

from event_chain.app.models.states.account import ParticipantAccountState

logger = logging.getLogger('model-admin')


class User:
    def __init__(self, **kwargs):
        self.passphrase = kwargs.get('passphrase')
        self.address = kwargs.get('address')
        self.moniker = kwargs.get('moniker')

        self.wallet = Wallet(pk=kwargs.get('pk'),
                             address=self.address,
                             token=kwargs.get('token'),
                             sk=kwargs.get('sk'))

    def get_wallet(self):
        return self.wallet.to_wallet_info()

    def poke(self):
        res = forge_rpc.poke(wallet=self.get_wallet(),
                             token=self.wallet.token)

        if forge_utils.is_response_ok(res):
            logger.info(f'Poke successfully.hash: {res.hash}')


class Wallet:
    def __init__(self, pk, address=None, sk=None, token=None, did=None):
        self.address = address
        self.pk = pk if isinstance(pk,
                                   bytes) else forge_utils.multibase_b58decode(pk)
        self.sk = sk
        self.token = token
        self.did = did

        if self.did:
            self.address = self.did.split(":")[-1]

    def to_wallet_info(self):
        return forge_protos.WalletInfo(
                pk=self.pk,
                sk=self.sk,
                address=self.address
        )


def get_participant_state(address):
    state = forge_rpc.get_single_account_state(address)
    if state:
        return ParticipantAccountState(state)
