import unittest
from unittest.mock import Mock, patch

from omnidimension import Client


def sent_headers(**kwargs):
    resp = Mock(status_code=200, text='{}')
    resp.json.return_value = {}
    resp.raise_for_status.return_value = None
    with patch('requests.request', return_value=resp) as req:
        Client('x' * 12).request('GET', '/agents', **kwargs)
    return req.call_args.kwargs['headers']


class TestUserAgent(unittest.TestCase):
    def test_sdk_identifies_itself(self):
        self.assertRegex(sent_headers()['User-Agent'], r'^OmniDimension-python-sdk/\S+$')

    def test_caller_can_override(self):
        self.assertEqual(sent_headers(headers={'User-Agent': 'mine'})['User-Agent'], 'mine')


if __name__ == '__main__':
    unittest.main()
