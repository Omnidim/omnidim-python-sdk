import unittest
from unittest.mock import Mock

from omnidimension import Client


def make_client():
    client = Client('x' * 12)
    client.request = Mock(return_value={"status": 200, "json": {}})
    return client


class TestListClonedVoices(unittest.TestCase):
    def setUp(self):
        self.client = make_client()

    def test_no_filters_send_no_params(self):
        self.client.voices.list_cloned_voices()
        params = self.client.request.call_args.kwargs['params']
        self.assertEqual(params, {})

    def test_forwards_limit_and_cursor(self):
        self.client.voices.list_cloned_voices(limit=10, cursor="abc")
        params = self.client.request.call_args.kwargs['params']
        self.assertEqual(params, {'limit': 10, 'cursor': 'abc'})


class TestCreateClonedVoice(unittest.TestCase):
    def setUp(self):
        self.client = make_client()

    def test_sends_required_fields(self):
        self.client.voices.create_cloned_voice("My voice", "https://x/sample.wav", True)
        body = self.client.request.call_args.kwargs['json_data']
        self.assertEqual(body, {
            'name': 'My voice',
            'clip': 'https://x/sample.wav',
            'consent': True,
        })

    def test_extra_fields_land_in_the_body(self):
        self.client.voices.create_cloned_voice("n", "c", True, language="en")
        body = self.client.request.call_args.kwargs['json_data']
        self.assertEqual(body['language'], 'en')

    def test_idempotency_key_only_when_given(self):
        self.client.voices.create_cloned_voice("n", "c", True)
        self.assertIsNone(self.client.request.call_args.kwargs['headers'])

        self.client.voices.create_cloned_voice("n", "c", True, idempotency_key="k-123")
        headers = self.client.request.call_args.kwargs['headers']
        self.assertEqual(headers['Idempotency-Key'], 'k-123')


class TestClonedVoiceById(unittest.TestCase):
    def setUp(self):
        self.client = make_client()

    def test_get_uses_voice_id(self):
        self.client.voices.get_cloned_voice(42)
        method, path = self.client.request.call_args.args
        self.assertEqual((method, path), ("GET", "voices/42"))

    def test_update_sends_fields_to_the_patch(self):
        self.client.voices.update_cloned_voice(42, name="Renamed")
        method, path = self.client.request.call_args.args
        body = self.client.request.call_args.kwargs['json_data']
        self.assertEqual((method, path), ("PATCH", "voices/42"))
        self.assertEqual(body, {'name': 'Renamed'})

    def test_delete_uses_voice_id(self):
        self.client.voices.delete_cloned_voice(42)
        method, path = self.client.request.call_args.args
        self.assertEqual((method, path), ("DELETE", "voices/42"))

    def test_sample_paths(self):
        self.client.voices.get_cloned_voice_sample(42)
        self.assertEqual(self.client.request.call_args.args, ("GET", "voices/42/sample"))

        self.client.voices.regenerate_cloned_voice_sample(42)
        self.assertEqual(self.client.request.call_args.args, ("POST", "voices/42/sample"))


if __name__ == '__main__':
    unittest.main()
