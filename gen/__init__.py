#!/usr/bin/env python3
import json
import os
import sys
import requests
import configparser


def get_file_system_prompt(user_file, edit=False):
    prompt_file = 'edit_file_system_prompt' if edit else \
            'file_system_prompt'

    with open(os.path.expanduser(f'~/.gen/{prompt_file}.txt'), 'r') as file:
        system_prompt = file.read()

    system_prompt = system_prompt.replace('<file_name>', file.name)
    return system_prompt.replace('<file_contents>', user_file.read())


def get_system_prompt():
    with open(os.path.expanduser('~/.gen/system_prompt.txt'), 'r') as file:
        return file.read()


def get_content_system_prompt(content):
    with open(os.path.expanduser('~/.gen/content_system_prompt.txt'), 'r') as file:
        system_prompt = file.read()

    return system_prompt.replace('<content>', content)


def generate(system_prompt, args, stream_cb):
    config = configparser.ConfigParser()
    # not sure why we have to manually expand the home path
    config.read(os.path.expanduser('~') + '/.gen/config')
    options = config[args.profile]

    headers = {}
    json_payload = {
        'model': options['model'],
        'stream': stream_cb is not None
    }

    endpoint = ''

    if options['provider'] == 'ollama':
        endpoint = options['endpoint'] + '/api/generate'
        json_payload['system'] = system_prompt
        json_payload['prompt'] = args.prompt
    if options['provider'] == 'cerebras':
        endpoint = 'https://api.cerebras.ai/v1/chat/completions'
        headers['Authorization'] = f'Bearer {options["key"]}'
        if options['effort']:
            json_payload['reasoning_effort'] = options['effort']
        json_payload['messages'] = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': args.prompt},
        ]

    response = requests.post(
        endpoint,
        headers=headers,
        json=json_payload,
        stream=stream_cb is not None,
    )

    if not stream_cb:
        return response.json()['response']

    full_response = ''
    for line in response.iter_lines():
        if not line:
            continue

        if options['provider'] == 'cerebras':
            line = line[6:]

        data = json.loads(line)

        if options['provider'] == 'cerebras':
            choices = data.get('choices', [])
            if len(choices) > 0:
                content = choices[0].get('delta', {}).get('content', '')
                full_response += content
                stream_cb(content)

        if options['provider'] == 'ollama':
            if not data['done']:
                full_response += data['response']
                stream_cb(data['response'])

    return full_response


def process_file(args, file):
    def loading(_):
        pass

    response = generate(
        get_file_system_prompt(file, edit=args.edit),
        args,
        stream_cb=loading if args.edit else output_token,
    )

    if args.edit:
        file.seek(0)
        file.write(response)
        file.truncate()
        sys.stdout.write(file.name)

    sys.stdout.write('\n')


def output_token(token):
    sys.stdout.write(token)
    sys.stdout.flush()
