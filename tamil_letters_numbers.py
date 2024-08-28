# Copyright (C) 2018 Nithya Duraisamy <nithyadurai87@gmail.com>
# Tamil sandhi checker - validate and fix list of Sandhi errors in Tamil text
import tamil
import collections
import codecs
import os
import sys

#change this to enable print statements
_DEBUG=False

#http://www.tamilvu.org/courses/degree/c021/c0214/html/c0214661.htm
BASE_DIRECTORY = os.path.split(__file__)[0]

தமிழ்_எழுத்து = os.path.join(BASE_DIRECTORY,"all-tamil-nouns.txt")
பெயர்_கோப்பு = codecs.open(தமிழ்_எழுத்து,"r","UTF-8")
பெயர்_பட்டியல் = பெயர்_கோப்பு.read().strip().split()

மெய்யெழுத்து = tamil.utf8.mei_letters
உயிரெழுத்து = tamil.utf8.uyir_letters
ஆய்தம் = ['ஃ']
குறிலெழுத்து = tamil.utf8.kuril_letters
நெடிலெழுத்து = tamil.utf8.nedil_letters
அகரவெழுத்து = tamil.utf8.agaram_letters
உயிர்மெய்யெழுத்து = tamil.utf8.uyirmei_letters
வல்லினம் = tamil.utf8.vallinam_letters
மெல்லினம் = tamil.utf8.mellinam_letters
ஓரெழுத்தொருமொழி=['ஆ', 'ஈ', 'ஊ', 'ஏ', 'ஐ', 'ஓ', 'கா', 'கூ', 'கை', 'கோ', 'சா', 'சீ', 'சே', 'சோ', 'தா', 'தீ', 'து', 'தூ', 'தே', 'தை', 'நா', 'நீ', 'நே', 'நை', 'நொ', 'நோ', 'பா', 'பூ', 'பே', 'பை', 'போ', 'மா', 'மீ', 'மூ', 'மே', 'மை', 'மோ', 'யா', 'வா', 'வீ', 'வை', 'வௌ']
சுட்டு=['அ','இ','உ']
வினா=['ஆ','ஏ','ஓ']
எண்கள்_எழுத்தில்=['ஒன்று','இரண்டு','மூன்று','நான்கு','ஐந்து','ஆறு','ஏழு','ஒன்பது','நூறு','ஒரு','இரு','அறு','எழு']
வியங்கோள்=['க', 'இய', 'இயர்'] # ஒரு சொல்லின் இறுதியில் இந்த வடிவம் வரும்.
தமிழ்_எழுத்துக்கள் = tamil.utf8.tamil_letters
சமசுகிருத_எழுத்துக்கள் = tamil.utf8.sanskrit_letters 
சமுசுகிருத_மெய்யெழுத்துக்கள் = tamil.utf8.sanskrit_mei_letters 
சிறப்புக்குறியீடுகள்=['.', '\'', ';', ',', ':', '?', '(', ')', '_', '-', '"', '%', '±', '#', '@', '!', '!', '$', '%', '^', '&', '*', '+', '/', '–', '\\', '>', '<', '|', '}', '{', ']', '[']
எண்கள்=['0', '1', '2', '3',  '4', '5', '6', '7', '8', '9', '½']
கிரந்தவெழுத்து = ["ஜ்", "ஷ்", "ஸ்", "ஹ்"
, "ஶ", "ஶா", "ஶி", "ஶீ", "ஶு", "ஶூ", "ஶெ", "ஶே", "ஶை", "ஶொ", "ஶோ", "ஶௌ"
, "ஜ"  , "ஜா"  , "ஜி"  , "ஜீ" , "ஜு" , "ஜூ" , "ஜெ" , "ஜே" , "ஜை" , "ஜொ" , "ஜோ" , "ஜௌ"
,"ஷ" , "ஷா", "ஷி", "ஷீ", "ஷு", "ஷூ", "ஷெ", "ஷே", "ஷை", "ஷொ", "ஷோ", "ஷௌ"
, "ஸ"  , "ஸா"  , "ஸி"  , "ஸீ"  , "ஸு"  , "ஸூ"  , "ஸெ"  , "ஸே"  , "ஸை"  , "ஸொ", "ஸோ", "ஸௌ"
, "ஹ"  , "ஹா"  , "ஹி"  , "ஹீ"  , "ஹு"  , "ஹூ"  , "ஹெ"  , "ஹே"  , "ஹை"  , "ஹொ"  , "ஹோ"  , "ஹௌ"
, "க்ஷ" , "க்ஷா" , "க்ஷி" , "க்ஷீ" , "க்ஷு" , "க்ஷூ" , "க்ஷெ" , "க்ஷே" , "க்ஷை" , "க்ஷொ" , "க்ஷோ" , "க்ஷௌ" ]
ஆங்கிலம் = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
assert( len(ஆங்கிலம்) == 52 )

#buggy!
def safe_splitMeiUyir(arg):
    try:
        # when uyir letters are passed to splitMeiUyir function it will throw an IndexError
        rval = tamil.utf8.splitMeiUyir(arg)
        if not isinstance(rval,tuple):
            if rval in uyir_letters:
                return (u'',rval)
            return (rval,u'')
        return rval
    except IndexError as idxerr:
        pass
    except ValueError as valerr:
        # non tamil letters cannot be split - e.g. '26வது'
        pass
    # could be english string etc. multiple-letter (word-like) input etc
    return (u'',u'')

class Results:
    # class contains results of 'check_sandhi' method
    ErrorLog = collections.namedtuple('ErrorLog',['rule','description','word']) #description of error
    def __init__(self):
        self.errors = [] #list of ErrorLog object

    def add(self,word,rule,descr):
        elog = Results.ErrorLog( rule, descr, word )
        self.errors.append(elog)

    @property
    def counter(self):
        return len(self.errors)

    def __unicode__(self):
        return self.__str__()

    def __str__(self):
        summary_list = [u"%s -> (%s, %s),\n"%(err.word,err.rule,err.description) for err in self.errors]
        return u"".join(summary_list)

