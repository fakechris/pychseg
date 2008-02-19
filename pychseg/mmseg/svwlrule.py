#coding:utf-8

from pychseg.utils.myitertools import takemost 


def filter(chunks):
    """
    >>> from word import Word
    >>> from chunk import Chunk
    >>> first = Chunk([Word('ab'),Word('ab'),Word('ab')])
    >>> chunks = [ first, Chunk([Word('abc'),Word('b'),Word('as')]) ]
    >>> r = filter(chunks)
    >>> len(r)
    1
    >>> r[0] == first
    True
    """    
    return takemost(lambda x:x.variance(), chunks, reverse=False)

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()   