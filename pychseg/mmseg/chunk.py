#coding:utf-8

#
#Copyright (c) 2008, Chris Song
#
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
#    * Neither the name of the <ORGANIZATION> nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#"AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

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