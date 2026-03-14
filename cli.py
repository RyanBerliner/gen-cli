#!/usr/bin/env python3

import argparse
import sys

from gen.prompt import get_system_prompt
from gen import (
    generate,
    output_token,
    process_file,
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='gen',
        description='[gen]erate LLM completions',
    )

    parser.add_argument('prompt')
    parser.add_argument('files', nargs='*', type=argparse.FileType('r+'))
    parser.add_argument('-e', '--edit', action='store_true')
    parser.add_argument('-f', '--force', action='store_true')
    parser.add_argument('--profile', default='default')
    args = parser.parse_args()

    if len(args.files) == 0:
        system_prompt = get_system_prompt()
        additional_content = None

        if not sys.stdin.isatty():
            additional_content = sys.stdin.read()

        generate(
            system_prompt,
            args,
            stream_cb=output_token,
            additional_content=additional_content
        )

        sys.stdout.write('\n')
        exit(0)

    for file in args.files:
        process_file(args, file)
