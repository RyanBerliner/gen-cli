import json

from gen.providers.base_provider import BaseProvider


class OpenAI(BaseProvider):
    endpoint = 'https://api.openai.com/v1/responses'

    def _build_payload(self, system_prompt, prompt):
        return {
            'model': self.model,
            'stream': True,
            'reasoning': {'effort': self.effort},
            'input': [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': prompt},
            ],
            # by default, the responses endpoint saves responses
            # settings store=False disables this
            'store': False,
        }

    def _extract_stream_event(self, line):
        line = line.decode('utf-8')
        if not line.startswith('data: '):
            return None

        return json.loads(line[6:])

    def _extract_output_token(self, line):
        if data := self._extract_stream_event(line):
            if data.get('type') == 'response.output_text.delta':
                return data.get('delta', None)

    def _is_thinking_progress(self, line):
        if data := self._extract_stream_event(line):
            if data.get('type') != 'response.output_item.added':
                return False

            if data.get('item', {}).get('type', None) != 'reasoning':
                return False

            return True
