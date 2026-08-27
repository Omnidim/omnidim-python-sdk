import unittest
from unittest.mock import Mock

from omnidimension import Client


def make_client():
    client = Client('x' * 12)
    client.request = Mock(return_value={"status": 200, "json": {}})
    return client


class TestCreateBulkCalls(unittest.TestCase):
    def setUp(self):
        self.client = make_client()
        self.contacts = [{"phone_number": "+1234567890", "customer_name": "John"}]

    def test_backward_compatible_body(self):
        self.client.bulk_call.create_bulk_calls("Campaign", self.contacts, 42)
        self.client.request.assert_called_once_with(
            "POST", "calls/bulk_call/create", params=None, headers=None,
            json_data={
                'name': 'Campaign',
                'contact_list': self.contacts,
                'phone_number_id': 42,
                'is_scheduled': False,
                'timezone': 'UTC',
                'enabled_reschedule_call': False,
            })

    def test_new_keys_appear_when_given(self):
        conditions = [{"column": "status", "operator": "=", "value": "new"}]
        rotation = {"numbers": [{"phone_number_id": 7, "sequence": 1}], "strategy": "round_robin"}
        self.client.bulk_call.create_bulk_calls(
            "Campaign", self.contacts, 42,
            bot_id=9, save_as_draft=True, call_conditions=conditions,
            rotation=rotation, concurrent_call_limit=5)
        body = self.client.request.call_args.kwargs['json_data']
        self.assertEqual(body['bot_id'], 9)
        self.assertIs(body['save_as_draft'], True)
        self.assertEqual(body['call_conditions'], conditions)
        self.assertEqual(body['rotation'], rotation)
        self.assertEqual(body['concurrent_call_limit'], 5)

    def test_save_as_draft_false_omitted(self):
        self.client.bulk_call.create_bulk_calls("Campaign", self.contacts, 42, save_as_draft=False)
        body = self.client.request.call_args.kwargs['json_data']
        self.assertNotIn('save_as_draft', body)

    def test_invalid_concurrent_call_limit(self):
        with self.assertRaises(ValueError):
            self.client.bulk_call.create_bulk_calls(
                "Campaign", self.contacts, 42, concurrent_call_limit=0)


class TestAddContact(unittest.TestCase):
    def setUp(self):
        self.client = make_client()

    def test_minimal_body(self):
        self.client.bulk_call.add_contact(123, "+1234567890")
        self.client.request.assert_called_once_with(
            "POST", "calls/bulk_call/123/add_contact", params=None, headers=None,
            json_data={'to_number': '+1234567890'})

    def test_optional_fields(self):
        self.client.bulk_call.add_contact(
            123, "+1234567890", custom_variables={"name": "John"}, metadata={"source": "crm"})
        self.client.request.assert_called_once_with(
            "POST", "calls/bulk_call/123/add_contact", params=None, headers=None,
            json_data={'to_number': '+1234567890',
                       'custom_variables': {'name': 'John'},
                       'metadata': {'source': 'crm'}})

    def test_empty_to_number(self):
        with self.assertRaises(ValueError):
            self.client.bulk_call.add_contact(123, "")


class TestAddContacts(unittest.TestCase):
    def setUp(self):
        self.client = make_client()

    def test_body(self):
        contacts = [{"to_number": "+1234567890"}, {"to_number": "+1987654321"}]
        self.client.bulk_call.add_contacts(123, contacts)
        self.client.request.assert_called_once_with(
            "POST", "calls/bulk_call/123/add_contacts", params=None, headers=None,
            json_data={'contacts': contacts})

    def test_rejects_over_1000(self):
        contacts = [{"to_number": "+1"}] * 1001
        with self.assertRaises(ValueError):
            self.client.bulk_call.add_contacts(123, contacts)

    def test_accepts_exactly_1000(self):
        contacts = [{"to_number": "+1"}] * 1000
        self.client.bulk_call.add_contacts(123, contacts)
        self.client.request.assert_called_once()

    def test_rejects_missing_to_number(self):
        with self.assertRaises(ValueError):
            self.client.bulk_call.add_contacts(123, [{"phone_number": "+1"}])

    def test_rejects_empty_list(self):
        with self.assertRaises(ValueError):
            self.client.bulk_call.add_contacts(123, [])


