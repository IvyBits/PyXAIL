from contextlib import closing
from io import StringIO
from operator import itemgetter
from xail.engine import *
import random

DEBUG_MODE = False


class XAIL(object):
    """Basic XAIL Engine"""

    def __init__(self):
        self.regex   = RegexEngine()
        self.substr  = SubstringEngine()
        self.matrix  = MatrixEngine()
        self.generic = GenericEngine()
        self.enginemap = {'#': self.matrix.add_entry,
                          '@': self.substr.add_entry,
                          '!': self.regex.add_entry}
        self.engines = [self.regex, self.substr, self.matrix, self.generic]

    def feed(self, file):
        if isinstance(file, basestring):
            file = closing(StringIO(file))
        engine_map = self.enginemap
        engine_chars = tuple(engine_map.keys())
        resp = []
        last = ''
        add_entry = None
        multiline = False
        add_resp = resp.append

        with file as file, self.matrix, self.substr, self.regex:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                elif line[0] == ';':
                    continue
                elif line.startswith(engine_chars):
                    if resp and add_entry is not None:
                        add_entry(last, resp)
                        del resp[:]
                    last = line[1:].strip()
                    if last:
                        add_entry = engine_map[line[0]]
                    else:
                        add_entry = self.generic.add_entry
                else:
                    if not line[-1] == '\\':
                        new_multiline = False
                    else:
                        stripped = line.rstrip('\\')
                        count = len(line) - len(stripped)
                        new_multiline = count & 1
                        line = stripped + '\\' * (count // 2)
                    if multiline:
                        resp[-1] += line
                    else:
                        add_resp(line)
                    multiline = new_multiline
            if resp and add_entry is not None:
                add_entry(last, resp)

    def results(self, input):
        out = []
        for engine in self.engines:
            o = engine.output(input)
            if o is not None:
                out.extend(o)
        out.sort(key=itemgetter(1), reverse=True)
        return out

    def final(self, input):
        data = self.results(input)
        if not data:
            return None
        if DEBUG_MODE:
            for content, probability in data:
                print '%.6f: %s' % (probability, content)
        kazi = data[0][1]  # The first entry always has the max
        data = [x for x in data if x[1] == kazi]
        return random.choice(data)[0]
