import unittest
from unittest.mock import Mock

from omnidimension import Client


def make_client():
    client = Client('x' * 12)
    client.request = Mock(return_value={"status": 200, "json": {}})
    return client


class TestWhatsAppWire(unittest.TestCase):
    def setUp(self):
        self.client = make_client()

    def sent(self):
        return self.client.request.call_args

    def test_send_message_carries_the_idempotency_key_and_type_fields(self):
        self.client.whatsapp.send_message(7, "+15551234567", "text", "key-1",
                                          text={"body": "Hi"})
        call = self.sent()
        self.assertEqual(call.args[:2], ("POST", "whatsapp/messages"))
        self.assertEqual(call.kwargs['headers'], {'Idempotency-Key': 'key-1'})
        self.assertEqual(call.kwargs['json_data'], {
            'phone_number_id': 7, 'to': '+15551234567', 'type': 'text',
            'text': {'body': 'Hi'},
        })

    def test_launch_campaign_carries_the_idempotency_key(self):
        self.client.whatsapp.launch_campaign(42, "launch-42")
        call = self.sent()
        self.assertEqual(call.args[:2], ("POST", "whatsapp/campaigns/42/launch"))
        self.assertEqual(call.kwargs['headers'], {'Idempotency-Key': 'launch-42'})

    def test_list_messages_always_sends_the_conversation_and_drops_unset_filters(self):
        self.client.whatsapp.list_messages(9, limit=20)
        self.assertEqual(self.sent().kwargs['params'], {'conversation_id': 9, 'limit': 20})

    def test_upload_media_is_multipart_with_fields_beside_the_file(self):
        self.client.whatsapp.upload_media(7, "image", ("a.png", b"\x89PNG", "image/png"))
        call = self.sent()
        self.assertEqual(call.kwargs['data'], {'phone_number_id': 7, 'type': 'image'})
        self.assertEqual(call.kwargs['files'], {'file': ("a.png", b"\x89PNG", "image/png")})
        self.assertNotIn('json_data', call.kwargs)

    def test_campaign_contacts_send_a_list_as_the_body(self):
        contacts = [{'phone_number': '+15551234567'}, {'phone_number': '+15557654321'}]
        self.client.whatsapp.add_campaign_contacts(42, contacts)
        self.assertEqual(self.sent().kwargs['json_data'], contacts)

    def test_import_numbers_leaves_out_an_unset_app_secret(self):
        self.client.whatsapp.import_numbers("waba", "token", ["111"])
        self.assertEqual(self.sent().kwargs['json_data'], {
            'waba_id': 'waba', 'access_token': 'token', 'phone_number_ids': ['111'],
        })


class TestSimulationAdditions(unittest.TestCase):
    def setUp(self):
        self.client = make_client()

    def test_generate_scenarios_posts_the_count_to_the_agent(self):
        self.client.simulation.generate_scenarios(123, 5)
        call = self.client.request.call_args
        self.assertEqual(call.args[:2], ("POST", "agents/123/auto-scenarios"))
        self.assertEqual(call.kwargs['json_data'], {'number_of_scenarios': 5})

    def test_apply_enhanced_prompt_posts_to_the_simulation(self):
        self.client.simulation.apply_enhanced_prompt(456)
        self.assertEqual(self.client.request.call_args.args[:2],
                         ("POST", "simulations/456/apply-enhanced-prompt"))


if __name__ == '__main__':
    unittest.main()
