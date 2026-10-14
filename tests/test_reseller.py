import io
import os
import tempfile
import unittest
from unittest.mock import Mock, patch

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


class TestSubmitKycStepReturnUrl(unittest.TestCase):
    def test_return_url_is_sent_on_a_redirect_step(self):
        client = make_client()
        client.reseller.submit_kyc_step(
            "verify-aadhaar", 456, "IN", carrier="carrier-2-new",
            return_url="https://app.example.com/kyc/done")
        body = client.request.call_args.kwargs['json_data']
        self.assertEqual(body['return_url'], "https://app.example.com/kyc/done")


PDF = b'%PDF-1.7\n' + b'x' * 10


class TestUploadKycDocument(unittest.TestCase):
    def setUp(self):
        self.client = make_client()

    def _sent(self):
        kwargs = self.client.request.call_args.kwargs
        return self.client.request.call_args.args, kwargs

    def test_bytes_go_as_multipart_with_the_form_fields(self):
        self.client.reseller.upload_kyc_document(
            "upload-pan", 456, "IN", PDF, filename="pan.pdf", carrier="carrier-2-new")
        args, kwargs = self._sent()
        self.assertEqual(args, ("POST", "reseller/kyc/steps/upload-pan"))
        self.assertEqual(kwargs['files'], {'document': ('pan.pdf', PDF)})
        self.assertEqual(kwargs['data'],
                         {'user_id': 456, 'region': 'IN', 'carrier': 'carrier-2-new'})
        self.assertIsNone(kwargs.get('json_data'))

    def test_a_path_is_read_and_named_after_the_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "my pan card.pdf")
            with open(path, "wb") as handle:
                handle.write(PDF)
            self.client.reseller.upload_kyc_document("upload-pan", 456, "IN", path)
        self.assertEqual(self._sent()[1]['files'], {'document': ('my pan card.pdf', PDF)})

    def test_an_open_file_is_read_and_named_after_the_file(self):
        handle = io.BytesIO(PDF)
        handle.name = "/tmp/scans/aadhaar.pdf"
        self.client.reseller.upload_kyc_document("upload-aadhaar", 456, "IN", handle)
        self.assertEqual(self._sent()[1]['files'], {'document': ('aadhaar.pdf', PDF)})

    def test_carrier_omitted_by_default(self):
        self.client.reseller.upload_kyc_document(
            "upload-pan", 456, "IN", PDF, filename="pan.pdf")
        self.assertNotIn('carrier', self._sent()[1]['data'])

    def test_bytes_need_a_filename(self):
        with self.assertRaises(ValueError):
            self.client.reseller.upload_kyc_document("upload-pan", 456, "IN", PDF)

    def test_required_arguments(self):
        for args in (("", 456, "IN", PDF), ("upload-pan", None, "IN", PDF),
                     ("upload-pan", 456, "", PDF), ("upload-pan", 456, "IN", None)):
            with self.subTest(args=args[:3]):
                with self.assertRaises(ValueError):
                    self.client.reseller.upload_kyc_document(*args, filename="pan.pdf")


class TestClientMultipart(unittest.TestCase):
    """The client forced a JSON content type on every call, so no file could be
    sent. A multipart call must leave the boundary header to requests."""

    def test_files_go_as_multipart_not_json(self):
        client = Client('x' * 12)
        response = Mock(status_code=200, content=b'{}')
        response.json.return_value = {}
        with patch('omnidimension.client.requests.request', return_value=response) as req:
            client.post("reseller/kyc/steps/upload-pan", data={'user_id': 1},
                        files={'document': ('pan.pdf', PDF)})
        kwargs = req.call_args.kwargs
        self.assertEqual(kwargs['files'], {'document': ('pan.pdf', PDF)})
        self.assertEqual(kwargs['data'], {'user_id': 1})
        self.assertIsNone(kwargs['json'])
        self.assertNotIn('Content-Type', kwargs['headers'])

    def test_json_posts_are_unchanged(self):
        client = Client('x' * 12)
        response = Mock(status_code=200, content=b'{}')
        response.json.return_value = {}
        with patch('omnidimension.client.requests.request', return_value=response) as req:
            client.post("agents/create", data={'name': 'a'})
        kwargs = req.call_args.kwargs
        self.assertEqual(kwargs['json'], {'name': 'a'})
        self.assertEqual(kwargs['headers']['Content-Type'], 'application/json')


class TestIdentityAndClientAccess(unittest.TestCase):
    def setUp(self):
        self.client = make_client()

    def sent(self):
        call = self.client.request.call_args
        return call.args[0], call.args[1], call.kwargs.get('json_data')

    def test_get_identity(self):
        self.client.reseller.get_identity()
        self.assertEqual(self.sent()[:2], ("GET", "reseller/identity"))

    def test_save_identity_sends_only_given_fields(self):
        self.client.reseller.save_identity(platform_name="Acme Voice", primary_color="#1976d2")
        method, path, body = self.sent()
        self.assertEqual((method, path), ("POST", "reseller/identity/save"))
        self.assertEqual(body, {"platform_name": "Acme Voice", "primary_color": "#1976d2"})

    def test_save_identity_smtp(self):
        self.client.reseller.save_identity_smtp(
            host="smtp.acme.example", port=587, username="u", password="p",
            encryption="ssl", from_email="hello@acme.example")
        method, path, body = self.sent()
        self.assertEqual((method, path), ("POST", "reseller/identity/smtp/save"))
        self.assertEqual(set(body), {"host", "port", "username", "password", "encryption", "from_email"})

    def test_test_identity_smtp_omits_blank_password(self):
        self.client.reseller.test_identity_smtp(host="smtp.acme.example", port=587, username="u")
        method, path, body = self.sent()
        self.assertEqual((method, path), ("POST", "reseller/identity/smtp/test"))
        self.assertEqual(set(body), {"host", "port", "username"})

    def test_disable_identity_smtp(self):
        self.client.reseller.disable_identity_smtp()
        method, path, body = self.sent()
        self.assertEqual((method, path), ("POST", "reseller/identity/smtp/disable"))
        self.assertIsNone(body)

    def test_set_client_access_user(self):
        self.client.reseller.set_client_access(blocked=False, user_id=1234)
        method, path, body = self.sent()
        self.assertEqual((method, path), ("POST", "reseller/users/access"))
        self.assertEqual(body, {"blocked": False, "user_id": 1234})

    def test_set_client_access_organization_with_detach(self):
        self.client.reseller.set_client_access(
            blocked=True, organization_id=5678, detach_numbers=True)
        body = self.sent()[2]
        self.assertEqual(body, {"blocked": True, "organization_id": 5678, "detach_numbers": True})

    def test_set_client_access_refuses_bad_target_or_blocked(self):
        with self.assertRaises(ValueError):
            self.client.reseller.set_client_access(blocked=True)
        with self.assertRaises(ValueError):
            self.client.reseller.set_client_access(blocked=True, user_id=1, organization_id=2)
        with self.assertRaises(ValueError):
            self.client.reseller.set_client_access(blocked="false", user_id=1)
