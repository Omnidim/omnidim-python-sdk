import unittest
from unittest.mock import Mock

from omnidimension import Client


def make_client():
    client = Client('x' * 12)
    client.request = Mock(return_value={"status": 200, "json": {}})
    return client


class TestWorkflow(unittest.TestCase):
    def setUp(self):
        self.client = make_client()

    def sent(self):
        call = self.client.request.call_args
        return call.args[0], call.args[1], call.kwargs

    def test_node_types_send_only_given_filters(self):
        self.client.workflow.list_node_types(q="whatsapp")
        verb, path, kw = self.sent()
        self.assertEqual((verb, path, kw['params']), ("GET", "workflow-node-types", {'q': 'whatsapp'}))
        self.client.workflow.list_node_types(category="crm")
        self.assertEqual(self.sent()[2]['params'], {'category': 'crm'})

    def test_get_node_type_and_field_options(self):
        self.client.workflow.get_node_type("send_whatsapp", detail="full")
        self.assertEqual(self.sent()[1], "workflow-node-types/send_whatsapp")
        self.assertEqual(self.sent()[2]['params'], {'detail': 'full'})
        self.client.workflow.list_field_options("send_whatsapp", "template", user_id=5, depends=9)
        verb, path, kw = self.sent()
        self.assertEqual(path, "workflow-node-types/send_whatsapp/options/template")
        self.assertEqual(kw['params'], {'depends': 9, 'user_id': 5})

    def test_list_and_get(self):
        self.client.workflow.list(limit=10, cursor="c1")
        self.assertEqual(self.sent()[2]['params'], {'limit': 10, 'cursor': 'c1'})
        self.client.workflow.get(7, view="structure")
        verb, path, kw = self.sent()
        self.assertEqual((verb, path, kw['params']), ("GET", "workflows/7", {'view': 'structure'}))

    def test_create_body_and_required_name(self):
        self.client.workflow.create("W", graph={"nodes": []}, user_id=3)
        verb, path, kw = self.sent()
        self.assertEqual((verb, path), ("POST", "workflows"))
        self.assertEqual(kw['json_data'], {'name': 'W', 'graph': {"nodes": []}})
        self.assertEqual(kw['params'], {'user_id': 3})
        with self.assertRaises(ValueError):
            self.client.workflow.create("")

    def test_create_omits_graph_when_none(self):
        self.client.workflow.create("W")
        self.assertEqual(self.sent()[2]['json_data'], {'name': 'W'})

    def test_edit_sends_revision_and_ops(self):
        self.client.workflow.edit(7, "rev1", [{"op": "delete_node", "id": "n1"}])
        verb, path, kw = self.sent()
        self.assertEqual((verb, path), ("PATCH", "workflows/7"))
        self.assertEqual(set(kw['json_data']), {'revision', 'ops'})
        with self.assertRaises(ValueError):
            self.client.workflow.edit(7, "rev1", [])

    def test_edit_sends_name_when_given(self):
        self.client.workflow.edit(7, "rev1", [{"op": "x"}], name="N", user_id=2)
        kw = self.sent()[2]
        self.assertEqual(kw['json_data'], {'revision': 'rev1', 'ops': [{"op": "x"}], 'name': 'N'})
        self.assertEqual(kw['params'], {'user_id': 2})

    def test_action_verbs_and_paths(self):
        wf = self.client.workflow
        for method, verb, path in [
            (wf.delete, "DELETE", "workflows/7"),
            (wf.validate, "POST", "workflows/7/validate"),
            (wf.publish, "POST", "workflows/7/publish"),
            (wf.activate, "POST", "workflows/7/activate"),
            (wf.deactivate, "POST", "workflows/7/deactivate"),
        ]:
            method(7, user_id=2)
            v, p, kw = self.sent()
            self.assertEqual((v, p, kw['params']), (verb, path, {'user_id': 2}))

    def test_test_run_and_execution(self):
        self.client.workflow.test(7, payload={"a": 1}, user_id=2)
        verb, path, kw = self.sent()
        self.assertEqual((verb, path, kw['json_data']), ("POST", "workflows/7/test", {'payload': {"a": 1}}))
        self.assertEqual(kw['params'], {'user_id': 2})
        self.client.workflow.get_execution(7, 11, user_id=2)
        verb, path, kw = self.sent()
        self.assertEqual((verb, path, kw['params']), ("GET", "workflows/7/executions/11", {'user_id': 2}))


class TestPostCallActionsAndIntegrations(unittest.TestCase):
    def setUp(self):
        self.client = make_client()

    def sent(self):
        call = self.client.request.call_args
        return call.args[0], call.args[1], call.kwargs

    def test_list_and_delete(self):
        self.client.agent.list_post_call_actions(4, user_id=2)
        verb, path, kw = self.sent()
        self.assertEqual((verb, path, kw['params']), ("GET", "agents/4/post-call-actions", {'user_id': 2}))
        self.client.agent.delete_post_call_action(4, "a1", user_id=2)
        verb, path, kw = self.sent()
        self.assertEqual((verb, path, kw['params']),
                         ("DELETE", "agents/4/post-call-actions/a1", {'user_id': 2}))

    def test_add_sends_type_fields_and_idempotency_header(self):
        self.client.agent.add_post_call_action(4, "webhook", idempotency_key="k1", url="https://x.io")
        verb, path, kw = self.sent()
        self.assertEqual((verb, path), ("POST", "agents/4/post-call-actions"))
        self.assertEqual(kw['json_data'], {'type': 'webhook', 'url': 'https://x.io'})
        self.assertEqual(kw['headers']['Idempotency-Key'], 'k1')
        self.client.agent.add_post_call_action(4, "webhook", url="https://x.io")
        self.assertIsNone(self.sent()[2]['headers'])
        with self.assertRaises(ValueError):
            self.client.agent.add_post_call_action(4, "")

    def test_update_sends_only_given_fields(self):
        self.client.agent.update_post_call_action(4, "a1", url="https://y.io", user_id=2)
        verb, path, kw = self.sent()
        self.assertEqual((verb, path, kw['json_data']),
                         ("PATCH", "agents/4/post-call-actions/a1", {'url': 'https://y.io', 'user_id': 2}))
        self.assertFalse(kw['params'])

    def test_integrations_user_id_optional(self):
        self.client.integrations.get_user_integrations()
        self.assertIsNone(self.sent()[2]['params'])
        self.client.integrations.get_user_integrations(user_id=9)
        self.assertEqual(self.sent()[2]['params'], {'user_id': 9})
