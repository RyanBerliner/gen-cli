import json
import urllib.request


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

    def _auth_headers(self):
        if not self.key:
            return {}

        return {'Authorization': f'Bearer {self.key}'}

    def _build_payload(self, system_prompt, prompt):
        raise NotImplementedError

    def _extract_output_token(self, line):
        raise NotImplementedError

    # Not all providers need to support outputting thinking tokens
    def _extract_thinking_token(self, line):
        pass

    def generate(
        self,
        system_prompt,
        prompt,
        output_token_cb,
        thinking_progress_cb
    ):
        full_response = ''
        payload = self._build_payload(system_prompt, prompt)

        request = urllib.request.Request(
            self.endpoint,
            data=json.dumps(payload).encode('utf-8'),
            headers={
                **self._auth_headers(),
                'Content-Type': 'application/json',
                # A not super sketchy user agent is required to get through
                # some apis firewall configurations
                # TODO: add a version string
                'User-Agent': 'python/gen-cli',
            },
        )

        with urllib.request.urlopen(request) as response:
            for line in response:
                if not line:
                    continue

                line = line.rstrip(b'\r\n')

                if output := self._extract_output_token(line):
                    full_response += output
                    output_token_cb(output)

                if thinking := self._extract_thinking_progress(line):
                    thinking_progress_cb(thinking)

        return full_response
