import os
import sys
import configparser

from gen.differ import RewriteDiffer, HashDiffer
from gen.editor import content_to_line_tree, line_tree_to_content
from gen.utils import user_selection
from gen.prompt import (
    get_edit_file_system_prompt,
    get_edit_file_system_prompt_hash,
    get_system_prompt,
)
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

    prompt = ''
    if args.context_files is not None:
        for context_file in args.context_files:
            prompt += \
                '<file_context>\n' + \
                f'<file_name>{context_file.name}</file_name>\n' + \
                f'{context_file.read()}\n' + \
                '</file_context>\n\n'

    if additional_content:
        prompt += \
            '<primary_content>\n' + \
            f'{additional_content}\n' + \
            '</primary_content>\n' + \
            f'<prompt>\n{args.prompt}\n</prompt>'
    else:
        prompt += args.prompt

    return provider.generate(system_prompt, prompt, stream_cb)


def process_file(args, file):
    system_prompt = get_system_prompt()

    if args.edit:
        system_prompt = get_edit_file_system_prompt()
    if args.experimental_edit:
        system_prompt = get_edit_file_system_prompt_hash()

    is_editting = args.edit or args.experimental_edit

    content = file.read()
    differ = HashDiffer(content) if args.experimental_edit else \
        RewriteDiffer(content)

    if args.experimental_edit:
        tree = content_to_line_tree(content)
        tree_content = line_tree_to_content(tree, with_hashes=True)
        content = tree_content

    response = generate(
        system_prompt,
        args,
        stream_cb=differ.output_diff if is_editting else output_token,
        additional_content=content,
    )

    if is_editting:
        selection = args.force
        if not args.force:
            differ.show_diff()
            selection = user_selection(f'\nConfirm changes to {file.name}', {
                'y': True,
                'n': False,
                '*': 5,
            })

        if selection is True:
            new_content = response if args.edit else \
                    line_tree_to_content(differ.tree)

            file.seek(0)
            file.write(new_content)
            file.truncate()

            sys.stdout.write(file.name)
        elif selection is False:
            sys.stdout.write('No changes written')
        else:
            file.seek(0)
            if args.context_files is not None:
                for context_file in args.context_files:
                    context_file.seek(0)

            args.prompt += f'\n\n{selection}'
            process_file(args, file)
            return

    sys.stdout.write('\n')


def output_token(token):
    sys.stdout.write(token)
    sys.stdout.flush()
