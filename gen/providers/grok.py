import json
import requests


class Grok:
    endpoint = 'https://api.x.ai/v1/responses'

    def __init__(self, options):
        self.model = options['model']
        self.key = options['key']
        self.effort = options['effort']

    def generate(self, system_prompt, args, stream_cb):
        json_payload = {
            'model': self.model,
            'stream': stream_cb is not None,
            'input': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': args.prompt},
            ],
            # by default, the responses endpoint saves responses for 30 days.
            # settings store=False disables this
            'store': False,
        }

        if self.effort:
            # json_payload['reasoning'] = {'effort': self.effort}
            json_payload['reasoning_effortl'] = self.effort

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

            # streaming responses on grok send all sorts of different event
            # types, not all of which are related to token outputs

            line = line.decode('utf-8')
            if not line.startswith('data: '):
                continue

            data = json.loads(line[6:])

            if data.get('type', '') != 'response.output_text.delta':
                continue

            if delta := data.get('delta', ''):
                full_response += delta
                stream_cb(delta)


        return full_response
