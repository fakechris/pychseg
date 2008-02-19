#coding:utf-8

import config

UNRECOGNIZED = 0
BASICLATIN_WORD = 1
CJK_WORD = 2
   
class Word:
    """
    >>> w = Word("abc", CJK_WORD)
    >>> w.value
    'abc'
    >>> len(w)
    3
    """    
    def __init__(self, value, wtype=CJK_WORD, frequency=0):
        self.wtype = wtype
        self.value = value   
        self.len = len(value)     
        # avoid math.log(0) --> range error
        if wtype==UNRECOGNIZED and len(value)==1:
            self.frequency=1
        else:
            self.frequency = frequency
            
    def __len__(self):
        return self.len
    
    def __unicode__(self):
        return self.value
    
    def __str__(self):
        return self.value.encode(config.OUTPUT_CHARSET)

    def __repr__(self):
        return self.value.encode(config.OUTPUT_CHARSET)
    
def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
        