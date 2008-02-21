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
from pychseg.utils.lrucache import lru_cache
from pychseg.utils.myitertools import joindictvalue

def idf(docFreq, numDocs):    
    return math.log(numDocs*1.0/(docFreq+1.0)) + 1.0

def tf(termFreq):
    return math.sqrt(termFreq)

allDocs = []
allTerms = {}

class Term:
    """
    >>> t = Term('test')
    >>> t.incdf()
    >>> t.termword
    'test'
    >>> t.docfreq
    1
    >>> allDocs.extend([1,3,4])    
    >>> t.idf() == math.log(3.0/2.0) + 1.0
    True
    >>> s=allDocs.pop();s=allDocs.pop();s=allDocs.pop()
    """
    def __init__(self, termword):
        self.termword = termword
        self.docfreq = 0
        # for caching         
        self._df = 0
        self._idf = 0.0
    
    def incdf(self):
        self.docfreq += 1
        
    def idf(self):
        if self._df == self.docfreq:
            return self._idf
        self._df = self.docfreq        
        self._idf = idf(self.docfreq, len(allDocs))
        return self._idf

class DocTerm:
    """
    >>> t = Term('test')
    >>> t.incdf()
    >>> dt = DocTerm(t, 3)
    >>> allDocs.extend([1,3,4])
    >>> dt.tfidf() == math.sqrt(3) * (math.log(3.0/2.0) + 1.0)
    True
    >>> dt.tfidf2() == math.pow(math.sqrt(3) * (math.log(3.0/2.0) + 1.0), 2)
    True
    >>> s=allDocs.pop();s=allDocs.pop();s=allDocs.pop()
    """    
    def __init__(self, termobj, termfreq):
        self.termobj = termobj
        self.termfreq = termfreq
        # for caching 
        self._tfidf = None
    
    # tf * idf
    def tfidf(self):
        if self._tfidf is None:
            self._tfidf = tf(self.termfreq) * self.termobj.idf()
        return self._tfidf        
    
    # sequare of tfidf
    def tfidf2(self):
        tfidf = self.tfidf()
        return tfidf * tfidf

class Document:
    """
    doc1 -> test, bingo, share, test
    doc2 -> test, write
    >>> t1 = Term('test')
    >>> t1.incdf(); t1.incdf() 
    >>> t2 = Term('bingo')
    >>> t2.incdf()
    >>> t3 = Term('share')
    >>> t3.incdf()
    >>> t4 = Term('write')
    >>> t4.incdf() 
    >>> dt11 = DocTerm(t1, 2)
    >>> dt12 = DocTerm(t2, 1)
    >>> dt13 = DocTerm(t3, 1)
    >>> dt21 = DocTerm(t1, 1)
    >>> dt22 = DocTerm(t4, 1)
    >>> d1 = Document( {'test':dt11, 'bingo':dt12, 'share':dt13} )
    >>> d2 = Document( {'test':dt21, 'write':dt22} )
    >>> allDocs.extend([d1,d2])   
    >>> d1.sum_tfidf2()
    1.6452791481550095
    >>> d2.sum_tfidf2()
    1.1633880426052334
    >>> d1.similarity(d2)
    0.26115930450350772
    >>> d2.similarity(d1)
    0.26115930450350772
    >>> s=allDocs.pop();s=allDocs.pop()
    """    
    def __init__(self, docterms):
        self.docterms = docterms
        # for caching
        self._sum_tfidf2 = None

    def sum_tfidf2(self):
        if self._sum_tfidf2 is None:            
            self._sum_tfidf2 = math.sqrt( 
                                         sum(map(lambda x:x.tfidf2(), self.docterms.values()), 
                                             0.0) 
                                         )
        return self._sum_tfidf2
    
    def similarity(self, doc):
        sum1and2 = sum( 
                       map(lambda xy:xy[0].tfidf()*xy[1].tfidf(), 
                           joindictvalue(self.docterms, doc.docterms)),
                       0.0)
        if sum1and2 < 0.00001:
            result = 0.0
        else:
            result = sum1and2 / ( self.sum_tfidf2() * doc.sum_tfidf2() )
        return result

def batch_similarity(docs, maxlen=100):
    """
    doc1 -> test, bingo, share, test
    doc2 -> test, write, wiki
    doc3 -> bingo, wiki
    >>> t1 = Term('test')
    >>> t1.incdf(); t1.incdf() 
    >>> t2 = Term('bingo')
    >>> t2.incdf(); t2.incdf()
    >>> t3 = Term('share')
    >>> t3.incdf()
    >>> t4 = Term('write')
    >>> t4.incdf() 
    >>> t5 = Term('wiki')
    >>> t5.incdf(); t5.incdf() 
    >>> dt11 = DocTerm(t1, 2)
    >>> dt12 = DocTerm(t2, 1)
    >>> dt13 = DocTerm(t3, 1)
    >>> dt21 = DocTerm(t1, 1)
    >>> dt22 = DocTerm(t4, 1)
    >>> dt23 = DocTerm(t5, 1)
    >>> dt31 = DocTerm(t2, 1)
    >>> dt32 = DocTerm(t5, 1)
    >>> d1 = Document( {'test':dt11, 'bingo':dt12, 'share':dt13} )
    >>> d2 = Document( {'test':dt21, 'write':dt22, 'wiki':dt23} )
    >>> d3 = Document( {'bingo':dt31, 'wiki':dt32} )
    >>> allDocs.extend([d1,d2,d3])   
    >>> batch_similarity(allDocs)
    [[(1, 0.31799276992267178), (2, 0.31701072958657012)], [(2, 0.35464863330313684), (0, 0.31799276992267178)], [(1, 0.35464863330313684), (0, 0.31701072958657012)]]
    >>> s=allDocs.pop();s=allDocs.pop();s=allDocs.pop()
    """
    reduced_result = []
    results = [ ]
    for d in docs:
        results.append({})
    for i, doc1 in enumerate(docs):        
        for j, doc2 in enumerate(docs[:i]):
            sim = doc1.similarity(doc2)
            results[i][j] = sim
            results[j][i] = sim
            
    # sorting and filter result    
    for r in results:
        reduced_result.append(
                               sorted( filter(lambda x:x[1]>0.0001, r.items()), lambda x,y:cmp(y[1],x[1]))[:maxlen]
                               )
    
    return reduced_result

class CosineSimilarity:     
    pass        
        
        
def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
    
        
        
        