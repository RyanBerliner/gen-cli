#!/usr/bin/env python3
import json
import os
import sys
import requests
import configparser

from gen.providers import (
    Cerebras,
    Ollama,
)


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

    Provider = None

    match options['provider']: 
        case 'ollama':
            Provider = Ollama
        case 'cerebras':
            Provider = Cerebras
        case _:
            raise Exception(f'Invalid provider {_}')

    provider = Provider(options)
    return provider.generate(system_prompt, args, stream_cb)


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
