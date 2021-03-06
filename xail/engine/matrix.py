from difflib import SequenceMatcher
from functools import partial
from operator import itemgetter, contains, methodcaller
from xail.stringutils import strip_clean
from xail.keywords import keywords
from itertools import imap

try:
    from xail.engine.substring import SubstringEngine
except ImportError:
    # Try to find SubstringEngine when ran as a script
    from substring import SubstringEngine


class MatrixEngine(SubstringEngine):
    """Matrix Engine: exactly same as SubstringEngine,
       except order and position doesn't matter"""

    def __init__(self, *args):
        SubstringEngine.__init__(self, *args)
        self.state = set()

    def search(self, input):
        """Returns tuple(index:str, resp:list, priority:float)
        
        Note that this method doesn't conform the ABC, you should only use
        it for debugging purpose or you are ONLY using this engine"""
        data = {}
        for index, resp in self._search_db(input):
            key = frozenset(index.split())
            resp = resp.split('\f')
            if key in data:
                data[key].extend(resp)
            else:
                data[key] = resp
        diff = SequenceMatcher(partial(contains, '?,./<>`~!@#$%&*()_+-={}[];:\'"|\\'), input + ' '.join(self.state))
        cleaned = strip_clean(input.lower())
        cleaned_words = cleaned.split()
        words = self.state.union(cleaned_words)

        def matches(entry):
            for key in entry[0]:
                if not any(imap(methodcaller('startswith', key), words)):
                    return False
            return True

        def getdiff(text):
            diff.set_seq2(text)
            return diff.ratio()

        data = filter(matches, data.iteritems())
        data = [(index, resp, getdiff(' '.join(sorted(index, key=cleaned.find))))
                for index, resp in data]
        data.sort(key=itemgetter(2), reverse=True)
        self.state = keywords(input)
        return data

if __name__ == '__main__':
    engine = MatrixEngine()
    engine.load("""\
#This file is based on Jon Skeet facts

#HELLO WORLD
Said Hello to World.

#FIRST JON SKEET
Jon Skeet's first words are "Let there be light" apparently.

#NAME ANONYMOUS METHOD
Anonymous methods and anonymous types are really all called Jon Skeet. They just don't like to boast.

#JON SKEET CODING CONVENTION
Jon Skeet's code doesn't follow a coding convention. It is the coding convention.

#BOTTLENECK PERFORMANCE
Jon Skeet doesn't have performance bottlenecks. He just makes the universe wait its turn.

#ACCEPT JON SKEET
Users don't mark Jon Skeet's answers as accepted. The universe accepts them out of a sense of truth and justice.

#DIVIDE ZERO
Jon Skeet and only Jon Skeet can divide by zero.

#JON SKEET FAIL COMPILE
When Jon Skeet's code fails to compile the compiler apologises.

#JON SKEET NULL
When Jon Skeet points to null, null quakes in fear.
""")
    while True:
        input = unicode(raw_input('>>> '), 'mbcs', 'ignore')
        for index, resps, diff in engine.search(input):
            print 'Index:', index
            print 'Diff:', diff
            print 'Responses:'
            for resp in resps:
                print '  - ', resp
            print
