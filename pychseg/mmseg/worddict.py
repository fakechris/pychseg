#coding:utf-8

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
    