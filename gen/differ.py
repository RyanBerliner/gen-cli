import json
import sys

from difflib import unified_diff

from .editor import (
    content_to_line_tree,
    delete_content,
    insert_new_content_after_line,
    line_tree_to_content,
    update_content,
)


class BaseDiffer:
    pass


class RewriteDiffer(BaseDiffer):
    GREEN = "\x1b[32m"
    RED = "\x1b[31m"
    RESET = "\x1b[0m"

    def __init__(self, file_content):
        self.start_contents = file_content.splitlines(keepends=True)
        self.end_contents = ''

    def show_diff(self, final=True):
        end_contents = [f'{line}\n' for line in self.end_contents.split('\n')]
        diff = unified_diff(self.start_contents, end_contents)

        # if this is the not the final diff we should assume that the last
        # chunk of subtracted lines is probably because we haven't gotten there
        # yet. so, lets hide the last group of subtracted lines and anything
        # after it. this does mean the the diff numbers are going to be wrong,
        # and some this won't always be the optimal strategy, but generally
        # it'll show a more comprehendible diff streaming in that doesnt look
        # like the entire thing is being rewritten. its not about showing
        # correct snapshots, its about showing a reasonble timeline of
        # progress as tokens stream in
        filtered_diff = list(diff)
        if not final and len(filtered_diff):
            filtered_diff.reverse()
            first = filtered_diff[0]

            while first and first.startswith('+') or first.startswith('-'):
                first = filtered_diff.pop(0)

            filtered_diff.reverse()

        for d in filtered_diff:
            if d.startswith('+++') or d.startswith('---'):
                sys.stdout.write(d)
            elif d.startswith('+'):
                sys.stdout.write(f'{self.GREEN}{d}{self.RESET}')
            elif d.startswith('-'):
                sys.stdout.write(f'{self.RED}{d}{self.RESET}')
            else:
                sys.stdout.write(d)

            sys.stdout.flush()

    def output_diff(self, new_token):
        self.end_contents += new_token

        # use the alt screen because the diff could (and most like will)
        # shrink. not using the alt screen in this case could mess with
        # scrollback history, especially in tmux

        # enter alt screen
        sys.stdout.write('\x1b[?1049h')
        # hide cursor
        sys.stdout.write('\x1b[?25l')
        # clear to the end
        sys.stdout.write('\x1b[?1049h')
        # move to top left
        sys.stdout.write('\x1b[0;0H')

        self.show_diff(final=False)

        # show cursor
        sys.stdout.write('\x1b[?25h')
        # leave alt screen
        sys.stdout.write('\x1b[?1049l')


class HashDiffer(BaseDiffer):
    GREEN = "\x1b[32m"
    RED = "\x1b[31m"
    RESET = "\x1b[0m"

    def __init__(self, file_contents):
        self.start_contents = file_contents.splitlines(keepends=True)
        self.tree = content_to_line_tree(file_contents)
        self.applied_ops_count = 0
        self.ops_content = ''

    def show_diff(self, final=True):
        ops = self.ops_content.splitlines()
        valid_ops = []
        for op in ops:
            try:
                valid_op = json.loads(op)
                valid_ops.append(valid_op)
            except Exception:
                continue

        if not final and len(valid_ops) <= self.applied_ops_count:
            return

        for op in valid_ops[self.applied_ops_count:]:
            op_type = op.get('op')
            start = op.get('start')
            end = op.get('end')
            new_content = op.get('newContent')

            if op_type == 'DELETE':
                delete_content(start, end, self.tree)
            elif op_type == 'UPDATE':
                update_content(start, end, new_content, self.tree)
            elif op_type == 'INSERT_AFTER':
                insert_new_content_after_line(new_content, start, self.tree)

        self.applied_ops_count += 1

        end_contents = line_tree_to_content(self.tree).splitlines(keepends=True)
        diff = unified_diff(self.start_contents, end_contents)

        for d in list(diff):
            if d.startswith('+++') or d.startswith('---'):
                sys.stdout.write(d)
            elif d.startswith('+'):
                sys.stdout.write(f'{self.GREEN}{d}{self.RESET}')
            elif d.startswith('-'):
                sys.stdout.write(f'{self.RED}{d}{self.RESET}')
            else:
                sys.stdout.write(d)

            sys.stdout.flush()

    def output_diff(self, new_token):
        self.ops_content += new_token

        # use the alt screen because the diff could (and most like will)
        # shrink. not using the alt screen in this case could mess with
        # scrollback history, especially in tmux

        # enter alt screen
        sys.stdout.write('\x1b[?1049h')
        # hide cursor
        sys.stdout.write('\x1b[?25l')
        # clear to the end
        sys.stdout.write('\x1b[?1049h')
        # move to top left
        sys.stdout.write('\x1b[0;0H')

        self.show_diff(final=False)

        # show cursor
        sys.stdout.write('\x1b[?25h')
        # leave alt screen
        sys.stdout.write('\x1b[?1049l')
