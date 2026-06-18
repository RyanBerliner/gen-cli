from unittest import TestCase

from gen.utils import user_selection


class UtilsTest(TestCase):
    def test_utils(self):
        # Nothing worth testing programatically at the moment
        pass


# This is for doing manual testing
# Run directly: `python -m test.test_utils`
if __name__ == '__main__':
    answer = user_selection('default options')
    print('selction:', answer)

    answer = user_selection('custom options', {
        'y': True,
        'n': False,
        '*': 10,
    })
    print('selection:', answer)
