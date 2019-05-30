import unittest

from forge_sdk import rpc

from event_chain.app import controllers


class EventControllerTest(unittest.TestCase):

    def setUp(self):
        self.general_factory_params = {
            'title': 'Jay Chou Concert',
            'price': 10,
            'limit': 20,
            'start_time': '2019/09/27 9pm',
            'end_time': '2019/09/27 11pm',
            'location': 'Las Vegas Hall',
            'img_url': 'http://img.com',
        }
        self.alice = rpc.create_wallet(moniker='alice', passphrase='abc123')

    def test_create_event_general(self):
        event_address = controllers.create_event_general(
                wallet=self.alice.wallet,
                **self.general_factory_params)
        assert event_address
