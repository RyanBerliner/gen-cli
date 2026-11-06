from contextlib import redirect_stderr
from io import StringIO
from time import sleep
from unittest import TestCase

from gen.thinker import StdErrThinker


class StdErrThinkerTest(TestCase):
    def test_thinker(self):
        stderr = StringIO()
        thinker = StdErrThinker()

        with redirect_stderr(stderr):
            thinker.progress()
            self.assertEqual(stderr.getvalue(), 'thinking ...')

            thinker.progress()
            self.assertEqual(stderr.getvalue(), 'thinking ....')

            thinker.progress()
            self.assertEqual(stderr.getvalue(), 'thinking .....')

            thinker.done()
            self.assertEqual(stderr.getvalue(), 'thinking .....\r\033[K')


# This is for doing manual testing
# Run directly: `python -m test.test_thinker`
if __name__ == '__main__':
    thinker = StdErrThinker()

    thinker.progress()
    sleep(1)
    thinker.progress()
    sleep(1)
    thinker.progress()
    sleep(1)
    thinker.done()
