
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

def takemost(val2cmp, iterable, reverse=True):
    """
    >>> takemost(lambda x:x/2, [9,3,4,1,4,9,2,8])
    [9, 9, 8]
    """    
    for i, obj in enumerate(iterable):
        v = val2cmp(obj)
        if i == 0:
            max_obj = [obj]
            max_val = v
        else:                
            if reverse:
                r = cmp(v, max_val)
            else:
                r = cmp(max_val, v)
            if r == 0:
                max_obj.append(obj)
            elif r>0:
                max_obj = [obj]
                max_val = v                     
    return max_obj
    
""" concept implementation
from itertools import takewhile
def takemost(val2cmp, iterable, reverse=True):    
    val = map(val2cmp, iterable)
    sorted_val = sorted( enumerate(val), lambda x,y: cmp(x[1],y[1]), reverse=reverse )
    most_val = takewhile(lambda x:x[1]==sorted_val[0][1], sorted_val)
    most_result = map(lambda x:iterable[x[0]], most_val)
    
    return most_result
"""

def joindict(dict1, dict2):
    """
    >>> [i for i in joindict({'1':2, 3:5, '3':12, '4':2}, {'4':11,1:12,3:2})]
    [3, '4']
    """       
    for d in dict1:
        if dict2.has_key(d):
            yield d

def joindictvalue(dict1, dict2):
    """
    >>> [i for i in joindictvalue({'1':2, 3:5, '3':12, '4':2}, {'4':11,1:12,3:2})]
    [(5, 2), (2, 11)]
    """       
    for d in dict1:
        if dict2.has_key(d):
            yield dict1[d], dict2[d]

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
    
