import sys


class BaseThinker:
    def progress(self):
        raise NotImplementedError

    def done(self):
        raise NotImplementedError

    def reset(self):
        raise NotImplementedError


class QuietThinker:
    def progress(self):
        pass

    def done(self):
        pass

    def reset(self):
        pass


class StdErrThinker(BaseThinker):
    def __init__(self):
        self.progress_count = 0

    def progress(self):
        if self.progress_count == 0:
            sys.stderr.write('thinking ..')

        sys.stderr.write('.')
        sys.stderr.flush()

        self.progress_count += 1

    def done(self):
        sys.stderr.write('\r\033[K')
        sys.stderr.flush()

    def reset(self):
        self.progress_count = 0
