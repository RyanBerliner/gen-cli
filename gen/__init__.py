import os
import sys
import configparser

from gen.utils import user_selection
from gen.providers import (
    Cerebras,
    Grok,
    Ollama,
    OpenAI,
)


def generate(
    user_prompt='',
    system_prompt='',
    outputter=None,
    thinker=None,
    profile=None,
    context_stdin=None,
    context_primary_file_content=None,
    context_supporting_files=None,
):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.expanduser('~'), '.gen', 'config'))
    options = config[profile]
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

    if context_stdin is not None:
        prompt += \
            '<stdin_context>\n' + \
            f'{context_stdin}\n' + \
            '</stdin_context>\n\n'

    if context_supporting_files is not None:
        for context_file in context_supporting_files:
            context_file.seek(0)
            prompt += \
                '<supporting_file_context>\n' + \
                f'<file_name>{context_file.name}</file_name>\n' + \
                f'{context_file.read()}\n' + \
                '</supporting_file_context>\n\n'

    if context_primary_file_content is not None:
        prompt += \
            '<primary_file_context>\n' + \
            f'{context_primary_file_content}\n' + \
            '</primary_file_context>\n\n'

    prompt += user_prompt

    return provider.generate(
        system_prompt,
        prompt,
        outputter,
        thinker,
    )


def edit_file(file, differ, **generate_kwargs):
    response = generate(**generate_kwargs)
    differ.show_diff()

    selection = user_selection(f'\nConfirm changes to {file.name}', {
        'y': True,
        'n': False,
        '*': 5,
    })

    if selection is True:
        new_content = differ.applied_diff(response)

        file.seek(0)
        file.write(new_content)
        file.truncate()

        sys.stdout.write(file.name)
        return True

    elif selection is False:
        sys.stdout.write('No changes written')
        return True

    else:
        generate_kwargs['user_prompt'] += f'\n\n{selection}'
        generate_kwargs['thinker'].reset()
        differ.reset()
        return edit_file(file, differ, **generate_kwargs)


def output_token(token):
    sys.stdout.write(token)
    sys.stdout.flush()
