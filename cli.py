#!/usr/bin/env python3

import argparse
import sys

from gen.prompt import get_system_prompt
from gen.thinker import StdErrThinker
from gen.differ import HashDiffer, RewriteDiffer
from gen.editor import content_to_line_tree, line_tree_to_content
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
    parser.add_argument('file', nargs='?', type=argparse.FileType('r+'))
    parser.add_argument('-c', '--context-files', nargs='+',
                        type=argparse.FileType('r+'))
    parser.add_argument('-e', '--edit', action='store_true')
    parser.add_argument('-x', '--hash-edit', action='store_true')
    parser.add_argument('--profile', default='default')
    args = parser.parse_args()

    generate_kwargs = {
        'system_prompt': get_system_prompt(args),
        'user_prompt': args.prompt,
        'thinker': StdErrThinker(),
        'outputter': output_token,
        'primary_content': args.file.read() if args.file else None,
        'context_files': args.context_files if args.context_files else [],
        'profile': args.profile,
    }

    if not sys.stdin.isatty():
        # TODO: should support stdin and file content at the same time.
        #       generate should support primary file, stdin, context files
        generate_kwargs['primary_content'] = sys.stdin.read()

    file_differ = None

    if args.edit:
        file_differ = RewriteDiffer(generate_kwargs['primary_content'])
    elif args.hash_edit:
        file_differ = HashDiffer(generate_kwargs['primary_content'])
        line_tree = content_to_line_tree(generate_kwargs['primary_content'])

        generate_kwargs['primary_content'] = line_tree_to_content(
            line_tree,
            with_hashes=True
        )

    if file_differ is not None:
        generate_kwargs['outputter'] = file_differ.output_diff
        accepted = False

        while not accepted:
            accepted = process_file(args.file, file_differ, **generate_kwargs)
    else:
        generate(**generate_kwargs)

    sys.stdout.write('\n')
    exit(0)
