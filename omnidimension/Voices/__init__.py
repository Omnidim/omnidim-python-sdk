class Voices():
    def __init__(self, client):
        """
        Initialize the Voices client with a reference to the main API client.

        Args:
            client: The main API client instance.
        """
        self.client = client

    def list_cloned_voices(self, limit=None, cursor=None):
        """
        List the cloned voices on this account.

        Args:
            limit (int): Maximum number of voices to return (optional).
            cursor (str): Pagination cursor from a previous call (optional).

        Returns:
            dict: Response containing the cloned voices and a cursor.
        """
        params = {}
        if limit is not None:
            params['limit'] = limit
        if cursor is not None:
            params['cursor'] = cursor
        return self.client.get("voices", params=params)

    def create_cloned_voice(self, name, clip, consent, idempotency_key=None, **fields):
        """
        Clone a voice from an audio sample. Creation is asynchronous: the
        voice is not usable until its status is ready, so poll
        get_cloned_voice. Voice cloning must be included in your plan.

        Args:
            name (str): Name for the cloned voice.
            clip: The audio sample to clone from.
            consent (bool): Confirmation that the speaker consented to cloning.
            idempotency_key (str): Key that makes a retry safe (optional).
            **fields: Any other create field from the spec.

        Returns:
            dict: Response containing the new voice and its status.
        """
        data = {
            'name': name,
            'clip': clip,
            'consent': consent,
        }
        data.update(fields)
        headers = {'Idempotency-Key': idempotency_key} if idempotency_key else None
        return self.client.post("voices", data=data, headers=headers)

    def get_cloned_voice(self, voice_id):
        """
        Retrieve one cloned voice, including its status.

        Args:
            voice_id (int): ID of the cloned voice.

        Returns:
            dict: Response containing the voice.
        """
        return self.client.get("voices/{}".format(voice_id))

    def update_cloned_voice(self, voice_id, **fields):
        """
        Update a cloned voice.

        Args:
            voice_id (int): ID of the cloned voice.
            **fields: The fields to change.

        Returns:
            dict: Response containing the updated voice.
        """
        return self.client.patch("voices/{}".format(voice_id), data=fields)

    def delete_cloned_voice(self, voice_id):
        """
        Delete a cloned voice.

        Args:
            voice_id (int): ID of the cloned voice.

        Returns:
            dict: Response indicating success or failure.
        """
        return self.client.delete("voices/{}".format(voice_id))

    def get_cloned_voice_sample(self, voice_id):
        """
        Fetch the sample audio for a cloned voice.

        Args:
            voice_id (int): ID of the cloned voice.

        Returns:
            dict: Response containing the sample.
        """
        return self.client.get("voices/{}/sample".format(voice_id))

    def regenerate_cloned_voice_sample(self, voice_id):
        """
        Ask for the sample audio of a cloned voice to be regenerated.

        Args:
            voice_id (int): ID of the cloned voice.

        Returns:
            dict: Response indicating the regeneration was queued.
        """
        return self.client.post("voices/{}/sample".format(voice_id))
