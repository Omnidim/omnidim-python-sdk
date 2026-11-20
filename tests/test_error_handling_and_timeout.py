import unittest
from unittest.mock import MagicMock, patch
import requests

from omnidimension.client import Client, APIError


class TestClientErrorHandlingAndTimeout(unittest.TestCase):
    def setUp(self):
        self.client = Client("test-api-key-12345", timeout=45.0)

    def test_default_and_custom_timeout(self):
        c_default = Client("test-api-key-12345")
        self.assertEqual(c_default.timeout, 60.0)
        self.assertEqual(self.client.timeout, 45.0)

    @patch("requests.request")
    def test_timeout_forwarded_to_requests(self, mock_request):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.content = b'{"status": "ok"}'
        mock_resp.json.return_value = {"status": "ok"}
        mock_request.return_value = mock_resp

        self.client.request("GET", "/agents")
        mock_request.assert_called_once()
        self.assertEqual(mock_request.call_args[1]["timeout"], 45.0)

    @patch("requests.request")
    def test_per_request_timeout_override(self, mock_request):
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.content = b'{"status": "ok"}'
        mock_resp.json.return_value = {"status": "ok"}
        mock_request.return_value = mock_resp

        self.client.request("GET", "/agents", timeout=12.5)
        self.assertEqual(mock_request.call_args[1]["timeout"], 12.5)

    @patch("requests.request")
    def test_error_message_extracted_from_detail(self, mock_request):
        mock_resp = MagicMock()
        mock_resp.status_code = 404
        mock_resp.json.return_value = {"detail": "Agent not found in database"}
        mock_request.side_effect = requests.exceptions.HTTPError(response=mock_resp)

        with self.assertRaises(APIError) as ctx:
            self.client.request("GET", "/agents/999")
        self.assertEqual(ctx.exception.status_code, 404)
        self.assertEqual(ctx.exception.message, "Agent not found in database")
        self.assertEqual(ctx.exception.response, {"detail": "Agent not found in database"})

    @patch("requests.request")
    def test_error_message_extracted_from_message_key(self, mock_request):
        mock_resp = MagicMock()
        mock_resp.status_code = 400
        mock_resp.json.return_value = {"status": "error", "message": "Campaign is not dynamic"}
        mock_request.side_effect = requests.exceptions.HTTPError(response=mock_resp)

        with self.assertRaises(APIError) as ctx:
            self.client.request("POST", "/calls/bulk_call/7/add_contacts")
        self.assertEqual(ctx.exception.status_code, 400)
        self.assertEqual(ctx.exception.message, "Campaign is not dynamic")

    @patch("requests.request")
    def test_error_message_fallback_on_raw_string(self, mock_request):
        mock_resp = MagicMock()
        mock_resp.status_code = 502
        mock_resp.json.return_value = "Bad Gateway upstream"
        mock_request.side_effect = requests.exceptions.HTTPError(response=mock_resp)

        with self.assertRaises(APIError) as ctx:
            self.client.request("GET", "/calls")
        self.assertEqual(ctx.exception.status_code, 502)
        self.assertEqual(ctx.exception.message, "Bad Gateway upstream")


if __name__ == "__main__":
    unittest.main()
