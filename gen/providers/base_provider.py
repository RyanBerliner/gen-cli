import requests


class BaseProvider:
    # If the provider could have any number of endpoints, the user is expected
    # to provide an endpoint in their config (which is subsequently passed to
    # the constructor here) and used alongside this endpoint path to create the
    # full endpoint. For providers with a single endpoint, no endpoint is
    # provided and the provider class should provide a single static property
    # called endpoint, being the fully qualified URL + path
    endpoint_path = None

    def __init__(self, model, key=None, effort=None, endpoint=None):
        self.model = model
        self.key = key
        self.effort = effort

        if self.endpoint_path:
            assert endpoint, 'Must supply an endpoint'
            self.endpoint = endpoint + self.endpoint_path

    def _get_headers(self):
        if not self.key:
            return {}

        return {'Authorization': f'Bearer {self.key}'}

    def _build_payload(self, system_prompt, prompt):
        raise NotImplementedError

    def _extract_stream_chunk(self, line):
        raise NotImplementedError

    def _handle_stream(self, response, stream_cb):
        full_response = ''

        for line in response.iter_lines():
            if not line:
                continue

            if chunk := self._extract_stream_chunk(line):
                full_response += chunk
                stream_cb(chunk)

        return full_response

    def generate(self, system_prompt, prompt, stream_cb):
        return self._handle_stream(
            requests.post(
                self.endpoint,
                headers=self._get_headers(),
                json=self._build_payload(system_prompt, prompt),
                stream=True,
            ),
            stream_cb
        )
