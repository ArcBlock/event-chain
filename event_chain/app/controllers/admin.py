import logging

from event_chain.app import models
from forge_sdk import rpc as forge_rpc, utils as forge_utils

logger = logging.getLogger('controller-admin')


def register_user(moniker, passphrase):
    res = forge_rpc.create_wallet(moniker=moniker,
                                  passphrase=passphrase)
    if forge_utils.is_response_ok(res):
        user = models.User(passphrase=passphrase,
                           moniker=moniker, token=res.token,
                           pk=res.wallet.pk, address=res.wallet.address)

        logger.info(f"User {moniker} created successfully!")
        user.poke()
        return user
    logger.error(f'Error in creating user {moniker}')


def load_user(passphrase, address):
    res = forge_rpc.load_wallet(passphrase=passphrase,
                                address=address)
    if forge_utils.is_response_ok(res):
        moniker = forge_rpc.get_single_account_state(address).moniker

        logger.info(f"User {address} loaded successfully!")
        return models.User(passphrase=passphrase,address=address,
                           moniker=moniker, token=res.token,
                           pk=res.wallet.pk)
    logger.error(f'Error in loading user {address}')
