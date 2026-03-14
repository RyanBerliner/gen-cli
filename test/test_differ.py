import json
import time

from unittest import TestCase

from gen.differ import Differ


class DifferTest(TestCase):
    def test_differ(self):
        # Nothing worth testing programatically at the moment
        pass


# This is for doing manual visual testing to see how the output looks as its
# streaming in. Run directly: `python -m test.test_differ`
if __name__ == '__main__':
    original = open('test/data/differ_sample_original.txt', 'r')
    update_stream = open('test/data/differ_sample_update_stream.txt', 'r')
    update_stream = json.loads(update_stream.read())

    differ = Differ(original)

    for token in update_stream:
        differ.output_diff(token)
        time.sleep(0.025)
