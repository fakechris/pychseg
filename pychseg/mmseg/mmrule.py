#coding:utf-8

from pychseg.utils.myitertools import takemost 

def filter(chunks):
    """
    >>> from word import Word
    >>> from chunk import Chunk
    >>> first = Chunk([Word('abc')])
    >>> chunks = [first , Chunk([Word('ab')]), Chunk([Word('a')]), Chunk([Word('a')]), Chunk([Word('a')])]
    >>> r = filter(chunks)
    >>> len(r)
    1
    >>> r[0] == first
    True
    >>> chunks = [ Chunk([Word('aa'),Word('bb'),Word('cc')]), Chunk([Word('a'),Word('b'),Word('c'),Word('d'),Word('f'),Word('e')]), Chunk([Word('aa'),Word('bb'),Word('c')]), Chunk([Word('a'),Word('b'),Word('c')]) ]
    >>> r = filter(chunks)
    >>> len(r)
    2
    """    
    return takemost(len, chunks)

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()   