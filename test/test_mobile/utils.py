from forge_sdk import utils as forge_utils, protos as forge_protos
import json


def parse_response(res):
    auth_info = res.get('authInfo')
    middle = auth_info.split('.')[1]
    res = forge_utils.multibase_b64decode(middle).decode()
    return json.loads(res)

def parse_origin_tx(parsed, protobuf=None):
    origin = parsed.get('requestedClaims')[0].get('origin')
    tx = forge_utils.parse_to_proto(forge_utils.multibase_b58decode(origin),
                                    forge_protos.Transaction)
    if protobuf:
        itx = forge_utils.parse_to_proto(tx.itx.value,
                                     protobuf)
        return tx, itx
    else:
        return tx, None
