import os
import sys
import configparser

from gen.differ import RewriteDiffer, HashDiffer
from gen.editor import content_to_line_tree, line_tree_to_content
from gen.utils import user_selection
from gen.thinker import StdErrThinker
from gen.providers import (
    Cerebras,
    Grok,
    Ollama,
    OpenAI,
)


def generate(
    system_prompt,
    args,
    output_token_cb,
    thinker,
    additional_content=None
):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.expanduser('~'), '.gen', 'config'))
    options = config[args.profile]
    model = options.get('model')
    effort = options.get('effort')

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
        model,
        key=options.get('key'),
        effort=effort,
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

    return provider.generate(
        system_prompt,
        prompt,
        output_token_cb,
        thinker,
    )


def process_file(system_prompt, args, file):
    is_editting = args.edit or args.hash_edit

    content = file.read()
    differ = HashDiffer(content) if args.hash_edit else \
        RewriteDiffer(content)

    if args.hash_edit:
        tree = content_to_line_tree(content)
        tree_content = line_tree_to_content(tree, with_hashes=True)
        content = tree_content

    response = generate(
        system_prompt,
        args,
        output_token_cb=differ.output_diff if is_editting else output_token,
        thinker=StdErrThinker(),
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
            process_file(system_prompt, args, file)
            return

    sys.stdout.write('\n')


def output_token(token):
    sys.stdout.write(token)
    sys.stdout.flush()
