def _params(user_id=None, **query):
    """Only the query parts given, so an omitted option falls back to the API default."""
    params = {k: v for k, v in query.items() if v is not None}
    if user_id is not None:
        params['user_id'] = user_id
    return params


class Workflow():
    def __init__(self, client):
        """
        Initialize the Workflow client with a reference to the main API client.

        Args:
            client: The main API client instance.
        """
        self.client = client

    def list_node_types(self, q=None, category=None):
        """
        List the node types a workflow can use.

        Args:
            q (str): Words to match against the type, label and description (optional).
            category (str): Only types in this category: triggers, messaging, calls,
                flow, ai, crm or integrations (optional).

        Returns:
            dict: Response containing the node types.
        """
        return self.client.get("workflow-node-types", params=_params(q=q, category=category))

    def get_node_type(self, node_type, detail=None):
        """
        Get one node type.

        Args:
            node_type (str): The node type name.
            detail (str): "minimal" (default) or "full", which adds descriptions,
                examples and the output example (optional).

        Returns:
            dict: Response containing the node type.

        Raises:
            ValueError: If node_type is not provided.
        """
        if not node_type:
            raise ValueError("node_type is required.")
        return self.client.get(f"workflow-node-types/{node_type}", params=_params(detail=detail))

    def list_field_options(self, node_type, field, user_id=None, depends=None):
        """
        List the choices for a field of a node type.

        Args:
            node_type (str): The node type name.
            field (str): The field to list choices for.
            user_id (int): Reseller accounts only, names the client to act on.
                Omit it to act on your own account (optional).
            depends (int): The value of the field this one depends on, such as
                the chosen phone number id (optional).

        Returns:
            dict: Response containing the choices.

        Raises:
            ValueError: If node_type or field is not provided.
        """
        if not node_type:
            raise ValueError("node_type is required.")
        if not field:
            raise ValueError("field is required.")
        return self.client.get(f"workflow-node-types/{node_type}/options/{field}",
                               params=_params(user_id, depends=depends))

    def list(self, user_id=None, limit=None, cursor=None):
        """
        List workflows.

        Args:
            user_id (int): Reseller accounts only, names the client to act on.
                Omit it to act on your own account (optional).
            limit (int): Rows per page, 1 to 100 (optional).
            cursor (str): The next_cursor from the previous page, passed back unchanged (optional).

        Returns:
            dict: Response containing the workflows.
        """
        return self.client.get("workflows", params=_params(user_id, limit=limit, cursor=cursor))

    def create(self, name, graph=None, user_id=None):
        """
        Create a workflow.

        Args:
            name (str): Name of the workflow.
            graph (dict): The starting nodes and connections (optional).
            user_id (int): Reseller accounts only, names the client to act on.
                Omit it to act on your own account (optional).

        Returns:
            dict: Response containing the created workflow.

        Raises:
            ValueError: If name is not provided.
        """
        if not name:
            raise ValueError("name is required.")

        data = {'name': name}
        if graph is not None:
            data['graph'] = graph
        return self.client.post("workflows", data=data, params=_params(user_id))

    def get(self, workflow_id, user_id=None, view=None):
        """
        Get a workflow.

        Args:
            workflow_id (int): The ID of the workflow.
            user_id (int): Reseller accounts only, names the client to act on.
                Omit it to act on your own account (optional).
            view (str): "full" (default) or "structure", which leaves node config out (optional).

        Returns:
            dict: Response containing the workflow.
        """
        return self.client.get(f"workflows/{workflow_id}", params=_params(user_id, view=view))

    def edit(self, workflow_id, revision, ops, name=None, user_id=None):
        """
        Edit a workflow draft. Use publish to make the change live.

        Args:
            workflow_id (int): The ID of the workflow.
            revision (str): The revision from your last read. A stale one gets a
                409 revision_conflict: read the workflow again and retry.
            ops (list): Operations that add, update, move or delete nodes, and
                connect or disconnect them. They apply all together or not at all.
            name (str): New name for the workflow (optional).
            user_id (int): Reseller accounts only, names the client to act on.
                Omit it to act on your own account (optional).

        Returns:
            dict: Response containing the updated workflow.

        Raises:
            ValueError: If revision or ops is not provided.
        """
        if not revision:
            raise ValueError("revision is required.")
        if not ops:
            raise ValueError("ops is required.")

        data = {'revision': revision, 'ops': ops}
        if name is not None:
            data['name'] = name
        return self.client.patch(f"workflows/{workflow_id}", data=data, params=_params(user_id))

    def delete(self, workflow_id, user_id=None):
        """
        Delete a workflow.

        Args:
            workflow_id (int): The ID of the workflow.
            user_id (int): Reseller accounts only, names the client to act on.
                Omit it to act on your own account (optional).

        Returns:
            dict: Response indicating success or failure.
        """
        return self.client.delete(f"workflows/{workflow_id}", params=_params(user_id))

    def validate(self, workflow_id, user_id=None):
        """
        Validate a workflow draft.

        Args:
            workflow_id (int): The ID of the workflow.
            user_id (int): Reseller accounts only, names the client to act on.
                Omit it to act on your own account (optional).

        Returns:
            dict: Response containing the validation result.
        """
        return self.client.post(f"workflows/{workflow_id}/validate", params=_params(user_id))

    def publish(self, workflow_id, user_id=None):
        """
        Publish a workflow draft.

        Args:
            workflow_id (int): The ID of the workflow.
            user_id (int): Reseller accounts only, names the client to act on.
                Omit it to act on your own account (optional).

        Returns:
            dict: Response containing the published workflow.
        """
        return self.client.post(f"workflows/{workflow_id}/publish", params=_params(user_id))

    def activate(self, workflow_id, user_id=None):
        """
        Activate a workflow.

        Args:
            workflow_id (int): The ID of the workflow.
            user_id (int): Reseller accounts only, names the client to act on.
                Omit it to act on your own account (optional).

        Returns:
            dict: Response containing the workflow.
        """
        return self.client.post(f"workflows/{workflow_id}/activate", params=_params(user_id))

    def deactivate(self, workflow_id, user_id=None):
        """
        Deactivate a workflow.

        Args:
            workflow_id (int): The ID of the workflow.
            user_id (int): Reseller accounts only, names the client to act on.
                Omit it to act on your own account (optional).

        Returns:
            dict: Response containing the workflow.
        """
        return self.client.post(f"workflows/{workflow_id}/deactivate", params=_params(user_id))

    def test(self, workflow_id, payload=None, user_id=None):
        """
        Run a workflow with a test payload.

        Args:
            workflow_id (int): The ID of the workflow.
            payload (dict): The trigger payload to run with (optional).
            user_id (int): Reseller accounts only, names the client to act on.
                Omit it to act on your own account (optional).

        Returns:
            dict: Response containing the test run.
        """
        data = {}
        if payload is not None:
            data['payload'] = payload
        return self.client.post(f"workflows/{workflow_id}/test", data=data, params=_params(user_id))

    def get_execution(self, workflow_id, execution_id, user_id=None):
        """
        Get a workflow run.

        Args:
            workflow_id (int): The ID of the workflow.
            execution_id (int): The ID of the run.
            user_id (int): Reseller accounts only, names the client to act on.
                Omit it to act on your own account (optional).

        Returns:
            dict: Response containing the run.
        """
        return self.client.get(f"workflows/{workflow_id}/executions/{execution_id}",
                               params=_params(user_id))
