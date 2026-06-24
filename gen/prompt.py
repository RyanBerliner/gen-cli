import os


def _get_prompt_file(filename):
    prompt_dir = os.path.join(os.path.dirname(__file__), '..', '.gen')

    with open(os.path.join(prompt_dir, filename), 'r') as file:
        return file.read()


def get_edit_file_system_prompt():
    return _get_prompt_file('edit_file_system_prompt.txt')


def get_edit_file_system_prompt_hash():
    return _get_prompt_file('edit_file_system_prompt_hash.txt')


def get_system_prompt():
    return _get_prompt_file('system_prompt.txt')
