import json

from gen.providers.base_provider import BaseProvider


class Cerebras(BaseProvider):
    endpoint = 'https://api.cerebras.ai/v1/chat/completions'

    def _build_payload(self, system_prompt, prompt):
        return {
            'model': self.model,
            'stream': True,
            'reasoning_effort': self.effort,
            'messages': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt},
            ]
        }

    def _extract_stream_chunk(self, line):
        data = line[6:]

        if data == b'[DONE]':
            return

        data = json.loads(data)

        if choices := data.get('choices', []):
            return choices[0].get('delta', {}).get('content', '')
