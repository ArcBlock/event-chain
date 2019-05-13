import unittest
import uuid
from time import sleep

from forge_sdk import rpc

from event_chain.application import controllers
from event_chain.application import models


class SimpeFlowTest(unittest.TestCase):

    def setUp(self):
        self.alice = rpc.create_wallet(moniker='lily1', passphrase='abc123')
        self.mike = rpc.create_wallet(moniker='rose1', passphrase='abc123')

    def test_all(self):
        general_factory_params = {
            'title': 'Jay Chou Concerts',
            'price': 10,
            'limit': 20,
            'start_time': '2019/09/27 9pm',
            'end_time': '2019/09/27 11pm',
            'location': 'Las Vegas Hall',
            'img_url': 'http://img.com',
            'description': 'test_description:' + str(uuid.uuid1()),
        }

        event_address = controllers.create_event_general(
                wallet=self.alice.wallet,
                **general_factory_params)
        print('alice', self.alice.wallet.address)
        sleep(5)

        event = models.EventState(rpc.get_single_asset_state(event_address))
        print('issuer', event.issuer)
        assert event.issuer == self.alice.wallet.address

        assert event.limit == 20
        assert event.title == 'Jay Chou Concerts'

        tickets = controllers.buy_tickets_general(event_address, 2,
                                                  self.mike.wallet)

        print('tickets', tickets)

        assert len(tickets) == 2

        sleep(5)
        for ticket in tickets:
            res = rpc.get_single_asset_state(ticket)
            assert res.issuer == self.alice.wallet.address
            assert res.owner == self.mike.wallet.address
