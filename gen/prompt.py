import os


def _get_prompt_file(filename):
    prompt_dir = os.path.join(os.path.dirname(__file__), '..', '.gen')

    with open(os.path.join(prompt_dir, filename), 'r') as file:
        return file.read()


def _edit_file_system_prompt():
    return _get_prompt_file('edit_file_system_prompt.txt')


def _edit_file_system_prompt_hash():
    return _get_prompt_file('edit_file_system_prompt_hash.txt')


def _default_system_prompt():
    return _get_prompt_file('system_prompt.txt')


def get_system_prompt(args):
    if args.edit:
        return _edit_file_system_prompt()

    if args.hash_edit:
        return _edit_file_system_prompt_hash()

    return _default_system_prompt()
