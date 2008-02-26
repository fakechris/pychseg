#coding:utf-8

from pychseg.mmseg.worddict import load_dict
from itertools import groupby

#dictdata = load_dict()
#dictkey = dictdata.keys()
dictkey = [u'a', u'bc', u'def', u'ghab', u'cab', u'cb', u'caef', u'caeg', u'gh',u'dhabcd']

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
    unicode2sequence[b[0]] = i+1    
    
# 这里应该把所有的词都转换为seq id    
#dictkey_seq = map(lambda y: u''.join( map(unichr, map(lambda x:unicode2sequence[ord(x)], y)) ), dictkey)

dictkey_seq = map(lambda y: map(lambda x:unicode2sequence[ord(x)], y), dictkey)
dictkey = dictkey_seq
# dictkey 格式 ---
#   [[a,b,c],[d,e],[]]

##################################
longest = dictlen[-1][0]
sort_keys = []
for i in range(longest):
    tempkey = filter(lambda x:len(x)>i, dictkey)
    sortdk = [(k,list(g)) for k,g in groupby( sorted(tempkey, lambda x,y:cmp(x[:i+1],y[:i+1])), lambda x:x[:i+1] )]
    sortdk = sorted(sortdk, lambda x,y:cmp(len(y[1]),len(x[1])))
    # sortdk 格式 ---
    #  [ ( [a], [ [a,b], [a,c] ... ] ), ...
    sort_keys.append(sortdk)

base = [0] * 200000 # big enough
check = [0] * 200000 # big enough
# 初始化level1节点
#for node1 in sortdk1:
#    base[ord(node1[0])] = 0
index = {}
for i in range( len(allkeyword) ):
    index[(i,)] = i
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

for i in range(longest-1):
    print "round ", i
    for node in filter(lambda x: len(x[1])>1 or len(x[1][0])>i+1, sort_keys[i]):
        print u' '*i + u''.join( map(unichr, map(lambda x:allkeyword[x-1][0], node[0])) )
        # node[0] -- this node
        # node[1] -- list of children nodes
        subnodes = filter(lambda x:x[0][:i+1]==node[0], sort_keys[i+1])
        subnodes_v = map(lambda x:x[0][i+1], subnodes)

        #print node[0]
        guess_node = minfreeid - subnodes_v[0]
        while 1:        
            result = guess_base_position(guess_node, subnodes_v)
            if result:
                break
            guess_node = guess_node + 1
        
        #print "    %s" % result 
        base_s = index[tuple(node[0])]
        # if base_s is already a word, set negtive value
        if  base[ base_s ] < 0:            
            base[ base_s ] = -result
        else:
            base[ base_s ] = result
        for subnode in subnodes_v:
            check[result + subnode] = base_s
            index[tuple(node[0] + [subnode])] = result+subnode      
            # if subnode is a word, set negtive value (leaf node)  
            if node[0] + [subnode] in node[1]:
                base[result + subnode] = -(result + subnode)
        minfreeid = find_next_freeid(minfreeid)
        #print "    %s" % minfreeid


print base[:100]
print check[:100]
    
# query
def query(text):
    # first convert input to seq.
    text_seq = map(lambda x:unicode2sequence[ord(x)], text)
    
    s = text_seq[0]
    for char in text_seq[1:]:
        t = abs(base[s]) + char        
        if check[t] == s:
            s = t
            continue
        else:
            return False
    if base[s] < 0:
        return True
    else:
        return False
    
# correct
print '...'
for char in [u'a', u'bc', u'def', u'ghab', u'cab', u'cb', u'caef', u'caeg', u'gh',u'dhabcd']:
    print query(char)
print '...'
for char in [u'ab', u'bcd', u'de', u'dha', u'cae', u'cabe']:
    print query(char)
print '...'    

# TODO: insert and delete nodes
def insert(word):
    word_seq = map(lambda x:unicode2sequence[ord(x)], word)
    # 

def delete(word):
    word_seq = map(lambda x:unicode2sequence[ord(x)], word)
