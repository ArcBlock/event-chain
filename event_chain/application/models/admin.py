import logging

from forge_sdk import rpc as forge_rpc

from event_chain import protos

logger = logging.getLogger('model-admin')


class User:
    def __init__(self, moniker, passphrase, address=None):
        self.moniker = moniker
        self.passphrase = passphrase
        if address:
            logger.debug("Loading wallet for {}".format(moniker))
            self.wallet, self.token = self.__load_wallet(address, passphrase)
            self.address = address
        else:
            logger.debug("creating wallet for {}".format(moniker))
            self.address, self.wallet, self.token = self.__init_wallet()
        logger.debug("wallet: {}".format(self.wallet))
        logger.debug("token: {}".format(self.token))
        logger.debug("address: {}".format(self.address))

    def get_wallet(self):
        wallet = protos.WalletInfo()
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
    def __init__(self, address, pk, sk=None, token=None, did=None):
        self.address = address
        self.pk = pk
        self.sk = sk
        self.token = token
        self.did = did
