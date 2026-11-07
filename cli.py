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
    edit_file,
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
        'user_prompt': args.prompt,
        'system_prompt': get_system_prompt(args),
        'thinker': StdErrThinker(),
        'outputter': output_token,
        'profile': args.profile,
        'context_stdin': None,
        'context_primary_file_content': None,
        'context_supporting_files': args.context_files,
    }

    if args.file is not None:
        generate_kwargs['context_primary_file_content'] = args.file.read()

    if not sys.stdin.isatty():
        generate_kwargs['context_stdin'] = sys.stdin.read()

    file_differ = None

    if args.edit or args.hash_edit and args.file:
        file_contents = generate_kwargs['context_primary_file_content']

        if args.edit:
            file_differ = RewriteDiffer(file_contents)
        elif args.hash_edit:
            file_differ = HashDiffer(file_contents)
            line_tree = content_to_line_tree(file_contents)

            generate_kwargs['context_primary_file_content'] = \
                line_tree_to_content(
                    line_tree,
                    with_hashes=True
                )

    if file_differ is not None:
        generate_kwargs['outputter'] = file_differ.output_diff
        accepted = False

        while not accepted:
            accepted = edit_file(args.file, file_differ, **generate_kwargs)
    else:
        generate(**generate_kwargs)

    sys.stdout.write('\n')
    exit(0)
