import unittest
from unittest.mock import Mock

from omnidimension import Client


def make_client():
    client = Client('x' * 12)
    client.request = Mock(return_value={"status": 200, "json": {}})
    return client


class TestKycRequirements(unittest.TestCase):
    def setUp(self):
        self.client = make_client()

    def test_carrier_omitted_by_default(self):
        self.client.reseller.kyc_requirements(region="IN")
        params = self.client.request.call_args.kwargs['params']
        self.assertNotIn('carrier', params)

    def test_carrier_forwarded_when_given(self):
        self.client.reseller.kyc_requirements(region="IN", carrier="carrier-1")
        params = self.client.request.call_args.kwargs['params']
        self.assertEqual(params['carrier'], 'carrier-1')

    def test_positional_call_still_works(self):
        self.client.reseller.kyc_requirements("IN")
        params = self.client.request.call_args.kwargs['params']
        self.assertEqual(params['region'], 'IN')
        self.assertNotIn('carrier', params)


class TestSubmitKycStep(unittest.TestCase):
    def setUp(self):
        self.client = make_client()

    def test_carrier_forwarded_when_given(self):
        self.client.reseller.submit_kyc_step(
            step="register", user_id=456, region="IN", carrier="carrier-1", full_name="Jane")
        body = self.client.request.call_args.kwargs['json_data']
        self.assertEqual(body['carrier'], 'carrier-1')
        self.assertEqual(body['full_name'], 'Jane')

    def test_carrier_omitted_by_default(self):
        self.client.reseller.submit_kyc_step(step="register", user_id=456, region="IN")
        body = self.client.request.call_args.kwargs['json_data']
        self.assertNotIn('carrier', body)

    def test_positional_call_still_works(self):
        # step, user_id, region positions must not shift; extra fields
        # still land in the body via **fields.
        self.client.reseller.submit_kyc_step("register", 456, "IN", full_name="Jane")
        body = self.client.request.call_args.kwargs['json_data']
        self.assertEqual(body['user_id'], 456)
        self.assertEqual(body['region'], 'IN')
        self.assertEqual(body['full_name'], 'Jane')
        self.assertNotIn('carrier', body)


if __name__ == '__main__':
    unittest.main()
