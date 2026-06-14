import json
import time

from unittest import TestCase

from gen.differ import HashDiffer
from gen.editor import (
    content_to_line_tree,
    debug_line_tree,
    line_tree_to_content,
    insert_new_content_after_line,
    delete_content,
    update_content,
)


class EditorTest(TestCase):
    def test_content_to_line_tree(self):
        self.assertEqual(
            content_to_line_tree('  lorem\nipsum \n\tdolor amet  '),
            [-1, '', '0000000',
             [0, '  lorem\n', 'a5ad466',
              [1, 'ipsum \n', 'b090a6c',
               [2, '\tdolor amet  ', 'a993fd6', None]]], 2]
        )

    def test_debug_line_tree(self):
        tree = content_to_line_tree('  lorem\nipsum \n\tdolor amet  ')

        self.assertEqual(
            debug_line_tree(tree),
            (
                '0000000|\n'
                'a5ad466|  lorem\n'
                'b090a6c|ipsum\n'
                'a993fd6|\tdolor amet'
            )
        )

    def test_line_tree_to_content(self):
        tree = content_to_line_tree('  lorem\nipsum \n\tdolor amet  ')

        self.assertEqual(
            line_tree_to_content(tree),
            (
                '  lorem\n'
                'ipsum \n'
                '\tdolor amet  '
            )
        )

        self.assertEqual(
            line_tree_to_content(tree, with_hashes=True),
            (
                'a5ad466|  lorem\n'
                'b090a6c|ipsum \n'
                'a993fd6|\tdolor amet  '
            )
        )

    def test_insert_new_content_after_line_middle(self):
        tree = content_to_line_tree('  lorem\nipsum \n\tdolor amet  ')

        # print(line_tree_to_content(tree, with_hashes=True))
        # also notice no trailing newline
        insert_new_content_after_line('line 1\nline 2', 'a5ad466', tree)

        self.assertEqual(
            line_tree_to_content(tree),
            (
                '  lorem\n'
                'line 1\n'
                'line 2\n'
                'ipsum \n'
                '\tdolor amet  '
            )
        )

    def test_insert_new_content_after_line_start(self):
        tree = content_to_line_tree('  lorem\nipsum \n\tdolor amet  ')
        insert_new_content_after_line('line 1', '0000000', tree)

        self.assertEqual(
            line_tree_to_content(tree),
            (
                'line 1\n'
                '  lorem\n'
                'ipsum \n'
                '\tdolor amet  '
            )
        )

    def test_insert_new_content_after_line_end(self):
        # notice that the current content does not end in a newline
        tree = content_to_line_tree('  lorem\nipsum \n\tdolor amet  ')
        # print(line_tree_to_content(tree, with_hashes=True))
        insert_new_content_after_line('line 1', 'a993fd6', tree)

        self.assertEqual(
            line_tree_to_content(tree),
            (
                '  lorem\n'
                'ipsum \n'
                '\tdolor amet  \n'
                'line 1\n'
            )
        )

    def test_delete_content_single_line(self):
        tree = content_to_line_tree('  lorem\nipsum \n\tdolor amet  ')
        # print(line_tree_to_content(tree, with_hashes=True))
        delete_content('b090a6c', 'b090a6c', tree)

        self.assertEqual(
            line_tree_to_content(tree),
            (
                '  lorem\n'
                '\tdolor amet  '
            )
        )

    def test_delete_content_multiple_lines(self):
        tree = content_to_line_tree('  lorem\nipsum \n\tdolor amet  ')
        # print(line_tree_to_content(tree, with_hashes=True))
        delete_content('b090a6c', 'a993fd6', tree)

        self.assertEqual(
            line_tree_to_content(tree),
            '  lorem\n'
        )

    def test_update_single_line(self):
        tree = content_to_line_tree('  lorem\nipsum \n\tdolor amet  ')
        # print(line_tree_to_content(tree, with_hashes=True))
        update_content('b090a6c', 'b090a6c', 'testing', tree)

        self.assertEqual(
            line_tree_to_content(tree),
            (
                '  lorem\n'
                'testing\n'
                '\tdolor amet  '
            )
        )

    def test_update_multiple_lines_1(self):
        tree = content_to_line_tree('  lorem\nipsum \n\tdolor amet  ')
        # print(line_tree_to_content(tree, with_hashes=True))
        update_content('b090a6c', 'a993fd6', 'testing', tree)

        self.assertEqual(
            line_tree_to_content(tree),
            (
                '  lorem\n'
                'testing\n'
            )
        )

    def test_update_multiple_lines_2(self):
        tree = content_to_line_tree('  lorem\nipsum \n\tdolor amet  ')
        # print(line_tree_to_content(tree, with_hashes=True))
        update_content('b090a6c', 'a993fd6', 'line 1\nline 2\nline 3', tree)

        self.assertEqual(
            line_tree_to_content(tree),
            (
                '  lorem\n'
                'line 1\n'
                'line 2\n'
                'line 3\n'
            )
        )


# This is for doing manual visual testing to see how the output looks as its
# streaming in. Run directly: `python -m test.test_editor`
if __name__ == '__main__':
    original = open('test/data/hash_edit_original.txt', 'r').read()
    update_stream = open('test/data/hash_edit_token_stream.txt', 'r')
    update_stream = json.loads(update_stream.read())

    differ = HashDiffer(original)

    for token in update_stream:
        differ.output_diff(token)
        tokens_per_second = 100
        time.sleep(1 / tokens_per_second)
