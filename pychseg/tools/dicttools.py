#coding:utf-8

from pychseg.mmseg.worddict import load_dict
from itertools import groupby

#dictdata = load_dict()
#dictkey = dictdata.keys()
dictkey = [u'a', u'bc', u'def', u'ghab', u'cab', u'cb', u'caef', u'caeg']
org_dictkey = dictkey

# 统计几个字母的长度的词的分布
# the length count
dictlen = [(k,len(list(g))) for k,g in groupby(sorted(map(len,dictkey)))]
# [(1, 12638), (2, 73385), (3, 19400), (4, 25869)]

# 统计所有的字符
# all key 321084 word
allkey = u"".join(dictkey)
allkey1 = map(ord, allkey)
# group and sort, got 12683 unique key and freq.
allkeyword = [(k,len(list(g))) for k,g in groupby(sorted(allkey1))]
# 12710 total unique keyword
allkeyword = sorted(allkeyword, lambda x,y:cmp(y[1],x[1]))

# sequence word <-> allkeyword
# 字典，每个字符对应一个seq id
# set map key dict ref.
unicode2sequence = [0] * 65535
for i, b in enumerate(allkeyword):
    unicode2sequence[b[0]] = i
    
# 这里应该把所有的词都转换为seq id    
#dictkey_seq = map(lambda y: u''.join( map(unichr, map(lambda x:unicode2sequence[ord(x)], y)) ), dictkey)

dictkey_seq = map(lambda y: map(lambda x:unicode2sequence[ord(x)], y), dictkey)

dictkey = dictkey_seq
##################################

# 排列每一级的节点个数
# level 1 node 131292/12683 1543->1
dictkey1 = dictkey
sortdk1 = [(k,list(g)) for k,g in groupby( sorted(dictkey1, lambda x,y:cmp(x[0],y[0])), lambda x:x[0] )]
sortdk1 = sorted(sortdk1, lambda x,y:cmp(len(y[1]),len(x[1])))

# level 2 node 118654/86907 67->1
dictkey2 = filter(lambda x:len(x)>1,dictkey)
sortdk2 = [(k,list(g)) for k,g in groupby( sorted(dictkey2, lambda x,y:cmp(x[:2],y[:2])), lambda x:x[:2] )]
sortdk2 = sorted(sortdk2, lambda x,y:cmp(len(y[1]),len(x[1])))

# level 3 node 45269/43063 13->1
dictkey3 = filter(lambda x:len(x)>2,dictkey)
sortdk3 = [(k,list(g)) for k,g in groupby( sorted(dictkey3, lambda x,y:cmp(x[:3],y[:3])), lambda x:x[:3] )]
sortdk3 = sorted(sortdk3, lambda x,y:cmp(len(y[1]),len(x[1])))

# level 4 node 25869/25869 1->1
dictkey4 = filter(lambda x:len(x)>3,dictkey)
sortdk4 = [(k,list(g)) for k,g in groupby( sorted(dictkey4, lambda x,y:cmp(x[:4],y[:4])), lambda x:x[:4] )]
sortdk4 = sorted(sortdk4, lambda x,y:cmp(len(y[1]),len(x[1])))

base = [0] * 200000 # big enough
check = [0] * 200000 # big enough
# 初始化level1节点
#for node1 in sortdk1:
#    base[ord(node1[0])] = 0

minfreeid = len(allkeyword)

def guess_base_position(base_pos, nodes):
    for node in nodes:
        if base[base_pos+node] != 0 or check[base_pos+node] != 0:
            return 0
        
    return base_pos

def find_next_freeid(pos):
    for i in range(pos+1, len(base)):
        if base[i] == 0 and check[i] == 0:
            return i
    
    return 0

# 依次设置level1节点的子节点    
for node1 in sortdk1:    
    #node1 = sortdk1[0]
    nodes2 = filter(lambda x:x[0][0]==node1[0], sortdk2)
    if not len(nodes2): continue
    #sum( map(lambda x:1 << x[0][1], nodes2) )
    nodes2_v = map(lambda x:x[0][1], nodes2)
    
    print node1[0]
    guess_node = minfreeid - nodes2_v[0]
    while 1:        
        result = guess_base_position(guess_node, nodes2_v)
        if result:
            break
        guess_node = guess_node + 1
    
    print "    %s" % result
    base[node1[0]] = result
    for node2 in nodes2_v:
        check[result + node2] = result        
    minfreeid = find_next_freeid(minfreeid)
    print "    %s" % minfreeid
        
        
# 依次设置level2节点的子节点    
for node2 in sortdk2:    
    nodes3 = filter(lambda x:x[0][:2]==node2[0], sortdk3)
    for node3 in nodes3:
        print "    ", node3[0]

# 依次设置level3节点的子节点        
for node3 in sortdk3:    
    nodes4 = filter(lambda x:x[0][:3]==node3[0], sortdk4)
    for node4 in nodes4:
        print "      ", node4[0]

# 不必处理level4节点了

##################################

"""
#all the keys 131292 first word
dictkey1 = map(lambda x:x[0], dictkey)
# turn to int
#dictkey1 = map(ord, dictkey1)
# group and sort, got 12683 unique key and freq.
sortdk1 = [(k,len(list(g))) for k,g in groupby(sorted(dictkey1))]
# sort by freq. 1543->1
sortdk1 = sorted(sortdk1, lambda x,y:cmp(y[1],x[1]))    

#all the 118654 key first 2 words
dictkey2 = map(lambda x:(x[0],x[1]), filter(lambda x:len(x)>1,dictkey))
# turn to int
#dictkey2=map(lambda x: (ord(x[0]) << 16) + ord(x[1])  ,dictkey2)
# group and sort, got 86907 unique key and freq.
sortdk2 = [(k,len(list(g))) for k,g in groupby(sorted(dictkey2))]
# sort by freq. 67 -> 1
sortdk2  = sorted(sortdk2, lambda x,y:cmp(y[1],x[1]))    

#all the 45269 key first 3 words
dictkey3 = map(lambda x:(x[0],x[1],x[2]), filter(lambda x:len(x)>2,dictkey))
#dictkey3=map(lambda x: (ord(x[0]) << 32) + (ord(x[1]) << 16) + ord(x[2])  ,dictkey3)
# group and sort, got 43063 unique key and freq.
sortdk3 = [(k,len(list(g))) for k,g in groupby(sorted(dictkey3))]
# sort by freq. 13 -> 1
sortdk3  = sorted(sortdk3, lambda x,y:cmp(y[1],x[1]))

#all the 25869 key first 4 words
dictkey4 = map(lambda x:(x[0],x[1],x[2],x[3]), filter(lambda x:len(x)>3,dictkey))
#dictkey4=map(lambda x: (ord(x[0]) << 48) + (ord(x[1]) << 32) + (ord(x[2]) << 16) + ord(x[3])  ,dictkey4)
sortdk4 = [(k,len(list(g))) for k,g in groupby(sorted(dictkey4))]
# sort by freq. 1 -> 1
sortdk4  = sorted(sortdk4, lambda x,y:cmp(y[1],x[1]))
"""



#base = map(lambda x:x[0], allkeyword)
#check = [0] * len(base)



