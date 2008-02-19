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

import logging

from word import Word, BASICLATIN_WORD, CJK_WORD, UNRECOGNIZED
from chunk import Chunk

import worddict, config
import mmrule, lawlrule, svwlrule, lsdmfocwrule, revlenrule

class Ambiguity(Exception):
    pass

def is_basic_latin(c):
    h = ord(c)
    return h >= 32 and h <= 127

def find_match_word_cache():
    def decorating_function(f):
        def wrapper(*args):
            obj = args[0]; pos = args[1]
            _cache = obj._find_cache
            
            # search it
            for c in _cache:
                if pos == c[0]:
                    wrapper.hits += 1
                    return c[1]
            # not found in cache
            result = f(*args)
            _cache.append((pos, result))
            if len(_cache) > 4:
                _cache.pop(0)            
            wrapper.misses += 1            
            return result
        wrapper.__doc__ = f.__doc__
        wrapper.__name__ = f.__name__
        wrapper.hits = wrapper.misses = 0
        return wrapper
    return decorating_function
                                  
class Algorithm:
    def __init__(self, text):
        self.word_dict = worddict.load_dict()
        self.text = text
        self.pos = 0
        self.length = len(self.text)
        
        self._find_cache = []
                
    def segment(self):
        while 1:
            w = self.next_token()
            if not w:
                return
            yield w
                
    def next_token(self):
        if self.pos >= self.length:
            return None
        c = self.text[self.pos]
        w = self.get_basic_latin_word()
        if w:
            return w
        else:
            chunks = self.create_chunks()
            if len(chunks):
                word = self.get_cjk_words(chunks)
                self.pos += len(word)
                return word
            else:
                return None
    
    def create_chunks(self): pass
            
    def get_basic_latin_word(self):
        """
        >>> a = Algorithm('abc def c')
        >>> a.get_basic_latin_word()
        abc
        >>> a.get_basic_latin_word()
        def
        >>> a.get_basic_latin_word()
        c
        >>> a = Algorithm('abc 我 c')
        >>> a.get_basic_latin_word()
        abc
        >>> a.get_basic_latin_word()
        """
        basicLatinWord = [] 
        while (self.pos < self.length and is_basic_latin(self.text[self.pos])):
            current_char = self.text[self.pos]
            self.pos += 1
            if current_char.isspace():
                if len(basicLatinWord):
                    return Word(u''.join(basicLatinWord), BASICLATIN_WORD)
            basicLatinWord.append(current_char)            
        if len(basicLatinWord):
            return Word(u''.join(basicLatinWord), BASICLATIN_WORD)
        else:
            return None
    
    def get_cjk_words(self, chunks):
        filters = [mmrule.filter, lawlrule.filter, svwlrule.filter, lsdmfocwrule.filter, revlenrule.filter]
        
        for filter in filters:
            chunks = filter(chunks) 
            if len(chunks) < 2:
                break
            
        if len(chunks) > 1:
            logging.warn( "Ambiguity words: %s" % chunks )            
            raise Ambiguity
        
        word = chunks[0].words[0]
        return word

    @find_match_word_cache()
    def find_match_word(self, pos):
        match_words = []
        
        c = self.text[pos]
        if self.word_dict.has_key(c):
            match_words.append(self.word_dict[c])
            
        for i in range(1, config.WORD_MAX_LENGTH):
            if pos+i == self.length or is_basic_latin(self.text[pos+i]):
                break
            temp = self.text[pos:pos+i+1]
            if self.word_dict.has_key(temp):
                match_words.append(self.word_dict[temp])
        
        if not len(match_words):    
            match_words.append( Word(c, UNRECOGNIZED) )
        return match_words
    
class SimpleAlgorithm(Algorithm):
    def create_chunks(self):
        return map(lambda x: Chunk([x]), self.find_match_word(self.pos))    
    
class ComplexAlgorithm(Algorithm):    
    def create_chunks(self):
        _pos=self.pos; _len=len; _length=self.length
        chunks = []
        
        words = self.find_match_word(_pos)
        for w0 in words:
            index0 = _pos+_len(w0)
            if index0 < _length:
                words1 = self.find_match_word(index0)
                for w1 in words1:
                    index1 = index0+_len(w1)
                    if index1 < _length:
                        words2 = self.find_match_word(index1)
                        for w2 in words2:
                            if w2.wtype == UNRECOGNIZED:
                                chunks.append(Chunk([w0,w1]))
                            else:
                                chunks.append(Chunk([w0,w1,w2]))
                    else:
                        chunks.append(Chunk([w0,w1]))
            else:
                chunks.append(Chunk([w0]))
        return chunks
                    
def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    import psyco
    psyco.full()
    
    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    )
    
    tests = [u"研究生命起源",
             u'我们都喜欢用Python',
             u"这是一句中文",
             u"研究生命科学",
             u"主持人把一只割去头的羊放在指定处。枪响后，甲乙两队共同向羊飞驰而去，先抢到羊的同队队员互相掩护，极力向终点奔驰，双方骑手们施展各种技巧，围追堵截，拼命抢夺。叼着羊先到达终点的为胜方。获胜者按照当地的习俗，将羊当场烤熟，请众骑手共享，称为“幸福肉”。",
             ]
    for t in tests:
        #a = SimpleAlgorithm(t)
        a = ComplexAlgorithm(t)
        words = a.segment()
        ww = [w for w in words]
        #print ww, len(ww)
        
    testdata = file("..//test//testdata.txt").read().decode('utf8')
    testlen = len(testdata)    
    logging.info("segment big chunks %s" % testlen)
        
    a = ComplexAlgorithm(testdata)
    
    def testcall(a, testdata):
        import time            
        start = time.time()
        #psyco.bind(a.segment)
        words = a.segment()
        ww = [w for w in words]
        end = time.time()        
        logging.info("segment big chunks done, %s words, %s seconds" % (len(ww), end-start))
        #print ww
    
    
    from pychseg.utils.profiler import profile_call        
    profile_call(testcall, a ,testdata)
    #testcall(a, testdata)
    
    print a.find_match_word.hits, a.find_match_word.misses
    