try:
    from xail.engine.base import BaseEngine
except ImportError:
    BaseEngine = object
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
from contextlib import closing
import random


class GenericEngine(BaseEngine):
    """The generic engine that responds with
       one-size-fit-all-but-useless answers"""
    def __init__(self, file=None):
        self.data = {"I don't understand.",
                     "I can't seem to understand.",
                     'Wait, I got a phone call.',
                     'Oh, my keyboard hung again.',
                     'Sorry, my computer lagged.'}
        if file:
            with open(file) as file:
                self.data.update(i.strip() for i in file)
        self._loaded_from_file = file is not None
        self.file = file
        self.data = list(self.data)
    
    @property
    def loaded_from_file(self):
        return self._loaded_from_file

    def close(self):
        pass
    
    def __del__(self):
        self.close()

    def add_entry(self, line, resp):
        self.data.extend(resp)

    def load(self, file):
        if isinstance(file, basestring):
            file = closing(StringIO(file))
        with file as file:
            for line in file:
                self.data.append(line.strip())
    
    def output(self, input, context=None):
        return [(x, 0.0) for x in self.data]
    
    def final(self, input, context=None):
        try:
            return random.choice(self.data)
        except IndexError:
            return

if __name__ == '__main__':
    from pprint import pprint
    engine = GenericEngine()
    pprint(engine.data)
    pprint(engine.output('x'))
    print engine.final('x')
