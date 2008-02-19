#coding:utf-8

from pychseg.utils.myitertools import takemost 


def filter(chunks):
    """
    >>> from word import Word
    >>> from chunk import Chunk
    >>> first = Chunk([Word('ab'),Word('b',frequency=3200626),Word('ab')])
    >>> chunks = [ first, Chunk([Word('a',frequency=224073),Word('zb'),Word('as')]) ]
    >>> r = filter(chunks)
    >>> len(r)
    1
    >>> r[0] == first
    True
    """    
    return takemost(lambda x:x.degreeOfMorphemicFreedom(), chunks)

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()   