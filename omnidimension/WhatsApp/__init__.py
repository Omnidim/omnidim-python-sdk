class WhatsApp():
    def __init__(self, client):
        """
        Initialize the WhatsApp client with a reference to the main API client.

        Args:
            client: The main API client instance.
        """
        self.client = client

    @staticmethod
    def _params(**values):
        return {k: v for k, v in values.items() if v is not None}

    # ---- numbers ----

    def list_numbers(self, limit=None, cursor=None):
        """List your WhatsApp numbers with their health and quality rating."""
        return self.client.get("whatsapp/numbers", params=self._params(limit=limit, cursor=cursor))

    def preview_numbers(self, waba_id, access_token):
        """
        List the numbers on a Meta WhatsApp Business account, with their
        health, before connecting any. Nothing is imported.

        Args:
            waba_id (str): The WhatsApp Business Account id.
            access_token (str): A Meta access token with WhatsApp permissions.
        """
        return self.client.post("whatsapp/numbers/preview",
                                data={'waba_id': waba_id, 'access_token': access_token})

    def import_numbers(self, waba_id, access_token, phone_number_ids, app_secret=None):
        """
        Connect numbers from a Meta WhatsApp Business account. Connecting a
        number again with a new token or app secret updates it.

        Args:
            waba_id (str): The WhatsApp Business Account id.
            access_token (str): A Meta access token with WhatsApp permissions.
            phone_number_ids (list): Meta phone number ids to connect.
            app_secret (str): The Meta app secret (optional).
        """
        data = {'waba_id': waba_id, 'access_token': access_token,
                'phone_number_ids': phone_number_ids}
        if app_secret is not None:
            data['app_secret'] = app_secret
        return self.client.post("whatsapp/numbers", data=data)

    def get_number(self, number_id):
        """Retrieve one WhatsApp number."""
        return self.client.get(f"whatsapp/numbers/{number_id}")

    def list_templates(self, number_id, status=None, limit=None, cursor=None):
        """List a number's message templates."""
        return self.client.get(f"whatsapp/numbers/{number_id}/templates",
                               params=self._params(status=status, limit=limit, cursor=cursor))

    def sync_templates(self, number_id):
        """Fetch the number's latest templates and their approval status from Meta."""
        return self.client.post(f"whatsapp/numbers/{number_id}/templates/sync")

    def get_calling(self, number_id):
        """Read whether WhatsApp calling is on for a number."""
        return self.client.get(f"whatsapp/numbers/{number_id}/calling")

    def set_calling(self, number_id, enabled):
        """Turn WhatsApp calling on or off for a number."""
        return self.client.patch(f"whatsapp/numbers/{number_id}/calling",
                                 data={'enabled': enabled})

    # ---- conversations and messages ----

    def list_conversations(self, number_id, filter=None, q=None, updated_since=None,
                           limit=None, cursor=None):
        """List a number's conversations. Pass updated_since to poll for changes."""
        return self.client.get(
            f"whatsapp/numbers/{number_id}/conversations",
            params=self._params(filter=filter, q=q, updated_since=updated_since,
                                limit=limit, cursor=cursor))

    def get_conversation(self, conversation_id):
        """Retrieve one conversation, including whether its 24-hour window is open."""
        return self.client.get(f"whatsapp/conversations/{conversation_id}")

    def take_over_conversation(self, conversation_id):
        """Stop the agent replying so a person can answer."""
        return self.client.post(f"whatsapp/conversations/{conversation_id}/take_over")

    def hand_back_conversation(self, conversation_id):
        """Let the agent reply again."""
        return self.client.post(f"whatsapp/conversations/{conversation_id}/hand_back")

    def list_messages(self, conversation_id, after=None, limit=None, cursor=None):
        """List a conversation's messages. Pass after to read only newer ones."""
        params = {'conversation_id': conversation_id}
        params.update(self._params(after=after, limit=limit, cursor=cursor))
        return self.client.get("whatsapp/messages", params=params)

    def send_message(self, phone_number_id, to, type, idempotency_key, **fields):
        """
        Send a message. A text needs an open 24-hour window; a template can
        start a conversation.

        Args:
            phone_number_id (int): The WhatsApp number to send from.
            to (str): The customer's number in E.164 format.
            type (str): The message type, such as "text", "template" or "image".
            idempotency_key (str): A unique string per message. A retry with
                the same key and body sends nothing new.
            **fields: The fields for that type, such as text, template,
                media, reply_to or take_over.
        """
        data = {'phone_number_id': phone_number_id, 'to': to, 'type': type}
        data.update(fields)
        return self.client.post("whatsapp/messages", data=data,
                                headers={'Idempotency-Key': idempotency_key})

    def get_message(self, message_id):
        """Retrieve one message, including its delivery status."""
        return self.client.get(f"whatsapp/messages/{message_id}")

    def upload_media(self, phone_number_id, type, file):
        """
        Upload a file to send in a message.

        Args:
            phone_number_id (int): The WhatsApp number the file will be sent from.
            type (str): The media type, such as "image" or "document".
            file: An open binary file, or a (filename, bytes, content_type) tuple.
        """
        return self.client.post("whatsapp/media",
                                data={'phone_number_id': phone_number_id, 'type': type},
                                files={'file': file})

    # ---- opt-outs ----

    def list_opt_outs(self, number_id, active=None, customer=None, limit=None, cursor=None):
        """List the customers blocked from receiving messages on a number."""
        return self.client.get(
            f"whatsapp/numbers/{number_id}/opt_outs",
            params=self._params(active=active, customer=customer, limit=limit, cursor=cursor))

    def add_opt_out(self, number_id, customer, note=None):
        """Block a customer from receiving messages on a number."""
        data = {'customer': customer}
        if note is not None:
            data['note'] = note
        return self.client.post(f"whatsapp/numbers/{number_id}/opt_outs", data=data)

    def lift_opt_out(self, number_id, opt_out_id):
        """Lift a block so the customer can receive messages again."""
        return self.client.delete(f"whatsapp/numbers/{number_id}/opt_outs/{opt_out_id}")

    # ---- campaigns ----

    def list_campaigns(self, status=None, phone_number_id=None, limit=None, cursor=None):
        """List broadcast campaigns."""
        return self.client.get("whatsapp/campaigns", params=self._params(
            status=status, phone_number_id=phone_number_id, limit=limit, cursor=cursor))

    def create_campaign(self, name, phone_number_id, template_id, **fields):
        """
        Create a draft broadcast campaign.

        Args:
            name (str): Campaign name.
            phone_number_id (int): The WhatsApp number to send from.
            template_id (int): The approved template to send.
            **fields: Any other create field from the spec, such as
                campaign_mode, agent_id or variable_mapping.
        """
        data = {'name': name, 'phone_number_id': phone_number_id, 'template_id': template_id}
        data.update(fields)
        return self.client.post("whatsapp/campaigns", data=data)

    def get_campaign(self, campaign_id):
        """Retrieve one campaign with its delivery counts."""
        return self.client.get(f"whatsapp/campaigns/{campaign_id}")

    def list_campaign_contacts(self, campaign_id, status=None, limit=None, cursor=None):
        """List a campaign's contacts and what happened to each."""
        return self.client.get(f"whatsapp/campaigns/{campaign_id}/contacts",
                               params=self._params(status=status, limit=limit, cursor=cursor))

    def add_campaign_contacts(self, campaign_id, contacts):
        """
        Add one contact or up to 500. On a running campaign they are sent now.

        Args:
            campaign_id (int): The campaign.
            contacts (dict or list): One contact, or a list of them. Each needs
                a phone_number; other keys can fill template parameters.
        """
        return self.client.post(f"whatsapp/campaigns/{campaign_id}/contacts", data=contacts)

    def launch_campaign(self, campaign_id, idempotency_key):
        """Start a draft campaign. A retry with the same idempotency_key does not start it twice."""
        return self.client.post(f"whatsapp/campaigns/{campaign_id}/launch",
                                headers={'Idempotency-Key': idempotency_key})

    def pause_campaign(self, campaign_id):
        """Pause a running campaign."""
        return self.client.post(f"whatsapp/campaigns/{campaign_id}/pause")

    def resume_campaign(self, campaign_id):
        """Resume a paused campaign."""
        return self.client.post(f"whatsapp/campaigns/{campaign_id}/resume")

    def cancel_campaign(self, campaign_id):
        """Stop a campaign for good. Contacts not yet sent are not sent."""
        return self.client.post(f"whatsapp/campaigns/{campaign_id}/cancel")
