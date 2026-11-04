#!/usr/bin/env python3

import argparse
import sys

from gen.prompt import get_system_prompt
from gen import (
    generate,
    output_token,
    thinking_token,
    process_file,
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='gen',
        description='[gen]erate LLM completions',
    )

    parser.add_argument('prompt')
    parser.add_argument('file', nargs='?', type=argparse.FileType('r+'))
    parser.add_argument('-c', '--context-files', nargs='+',
                        type=argparse.FileType('r+'))
    parser.add_argument('-e', '--edit', action='store_true')
    parser.add_argument('-x', '--hash-edit', action='store_true')
    parser.add_argument('-f', '--force', action='store_true')
    parser.add_argument('--profile', default='default')
    args = parser.parse_args()

    system_prompt = get_system_prompt(args)

    additional_content = None
    if not sys.stdin.isatty():
        additional_content = sys.stdin.read()

    if args.file is None:
        generate(
            system_prompt,
            args,
            output_token_cb=output_token,
            thinking_token_cb=thinking_token,
            additional_content=additional_content
        )

        sys.stdout.write('\n')
        exit(0)

    process_file(system_prompt, args, args.file)
