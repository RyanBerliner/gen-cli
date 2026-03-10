#!/usr/bin/env python3
import json
import os
import sys
import requests
import configparser

from gen.utils import noop
from gen.prompt import get_file_system_prompt
from gen.providers import (
    Cerebras,
    Grok,
    Ollama,
)


def generate(system_prompt, args, stream_cb):
    config = configparser.ConfigParser()
    # not sure why we have to manually expand the home path
    config.read(os.path.expanduser('~') + '/.gen/config')
    options = config[args.profile]

    match options['provider']: 
        case 'cerebras':
            Provider = Cerebras
        case 'grok':
            Provider = Grok
        case 'ollama':
            Provider = Ollama
        case _:
            raise Exception(f'Invalid provider {_}')

    provider = Provider(
        options.get('model'),
        key=options.get('key'),
        effort=options.get('effort'),
        endpoint=options.get('endpoint'),
    )

    return provider.generate(system_prompt, args.prompt, stream_cb)


def process_file(args, file):
    response = generate(
        get_file_system_prompt(file, edit=args.edit),
        args,
        stream_cb=noop if args.edit else output_token,
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
