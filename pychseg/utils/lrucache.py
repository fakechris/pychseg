
from collections import deque

def lru_cache(maxsize=16):
    '''Decorator applying a least-recently-used cache with the given maximum size.

    Arguments to the cached function must be hashable.
    Cache performance statistics stored in f.hits and f.misses.
    '''
    def decorating_function(f):
        cache = {}              # mapping of args to results
        queue = deque()         # order that keys have been accessed
        refcount = {}           # number of times each key is in the access queue
        def wrapper(*args):
            
            # localize variable access (ugly but fast)
            _cache=cache; _len=len; _refcount=refcount; _maxsize=maxsize
            queue_append=queue.append; queue_popleft = queue.popleft

            # get cache entry or compute if not found
            try:
                result = _cache[args]
                wrapper.hits += 1
            except KeyError:
                result = _cache[args] = f(*args)
                wrapper.misses += 1

            # no arguments, just cache it!
            if not _len(args):
                return result

            # record that this key was recently accessed
            queue_append(args)
            _refcount[args] = _refcount.get(args, 0) + 1

            # Purge least recently accessed cache contents
            while _len(_cache) > _maxsize:
                k = queue_popleft()
                _refcount[k] -= 1
                if not _refcount[k]:
                    del _cache[k]
                    del _refcount[k]
    
            # Periodically compact the queue by duplicate keys
            if _len(queue) > _maxsize * 4:
                for i in [None] * _len(queue):
                    k = queue_popleft()
                    if _refcount[k] == 1:
                        queue_append(k)
                    else:
                        _refcount[k] -= 1
                assert len(queue) == len(cache) == len(refcount) == sum(refcount.itervalues())

            return result
        wrapper.__doc__ = f.__doc__
        wrapper.__name__ = f.__name__
        wrapper.hits = wrapper.misses = 0
        return wrapper
    return decorating_function

def instance_cache(maxsize=16):
    '''Decorator applying a least-recently-used cache with the given maximum size.

    Arguments to the cached function must be hashable.
    Cache performance statistics stored in f.hits and f.misses.
    Cache stored in object instance, won't cache result if not object function
    '''
    def decorating_function(f):
        def wrapper(*args):  
            # localize variable access (ugly but fast)          
            _func_name = f.func_code.co_name
            _func_argcount = f.func_code.co_argcount
            _func_varnames = f.func_code.co_varnames
            
            # only caching for instance, skip this test
            if not (_func_argcount>0 and _func_varnames[0] is 'self'):
                return f(*args)
            
            _instance = args[0]
            _args = args[1:]
            _len=len; _maxsize=maxsize

            _cache_prop = "_%s_cache" % _func_name
            _refcount_prop = "_%s_refcount" % _func_name
            _queue_prop = "_%s_queue" % _func_name
            
            # no arguments, just cache it!
            if not _len(_args):
                try:
                    result = getattr(_instance, _cache_prop)
                    wrapper.hits += 1
                except AttributeError:
                    result = f(*args)
                    setattr(_instance, _cache_prop, result)
                    wrapper.misses += 1
                return result
                    
            # get cache entry or compute if not found
            try:
                _cache=getattr(_instance, _cache_prop) 
                _refcount=getattr(_instance, _refcount_prop)
                _queue=getattr(_instance, _queue_prop)
                queue_append=_queue.append; queue_popleft=_queue.popleft
                
                result = _cache[_args]
                wrapper.hits += 1
            except AttributeError:
                setattr(_instance, _cache_prop, {})
                setattr(_instance, _refcount_prop, {})
                setattr(_instance, _queue_prop, deque())
                
                _cache=getattr(_instance, _cache_prop) 
                _refcount=getattr(_instance, _refcount_prop)
                _queue=getattr(_instance, _queue_prop)
                queue_append=_queue.append; queue_popleft=_queue.popleft
                
                result = _cache[_args] = f(*args)
                wrapper.misses += 1
            except KeyError:
                result = _cache[_args] = f(*args)
                wrapper.misses += 1
                
            # record that this key was recently accessed
            queue_append(_args)
            _refcount[_args] = _refcount.get(_args, 0) + 1

            # Purge least recently accessed cache contents
            while _len(_cache) > _maxsize:
                k = queue_popleft()
                _refcount[k] -= 1
                if not _refcount[k]:
                    del _cache[k]
                    del _refcount[k]
    
            # Periodically compact the queue by duplicate keys
            if _len(_queue) > _maxsize * 4:
                for i in [None] * _len(_queue):
                    k = queue_popleft()
                    if _refcount[k] == 1:
                        queue_append(k)
                    else:
                        _refcount[k] -= 1
                assert len(_queue) == len(cache) == len(refcount) == sum(refcount.itervalues())

            return result
        wrapper.__doc__ = f.__doc__
        wrapper.__name__ = f.__name__
        wrapper.hits = wrapper.misses = 0
        return wrapper
    return decorating_function

if __name__ == '__main__':
    
    class myclass2:
        @instance_cache()
        def h(self):
            return 12
        
        @instance_cache(maxsize=2)
        def x(self, i):
            return i * i
        
    x = myclass2()
    x.h()
    x.h()
    x.h()
    x.h()
    x.x(1)
    x.x(2)
    x.x(3)
    x.x(2)
    x.x(44)
    y = myclass2()
    y.h()
    y.x(44)
    
    
    class myclass:
        @lru_cache(maxsize=1)
        def g(self):
            return 11

    m = myclass()
    m.g()
    m.g()
    m.g()
    print m.g.hits, m.g.misses
    n = myclass()
    n.g()
    n.g()
    print n.g.hits, n.g.misses
         
    @lru_cache(maxsize=20)
    def f(x, y):
        return 3*x+y

    domain = range(5)
    from random import choice
    for i in range(1000):
        r = f(choice(domain), choice(domain))

    print f.hits, f.misses

