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

import logging, os

import config
from word import Word, CJK_WORD

import pychseg
from pychseg.utils.lrucache import lru_cache

@lru_cache()
def load_dict():
    word_dict = {}
    load_path = pychseg.__path__[0]
    chars = os.path.normpath( os.path.join(load_path, ".\\wordlist\\chars.lex" ) )
    words = os.path.normpath( os.path.join(load_path, ".\\wordlist\\words.lex" ) )
    logging.info("loading single chars dict") 
    load_words(chars, word_dict, "UTF-8")
    logging.info("loading words dict")
    load_words(words, word_dict, "UTF-8")
    logging.info("dict loaded!")
    return word_dict

def load_words(filename, word_dict, charset):
    for line in file(filename):
        # convert into unicode
        line = line.strip().decode(charset)
        if line.find('#') < 0:
            items = line.split(' ')
            if len(items[0]) > config.WORD_MAX_LENGTH:
                continue
            if len(items) > 1:
                try:
                    word_dict[items[0]] = Word(items[0], frequency=int(items[1]))
                except:
                    pass
            else:
                word_dict[items[0]] = Word(items[0])

if __name__ == "__main__":
    d = load_dict()
    print len(d)
    