import json
import requests


class Ollama:
    def __init__(self, options):
        self.model = options['model']
        self.endpoint = options['endpoint']

    def generate(self, system_prompt, args, stream_cb):
        response = requests.post(
            f'{self.endpoint}/api/generate',
            json={
                'model': self.model,
                'system': system_prompt,
                'prompt': args.prompt,
                'stream': stream_cb is not None
            },
            stream=stream_cb is not None,
        )

        if not stream_cb:
            return response.json()['response']

        full_response = ''
        for line in response.iter_lines():
            if not line:
                continue

            data = json.loads(line)

            if not data['done']:
                full_response += data['response']
                stream_cb(data['response'])

        return full_response
