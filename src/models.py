#!/usr/bin/env python
# coding=UTF-8
import sys
import codecs
import nltk
import re
from nltk.corpus import stopwords

class AnalyzeConversation(object):

    all_stop_words = None
    fp = None
    fdist = None

    def __init__(self, file):
        #input_file = 'luiza.txt'
        #fp = codecs.open(input_file, 'r', 'utf-8')
        self.fp = file

    def load_stop_words(self):
        stopwords_file = './resources/stopwords.txt'
        names_file = './resources/names.txt'
        default_stopwords = set(nltk.corpus.stopwords.words('portuguese'))
        custom_stopwords = set(codecs.open(stopwords_file, 'r', 'utf-8').read().splitlines())
        names = set(codecs.open(names_file, 'r', 'utf-8').read().splitlines())
        self.all_stopwords = default_stopwords | custom_stopwords | names

    def start_analyze(self):
        #Separa palavras
        words = nltk.word_tokenize(self.fp.stream.read().decode('utf-8'))
        #remove caracteres unicos
        words = [word for word in words if len(word) > 1]
        #Remove numeros
        words = [word for word in words if not word.isnumeric()]
        #Remove datas
        words = [word for word in words if not re.findall(r"\d\d\/\d\d\/\d\d", word)]
        #Remove horas
        words = [word for word in words if not re.findall(r"\d\d:\d\d", word)]
        #Transforma em minusculo
        words = [word.lower() for word in words]
        #remove caracteres inválidos
        words = [word for word in words if re.findall(r"\w", word)]
        #remove risadas
        words = [word for word in words if not re.findall(r"(k){3,}", word)]
        words = [word for word in words if not re.findall(r"(ha){2,}", word)]
        words = [word for word in words if not re.findall(r"(ka){2,}", word)]
        #remove digito +55
        words = [word for word in words if not re.findall(r"\+\d\d", word)]
        #remove numero de telefones
        words = [word for word in words if not re.findall(r"\d\d\d\d-\d\d\d\d", word)]
        #remove stopwords
        words = [word for word in words if word not in self.all_stopwords]
        #calcula frequencia de distrubuição
        self.fdist = nltk.FreqDist(words)

    def get_result(self, qtd = 15):
        result = []
        for w, f in self.fdist.most_common(qtd):
            result.append(Word(w, f))

        return result
        
class Word(object):
    def __init__(self, word, frequency):
        self.word = word
        self.frequency = frequency
