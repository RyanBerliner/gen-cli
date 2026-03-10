import os


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
