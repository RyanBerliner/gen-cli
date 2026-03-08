import json
import requests


class Cerebras:
    endpoint = 'https://api.cerebras.ai/v1/chat/completions'

    def __init__(self, options):
        self.model = options['model']
        self.key = options['key']
        self.effort = options['effort']

    def generate(self, system_prompt, args, stream_cb):
        json_payload = {
            'model': self.model,
            'stream': stream_cb is not None,
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': args.prompt},
            ]
        }

        if self.effort:
            json_payload['reasoning_effort'] = self.effort

        response = requests.post(
            self.endpoint,
            headers={'Authorization': f'Bearer {self.key}'},
            json=json_payload,
            stream=stream_cb is not None,
        )

        if not stream_cb:
            return response.json()['response']

        full_response = ''
        for line in response.iter_lines():
            if not line:
                continue

            # data is prefixed like 'DATA: '
            data = json.loads(line[6:])

            if choices := data.get('choices', []):
                content = choices[0].get('delta', {}).get('content', '')
                full_response += content
                stream_cb(content)


        return full_response
