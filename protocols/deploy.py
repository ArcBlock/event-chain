import json
import os

from forge_sdk import ForgeConn, did, mcrypto, protos, utils
import logging

logger = logging.getLogger('deploy-script')

m_sk = os.environ.get('MODERATOR_SK')
m_pk = os.environ.get('MODERATOR_PK')

m_address='z11N3R6GZrNingR11Dub9EbVMJGgyZTJGMQB'

forge = ForgeConn('127.0.0.1:27210')
input = os.path.join(os.path.dirname(__file__), 'event_chain/event_chain/event_chain.itx.json')

def delcare_moderator():
    m_wallet = protos.WalletInfo(
            sk=utils.multibase_b64decode(m_sk),
            pk=utils.multibase_b64decode(m_pk),
            address=m_address
    )
    res = forge.rpc.declare(moniker='moderator',
                      wallet=m_wallet)

    if res.code == 0:
        logger.info("Moderator wallet created!")
        return m_wallet
    else:
        logger.error("Fail to declare moderator wallet.")

def deploy(m_wallet):
    with open (input) as f:
        raw = json.load(f).get('event_chain')
        logger.info("Protocol json loaded!")

        decoded = utils.multibase_b64decode(raw)
        itx = utils.parse_to_proto(decoded, protos.DeployProtocolTx)
        itx_hash = mcrypto.Hasher('sha3').hash(itx.SerializeToString())
        addr = did.AbtDid(role_type='tx', form='short').hash_to_did(itx_hash)
        itx.address = addr

        res=forge.rpc.send_itx(tx=itx, wallet=m_wallet, type_url='fg:t:deploy_protocol',
                               nonce=0)
        if res.code == 0:
            logger.info("event_chain tx deployed.")
        else:
            logger.error("fail to deploy event_chain tx.")
            logger.error(res)

if __name__=="__main__":
    m_wallet = delcare_moderator()
    deploy(m_wallet)