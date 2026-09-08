import unittest
from unittest.mock import Mock

from omnidimension import Client


def make_client():
    client = Client('x' * 12)
    client.request = Mock(return_value={"status": 200, "json": {}})
    return client


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.client = make_client()

    def test_carrier_omitted_by_default(self):
        self.client.phone_number.search(region="IN")
        params = self.client.request.call_args.kwargs['params']
        self.assertNotIn('carrier', params)

    def test_carrier_forwarded_when_given(self):
        self.client.phone_number.search(region="IN", carrier="carrier-1")
        params = self.client.request.call_args.kwargs['params']
        self.assertEqual(params['carrier'], 'carrier-1')

    def test_positional_call_still_works(self):
        # region, pattern, page, limit, user_id positions must not shift.
        self.client.phone_number.search("IN", "80", 1, 20, None)
        params = self.client.request.call_args.kwargs['params']
        self.assertEqual(params['pattern'], '80')
        self.assertNotIn('carrier', params)


class TestPurchase(unittest.TestCase):
    def setUp(self):
        self.client = make_client()

    def test_carrier_forwarded_when_given(self):
        self.client.phone_number.purchase(
            region="IN", phone_number="+911234567890", carrier="carrier-2-new")
        body = self.client.request.call_args.kwargs['json_data']
        self.assertEqual(body['carrier'], 'carrier-2-new')

    def test_carrier_omitted_by_default(self):
        self.client.phone_number.purchase(region="IN", phone_number="+911234567890")
        body = self.client.request.call_args.kwargs['json_data']
        self.assertNotIn('carrier', body)


if __name__ == '__main__':
    unittest.main()
