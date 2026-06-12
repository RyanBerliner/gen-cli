from unittest import TestCase

from gen.editor import (
    content_to_line_tree,
    debug_line_tree,
    line_tree_to_content,
    insert_new_content_after_line,
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

        # notice that there is no newline inserted after "line 1" since its the
        # last line anyway
        self.assertEqual(
            line_tree_to_content(tree),
            (
                '  lorem\n'
                'ipsum \n'
                '\tdolor amet  \n'
                'line 1'
            )
        )
