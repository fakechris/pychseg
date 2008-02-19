#coding:utf-8

def profile_call(*callargs):            
    import hotshot, hotshot.stats    
    prof = hotshot.Profile("call.prof")
    prof.runcall(*callargs)
    prof.close()
    stats = hotshot.stats.load("call.prof")
    stats.strip_dirs()
    stats.sort_stats('time', 'calls')
    stats.print_stats(20)
