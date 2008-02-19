#coding:utf-8

import math
from word import Word, CJK_WORD

from pychseg.utils.lrucache import instance_cache

class Chunk:
    """
    >>> c = Chunk([Word('ab'),'de','fe'])
    >>> len(c)
    6
    >>> c.averageLength()
    2.0
    >>> c.variance()
    0.0
    >>> c = Chunk(['abc','d','fe'])
    >>> len(c)
    6
    >>> c.averageLength()
    2.0
    >>> c.variance()
    0.81649658092772603
    >>> c = Chunk([Word('ab'),Word('d',CJK_WORD,3200626),Word('fe')])
    >>> c.degreeOfMorphemicFreedom()
    14.97885697363788
    >>> c.reverseLen()
    212
    """
    def __init__(self, words):
        self.words = words
        
        self._len = None
        self._average = None 
        self._variance = None
        self._degree = None
        self._revlen = None
    
    def __len__(self):
        if self._len is None:
            self._len = sum(map(len, self.words))
        return self._len
    
    def averageLength(self):
        if self._average is None:
            self._average = float(self.__len__()) / len(self.words)
        return self._average
    
    def variance(self):
        average = self.averageLength()
        if self._variance is None:
            self._variance = math.sqrt( 
                         sum(
                             map(lambda x: math.pow(len(x)-average,2),
                                 self.words), 
                             0.0) / len(self.words)
                         )
        return self._variance
        
    def degreeOfMorphemicFreedom(self):
        if self._degree is None:
            self._degree = sum(
                        map(lambda x: math.log(x.frequency),
                            filter(lambda x:len(x)==1, self.words)),
                        0.0)
        return self._degree
        
    def reverseLen(self):
        if self._revlen is None:
            self._revlen = sum(
                               [l*i for i,l in zip([1,10,100,1000], map(len, self.words) )] 
                               )
        return self._revlen
        
    # for debugging
    def __repr__(self):        
        return '[%s]' % ','.join(map(repr, self.words))
        
def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()    