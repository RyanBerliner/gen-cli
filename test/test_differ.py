import argparse
import json
import time

from unittest import TestCase

from gen.differ import RewriteDiffer, HashDiffer


class DifferTest(TestCase):
    def test_differ(self):
        # Nothing worth testing programatically at the moment
        pass


def try_hash_differ():
    original = open('test/data/hash_edit_original.txt', 'r').read()
    update_stream = open('test/data/hash_edit_token_stream.txt', 'r')
    update_stream = json.loads(update_stream.read())

    differ = HashDiffer(original)

    for token in update_stream:
        differ.output_diff(token)
        tokens_per_second = 100
        time.sleep(1 / tokens_per_second)


def try_rewrite_differ():
    original = open('test/data/differ_sample_original.txt', 'r').read()
    update_stream = open('test/data/differ_sample_update_stream.txt', 'r')
    update_stream = json.loads(update_stream.read())

    differ = RewriteDiffer(original)

    for token in update_stream:
        differ.output_diff(token)
        tokens_per_second = 300
        time.sleep(1 / tokens_per_second)

    differ.show_diff()


# This is for doing manual visual testing to see how the output looks as its
# streaming in. Run directly: `python -m test.test_differ --rewrite|hash`
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--rewrite', action='store_true')
    group.add_argument('--hash', action='store_true')
    args = parser.parse_args()

    if args.rewrite:
        try_rewrite_differ()
    elif args.hash:
        try_hash_differ()
