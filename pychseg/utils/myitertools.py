
def takemost(val2cmp, iterable, reverse=True):
    """
    >>> takemost(lambda x:x/2, [9,3,4,1,4,9,2,8])
    [9, 9, 8]
    """    
    for i, obj in enumerate(iterable):
        v = val2cmp(obj)
        if i == 0:
            max_obj = [ obj ]
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

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
    