class TestStartAndRetry(unittest.TestCase):
    def setUp(self):
        self.client = make_client()

    def test_start_bulk_call(self):
        self.client.bulk_call.start_bulk_call(123)
        self.client.request.assert_called_once_with(
            "POST", "calls/bulk_call/123/start", params=None, headers=None, json_data={})

    def test_manual_retry(self):
        self.client.bulk_call.manual_retry(123)
        self.client.request.assert_called_once_with(
            "POST", "calls/bulk_call/123/manual_retry", params=None, headers=None, json_data={})


class TestUpdateConcurrency(unittest.TestCase):
    def setUp(self):
        self.client = make_client()

    def test_body(self):
        self.client.bulk_call.update_concurrency(123, 8)
        self.client.request.assert_called_once_with(
            "PUT", "calls/bulk_call/123/concurrency", params=None, headers=None,
            json_data={'concurrent_call_limit': 8})

    def test_rejects_zero(self):
        with self.assertRaises(ValueError):
            self.client.bulk_call.update_concurrency(123, 0)


class TestGetBulkCallLines(unittest.TestCase):
    def setUp(self):
        self.client = make_client()

    def test_no_filters_sends_empty_params(self):
        self.client.bulk_call.get_bulk_call_lines(123)
        self.client.request.assert_called_once_with(
            "GET", "calls/bulk_call/123/lines", params={}, headers=None)

    def test_all_filters(self):
        self.client.bulk_call.get_bulk_call_lines(
            123, pagesize=50, cursor="abc", call_status="completed",
            interaction_status="answered", search="john", include_total=True)
        self.client.request.assert_called_once_with(
            "GET", "calls/bulk_call/123/lines", headers=None,
            params={'pagesize': 50, 'cursor': 'abc', 'call_status': 'completed',
                    'interaction_status': 'answered', 'search': 'john',
                    'include_total': 'true'})

    def test_include_total_falsy_omitted(self):
        self.client.bulk_call.get_bulk_call_lines(123, include_total=False)
        params = self.client.request.call_args.kwargs['params']
        self.assertNotIn('include_total', params)

    def test_rejects_pagesize_over_150(self):
        with self.assertRaises(ValueError):
            self.client.bulk_call.get_bulk_call_lines(123, pagesize=151)


class TestLiveStatus(unittest.TestCase):
    def test_hyphenated_path(self):
        client = make_client()
        client.bulk_call.get_live_status(123)
        client.request.assert_called_once_with(
            "GET", "bulk-call/123/live-status", params=None, headers=None)


class TestRotationNumbers(unittest.TestCase):
    def setUp(self):
        self.client = make_client()

    def test_list(self):
        self.client.bulk_call.list_rotation_numbers(123)
        self.client.request.assert_called_once_with(
            "GET", "calls/bulk_call/123/numbers", params=None, headers=None)

    def test_add(self):
        self.client.bulk_call.add_rotation_number(123, 7)
        self.client.request.assert_called_once_with(
            "POST", "calls/bulk_call/123/numbers", params=None, headers=None,
            json_data={'phone_number_id': 7})

    def test_add_coerces_numeric_string_and_rejects_garbage(self):
        # The API's spec types ids as strings ("177"), so both int and numeric
        # string are accepted; anything non-numeric still fails loudly.
        self.client.bulk_call.add_rotation_number(123, "7")
        self.client.request.assert_called_once_with(
            "POST", "calls/bulk_call/123/numbers", params=None, headers=None,
            json_data={'phone_number_id': 7})
        with self.assertRaises(ValueError):
            self.client.bulk_call.add_rotation_number(123, "seven")

    def test_set_active(self):
        self.client.bulk_call.set_rotation_number_active(123, 456, False)
        self.client.request.assert_called_once_with(
            "PUT", "calls/bulk_call/123/numbers/456", params=None, headers=None,
            json_data={'is_active': False})

    def test_set_active_rejects_non_bool(self):
        with self.assertRaises(ValueError):
            self.client.bulk_call.set_rotation_number_active(123, 456, "yes")


if __name__ == '__main__':
    unittest.main()
