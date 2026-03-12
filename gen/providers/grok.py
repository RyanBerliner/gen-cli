import json

from gen.providers.base_provider import BaseProvider


class Grok(BaseProvider):
    endpoint = 'https://api.x.ai/v1/responses'

    def _build_payload(self, system_prompt, prompt):
        return {
            'model': self.model,
            'stream': True,
            'reasoning_effort': self.effort,
            'input': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt},
            ],
            # by default, the responses endpoint saves responses for 30 days.
            # settings store=False disables this
            'store': False,
        }

    def _extract_stream_chunk(self, line):
        # streaming responses on grok send all sorts of different event types,
        # not all of which are related to token outputs. chunks we care about
        # are prefixed like 'data: '
        line = line.decode('utf-8')
        if not line.startswith('data: '):
            return None

        data = json.loads(line[6:])

        if data.get('type') == 'response.output_text.delta':
            return data.get('delta', None)
