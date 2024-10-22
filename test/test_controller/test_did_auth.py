import json
import unittest

from forge_sdk import protos
from forge_sdk import did

from forge_sdk import utils as forge_utils


class AuthRequestTest(unittest.TestCase):

    def setUp(self):
        args = {
            'from': 'z1bdvuibh8L9wG8Re5CZmyzrMYo7rjrV3i7',
            'nonce': 1,
            'pk': b'fakepk',
        }
        self.sample_tx = protos.Transaction(**args)

    def test_require_multisig(self):
        user_did = "z1bdvuibh8L9wG8Re5CZmyzrMYo7rjrV3i7"
        args = {
            'user_did': user_did,
            'tx': self.sample_tx,
            'url': 'http: // sample_url',
            'description': 'this is a test',
            'workflow': 'work-flow-test',
            'action': 'requestAuth'
        }

        response = did.require_sig(**args)

        body = json.loads(forge_utils.multibase_b64decode(
            json.loads(response).get('authInfo').split('.')[1]))

        assert (body.get('url') == 'http: // sample_url')
        assert(body.get('action') == 'requestAuth')
