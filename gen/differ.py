import sys

from difflib import unified_diff


class Differ:
    GREEN = "\x1b[32m"
    RED = "\x1b[31m"
    RESET = "\x1b[0m"

    def __init__(self, file):
        self.start_contents = file.readlines()
        self.end_contents = ''
        self.last_diff_line_count = 0

    def output_diff(self, new_token):
        self.end_contents += new_token
        end_contents = [f'{line}\n' for line in self.end_contents.split('\n')]
        diff = unified_diff(self.start_contents, end_contents)

        for _ in range(self.last_diff_line_count):
            sys.stdout.write('\x1b[1A\x1b[2K')
            sys.stdout.flush()

        self.last_diff_line_count = 0
        for d in diff:
            self.last_diff_line_count += 1

            if d.startswith('+++') or d.startswith('---'):
                sys.stdout.write(d)
            elif d.startswith('+'):
                sys.stdout.write(f'{self.GREEN}{d}{self.RESET}')
            elif d.startswith('-'):
                sys.stdout.write(f'{self.RED}{d}{self.RESET}')
            else:
                sys.stdout.write(d)

            sys.stdout.flush()
