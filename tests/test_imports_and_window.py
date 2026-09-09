import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import Mock

from omnidimension import Client


def make_client():
    client = Client('x' * 12)
    client.request = Mock(return_value={"status": 200, "json": {}})
    return client


class TestClientIsQuiet(unittest.TestCase):
    def test_constructing_a_client_prints_nothing(self):
        # 0.4.1 shipped a debug print of the base URL, so every caller got a
        # stray line on stdout. Anything that writes to stdout from a library
        # corrupts a caller piping structured output.
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            Client('x' * 12)
        self.assertEqual(buffer.getvalue(), "")


class TestImportTwilio(unittest.TestCase):
    def setUp(self):
        self.client = make_client()

    def test_posts_the_credentials(self):
        self.client.phone_number.import_twilio(
            phone_number="+15551234567", account_sid="AC1", account_token="tok")
        args, kwargs = self.client.request.call_args
        self.assertEqual(args[0], "POST")
        self.assertIn("phone_number/import/twilio", args[1])
        self.assertEqual(kwargs['json_data']['account_sid'], "AC1")

    def test_name_is_omitted_when_not_given(self):
        self.client.phone_number.import_twilio("+15551234567", "AC1", "tok")
        self.assertNotIn('name', self.client.request.call_args.kwargs['json_data'])

    def test_missing_token_is_refused_before_the_call(self):
        with self.assertRaisesRegex(ValueError, "account_token is required"):
            self.client.phone_number.import_twilio("+15551234567", "AC1", "")
        self.client.request.assert_not_called()


class TestImportExotel(unittest.TestCase):
    FULL = dict(exotel_phone_number="+915551234567", exotel_api_key="k",
                exotel_api_token="t", exotel_subdomain="sub",
                exotel_account_sid="sid", exotel_app_id="app")

    def setUp(self):
        self.client = make_client()

    def test_posts_every_credential(self):
        self.client.phone_number.import_exotel(**self.FULL)
        body = self.client.request.call_args.kwargs['json_data']
        for field, value in self.FULL.items():
            self.assertEqual(body[field], value)

    def test_each_required_field_is_checked(self):
        for field in self.FULL:
            partial = dict(self.FULL, **{field: ""})
            with self.subTest(field):
                with self.assertRaisesRegex(ValueError, f"{field} is required"):
                    self.client.phone_number.import_exotel(**partial)


class TestImportSip(unittest.TestCase):
    def setUp(self):
        self.client = make_client()

    def test_optional_fields_are_left_out_rather_than_sent_as_none(self):
        self.client.phone_number.import_sip("+15551234567", "sip.example", "trunk")
        body = self.client.request.call_args.kwargs['json_data']
        self.assertEqual(set(body), {"phone_number", "sip_host", "sip_trunk_name"})

    def test_optional_fields_pass_through_when_given(self):
        self.client.phone_number.import_sip(
            "+15551234567", "sip.example", "trunk", sip_port=5080, sip_strip_plus=False)
        body = self.client.request.call_args.kwargs['json_data']
        self.assertEqual(body['sip_port'], 5080)
        # False is a real value, not an omission.
        self.assertIs(body['sip_strip_plus'], False)


class TestDailyTimeControl(unittest.TestCase):
    def setUp(self):
        self.client = make_client()

    def test_puts_to_the_campaign_window(self):
        self.client.bulk_call.set_daily_time_control(
            7, enable_daily_hard_stop=True, enable_daily_auto_start=False)
        args, kwargs = self.client.request.call_args
        self.assertEqual(args[0], "PUT")
        self.assertIn("calls/bulk_call/7/daily-time-control", args[1])
        self.assertIs(kwargs['json_data']['enable_daily_auto_start'], False)

    def test_the_window_carries_its_own_timezones(self):
        self.client.bulk_call.set_daily_time_control(
            7, True, True, daily_stop_time=21.0, daily_stop_timezone="Asia/Kolkata")
        body = self.client.request.call_args.kwargs['json_data']
        self.assertEqual(body['daily_stop_timezone'], "Asia/Kolkata")
        self.assertNotIn('daily_start_time', body)

    def test_a_non_boolean_flag_is_refused(self):
        with self.assertRaisesRegex(ValueError, "enable_daily_hard_stop must be a boolean"):
            self.client.bulk_call.set_daily_time_control(7, "yes", True)
        self.client.request.assert_not_called()


if __name__ == "__main__":
    unittest.main()
