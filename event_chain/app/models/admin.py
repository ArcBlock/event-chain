import logging

from forge_sdk import rpc as forge_rpc, protos as forge_protos

from event_chain import protos
from forge_sdk import utils as forge_utils
from event_chain.app.models.states.account import ParticipantAccountState

logger = logging.getLogger('model-admin')


class User:
    def __init__(self, moniker, passphrase, address=None):
        self.moniker = moniker
        self.passphrase = passphrase
        if address:
            self.wallet, self.token = self.__load_wallet(address, passphrase)
            self.address = address
        else:
            logger.debug("creating wallet for {}".format(moniker))
            self.address, self.wallet, self.token = self.__init_wallet()

    def get_wallet(self):
        wallet = forge_protos.WalletInfo()
        wallet.ParseFromString(self.wallet)
        return wallet

    def __init_wallet(self):
        res = forge_rpc.create_wallet(
            moniker=self.moniker,
            passphrase=self.passphrase,
        )
        if res.code != 0:
            logger.error("Creating wallet failed!")
            logger.error(res)
        return res.wallet.address, res.wallet.SerializeToString(), res.token

    def __load_wallet(self, address, passphrase):
        res = forge_rpc.load_wallet(address, passphrase)
        if res.code != 0:
            logger.error(
                "Reloading wallet failed! Please check your passphrase.",
            )
            logger.error(res)
        return res.wallet.SerializeToString(), res.token

    def poke(self):
        res = forge_rpc.poke(wallet=self.get_wallet(),
                             token=self.token)

        if res.code != 0:
            logger.error("Poke Failed.")
            logger.error(res)
        else:
            logger.debug('Poke successfully.hash: {}'.format(res.hash))


class Wallet:
    def __init__(self, pk, address=None, sk=None, token=None, did=None):
        self.address = address
        self.pk = forge_utils.multibase_b58decode(pk)
        self.sk = sk
        self.token = token
        self.did = did

        if self.did:
            self.address = self.did.split(":")[2]


def get_participant_state(address):
    state = forge_rpc.get_single_account_state(address)
    if state:
        return ParticipantAccountState(state)
