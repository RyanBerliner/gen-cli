from unittest import TestCase

from gen.editor import (
    content_to_line_tree,
    complete_line_tree,
    line_tree_to_content,
)


class EditorTest(TestCase):
    def test_content_to_line_tree(self):
        self.assertEqual(
            content_to_line_tree('  lorem\nipsum \n\tdolor amet  '),
            [-1, '',
             [0, '  lorem\n',
              [1, 'ipsum \n',
               [2, '\tdolor amet  ', None]]], 2]
        )

    def test_complete_line_tree(self):
        tree = content_to_line_tree('  lorem\nipsum \n\tdolor amet  ')

        self.assertEqual(
            complete_line_tree(tree),
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
