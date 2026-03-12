import json

from gen.providers.base_provider import BaseProvider


class Ollama(BaseProvider):
    endpoint_path = '/api/generate'

    def _build_payload(self, system_prompt, prompt):
        return {
            'model': self.model,
            'system': system_prompt,
            'prompt': prompt,
            'stream': True,
        }

    def _extract_stream_chunk(self, line):
        data = json.loads(line)
        if not data['done']:
            return data['response']
