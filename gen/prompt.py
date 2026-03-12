import os


def get_edit_file_system_prompt():
    filename = '~/.gen/edit_file_system_prompt.txt'

    with open(os.path.expanduser(filename), 'r') as file:
        return file.read()


def get_system_prompt():
    with open(os.path.expanduser('~/.gen/system_prompt.txt'), 'r') as file:
        return file.read()
