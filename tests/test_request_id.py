import unittest
from unittest.mock import Mock, patch

import requests

from omnidimension import Client
from omnidimension.client import APIError


def fail(headers=None, body=None, status=500):
    resp = Mock(status_code=status, headers=headers or {})
    resp.json.return_value = body if body is not None else {}
    if body is None:
        resp.json.side_effect = ValueError('no json')
    resp.raise_for_status.side_effect = requests.exceptions.HTTPError('boom', response=resp)
    with patch('requests.request', return_value=resp):
        with unittest.TestCase().assertRaises(APIError) as cm:
            Client('x' * 12).request('GET', '/agents')
    return cm.exception


class TestRequestId(unittest.TestCase):
    def test_from_header(self):
        e = fail(headers={'X-Request-Id': 'abc'}, body={'error': 'bad'})
        self.assertEqual(e.request_id, 'abc')
        self.assertIn('(request id: abc)', str(e))

    def test_from_body_request_id(self):
        self.assertEqual(fail(body={'error': 'bad', 'request_id': 'r1'}).request_id, 'r1')

    def test_from_body_ref(self):
        self.assertEqual(fail(body={'error': 'bad', 'ref': 'f9'}).request_id, 'f9')

    def test_absent_is_none_and_message_unchanged(self):
        e = fail(body={'error': 'bad'})
        self.assertIsNone(e.request_id)
        self.assertNotIn('request id', str(e))

    def test_non_json_body_still_reads_header(self):
        self.assertEqual(fail(headers={'X-Request-Id': 'h'}).request_id, 'h')


if __name__ == '__main__':
    unittest.main()
