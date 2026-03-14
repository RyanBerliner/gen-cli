#!/usr/bin/env python3

import os
import sys
import configparser

from gen.differ import Differ
from gen.utils import user_confirmation
from gen.prompt import get_system_prompt, get_edit_file_system_prompt
from gen.providers import (
    Cerebras,
    Grok,
    Ollama,
    OpenAI,
)


def generate(system_prompt, args, stream_cb, additional_content=None):
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
        case 'openai':
            Provider = OpenAI
        case unknown:
            raise Exception(f'Invalid provider {unknown}')

    provider = Provider(
        options.get('model'),
        key=options.get('key'),
        effort=options.get('effort'),
        endpoint=options.get('endpoint'),
    )

    prompt = args.prompt
    if additional_content:
        prompt = args.prompt = \
            f'<content>\n{additional_content}\n</content>\n' + \
            f'<prompt>\n{prompt}\n</prompt>'

    return provider.generate(system_prompt, prompt, stream_cb)


def process_file(args, file):
    system_prompt = get_system_prompt()
    if args.edit:
        system_prompt = get_edit_file_system_prompt()

    differ = Differ(file)
    # should probably not read the file twice like this
    file.seek(0)

    response = generate(
        system_prompt,
        args,
        stream_cb=differ.output_diff if args.edit else output_token,
        additional_content=file.read(),
    )

    if args.edit:
        doit = args.force
        if not args.force:
            doit = user_confirmation('Are you sure?')

        if doit:
            file.seek(0)
            file.write(response)
            file.truncate()
            sys.stdout.write(file.name)
        else:
            sys.stdout.write('No changes written')

    sys.stdout.write('\n')


def output_token(token):
    sys.stdout.write(token)
    sys.stdout.flush()
