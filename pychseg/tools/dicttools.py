#coding:utf-8

from pychseg.mmseg.worddict import load_dict
from itertools import groupby

class DoubleArrayTrie(dict):
    def __init__(self):
        self.keys = self.keys_group = self.allkeyword = None
        self.unicode2sequence = None
        self.seqkeys = None
        self.index = {}
        self.minfreeid = 0
        
        # TODO: 应该按需扩展大小
        self.base = [0] * 200000 # big enough
        self.check = [0] * 200000 # big enough
    
    def setitems(self, keys, values):
        # 所有的词
        self.keys = keys
        # 统计词的长度分布 --> list of (wordlen, wordcount)
        self.keys_group = [(k,len(list(g))) for k,g in groupby(sorted(map(len,keys)))]
                    
        allkey = map(ord, u"".join(keys))
        # --> list of (uniquechar, charcount)
        allkeyword = [(k,len(list(g))) for k,g in groupby(sorted(allkey))]
        # 统计所有的字符，按频率排序，也是 sequence --> unicode 的索引    
        self.allkeyword = sorted(allkeyword, lambda x,y:cmp(y[1],x[1]))
        
        # 每个unicode --> sequence的索引
        self.unicode2sequence = [0] * 65535
        for i, b in enumerate(allkeyword):
            self.unicode2sequence[b[0]] = i+1    

        # 转换为seq的所有词表
        self.seqkeys = map(lambda y: map(lambda x:self.unicode2sequence[ord(x)], y), keys)
        
        # 最长的词长度
        longest = self.keys_group[-1][0]

        # 对于trie的每层节点按从多到少排序，为了创建空间利用率最优的trie
        sort_keys = []
        for i in range(longest):
            tempkey = filter(lambda x:len(x)>i, self.seqkeys)
            sortdk = [(k,list(g)) for k,g in groupby( sorted(tempkey, lambda x,y:cmp(x[:i+1],y[:i+1])), lambda x:x[:i+1] )]
            sortdk = sorted(sortdk, lambda x,y:cmp(len(y[1]),len(x[1])))
            # sortdk 格式 ---
            #  [ ( [a], [ [a,b], [a,c] ... ] ), ...
            sort_keys.append(sortdk)
        
        # 索引每个节点在base数组的标号
        for i in range( len(allkeyword) ):
            self.index[(i,)] = i
        self.minfreeid = len(allkeyword)    

        # 依次加入trie
        for i in range(longest-1):
            print "round ", i
            for node in filter(lambda x: len(x[1])>1 or len(x[1][0])>i+1, sort_keys[i]):
                print u' '*i + u''.join( map(unichr, map(lambda x:self.allkeyword[x-1][0], node[0])) )
                # node[0] -- this node
                # node[1] -- list of children nodes
                subnodes = filter(lambda x:x[0][:i+1]==node[0], sort_keys[i+1])
                subnodes_v = map(lambda x:x[0][i+1], subnodes)
        
                self.add_subnodes(node[0], node[1], subnodes_v)
                
        print self.base[:100]
        print self.check[:100]
    ##
    # @param current_node Current base node list, eg. [1,2]
    # @param subnodes_word_list All words followed by this node [[1,2,3],[1,2,4]..]
    # @param subnodes All possible node  
    #
    def add_subnodes(self, current_node, subnodes_word_list, subnodes):
        guess_node = self.minfreeid - subnodes[0]
        while 1:        
            result = self.guess_base_position(guess_node, subnodes)
            if result:
                break
            guess_node = guess_node + 1
        
        #print "    %s" % result 
        base_s = self.index[tuple(current_node)]
        # if base_s is already a word, set negtive value
        if  self.base[ base_s ] < 0:            
            self.base[ base_s ] = -result
        else:
            self.base[ base_s ] = result
        for subnode in subnodes:
            self.check[result + subnode] = base_s
            self.index[tuple(current_node + [subnode])] = result+subnode      
            # if subnode is a word, set negtive value (leaf node)  
            if current_node + [subnode] in subnodes_word_list:
                self.base[result + subnode] = -(result + subnode)
        self.minfreeid = self.find_next_freeid()
        return result
            
    def __setitem__(self, key, value):
        key_seq = map(lambda x:self.unicode2sequence[ord(x)], key)    
    
        s = key_seq[0]
        add_mode = 1
        for i, char in enumerate(key_seq[1:]):
            if add_mode == 1:
                t = abs(self.base[s]) + char
                if self.check[t] == s:
                    s = t
                    continue
                else:
                    add_mode = 2
                    
            current_node = key_seq[:i+1]                      
            if add_mode == 2:                      
                # 最终节点，直接查找一个插入点
                if self.base[s]+s == 0:                    
                    subnodes = [char]
                    s = self.add_subnodes(current_node, [key_seq], subnodes) + char                    
                else: # 需要查找所有子节点和本节点是否冲突，若冲突则全部子节点需要重新定位
                    t = abs(self.base[s]) + char
                    if self.base[t]==0 and self.check[t]==0: # 不冲突
                        # TODO: 设置check等
                        self.check[t] = s
                    else: # TODO:冲突，需要解决冲突，重定位所有的subnode                    
                        subnodes = [char] + self.find_all_subnodes(self.base[s])
                        s = self.add_subnodes(current_node, [key_seq], subnodes) + char
                add_mode = 3
            elif add_mode == 3:
                subnodes = [char]                
                s = self.add_subnodes(current_node, [key_seq], subnodes) + char
            
    def __delitem__(self, key):
        key_seq = map(lambda x:self.unicode2sequence[ord(x)], key)
        
        s = key_seq[0]
        for char in key_seq[1:]:
            t = abs(self.base[s]) + char
            if self.check[t] == s:
                s = t
                continue
            else:
                return 
            
        # not in word
        if self.base[s] >= 0:
            return
        
        # not a leaf word
        if self.base[s]+s != 0:
            self.base[s] = abs(self.base[s])
        else:
            # TODO: 上一级的节点有可能没用了并没有删除,有可能冗余
            self.base[s] = self.check[s] = 0
                
    def __getitem__(self, key):
        # first convert input to seq.
        text_seq = map(lambda x:self.unicode2sequence[ord(x)], key)
        
        # then query it
        s = text_seq[0]
        for char in text_seq[1:]:
            t = abs(self.base[s]) + char        
            if self.check[t] == s:
                s = t
                continue
            else:
                return False
        if self.base[s] < 0:
            return True
        else:
            return False

    def find_all_subnodes(self, base_node):
        return filter( lambda x:self.check[base_node+x]==base_node, range(len(self.allkeyword)) )

    def guess_base_position(self, base_pos, nodes):
        for node in nodes:
            if self.base[base_pos+node] != 0 or self.check[base_pos+node] != 0:
                return 0
            
        return base_pos
    
    def find_next_freeid(self):
        for i in range(self.minfreeid+1, len(self.base)):
            if self.base[i] == 0 and self.check[i] == 0:
                return i
        
        return 0

def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    dictkey = [u'a', u'bc', u'def', u'ghab', u'cab', u'cb', u'caef', u'caeg', u'gh',u'dhabcd']
    
    dat = DoubleArrayTrie()
    #dictdata = load_dict()
    dat.setitems(dictkey, None)
    print '...'
    for char in [u'a', u'bc', u'def', u'ghab', u'cab', u'cb', u'caef', u'caeg', u'gh',u'dhabcd']:
        print dat[char]
    print '...'
    for char in [u'ab', u'bcd', u'de', u'dha', u'cae', u'cabe']:
        print dat[char]
    print '...'    
    del dat[u'def']
    print dat[u'def']
    print dat[u'de']
    del dat[u'gh']
    print dat[u'gh']
    print dat[u'ghab']
    del dat[u'caef']
    print dat[u'caef']
    print dat[u'caeg']
    print  '...'
    dat[u'bcde'] = 1
    print dat[u'bcde']
    print dat[u'bc']
    dat[u'gabc'] = 1
    print dat[u'gabc']
        
    