import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from bs4 import BeautifulSoup

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

class PreprocessLibrary:
    
    def __init__(self):
        self.stemmer = StemmerFactory().create_stemmer()
        self.stopword = StopWordRemoverFactory().create_stop_word_remover()

    def cleaningAbstrak(self, text):
        text = str(text)
        text = BeautifulSoup(text, "html.parser").get_text()
        text = text.lower()
        text = re.sub(r'http\\S+', '', text)
        text = re.sub('(@\\w+|#\\w+)', '', text)
        text = re.sub('[^a-zA-Z]', ' ', text)
        text = re.sub("\\n", " ", text)
        text = self.stopword.remove(text)
        text = self.stemmer.stem(text)
        text = re.sub('(s{2,})', ' ', text)
        return text

    def cleaningJudul(self, text):
        text = str(text)
        text = BeautifulSoup(text, "html.parser").get_text()
        text = text.title()
        text = re.sub("\\n", " ", text)
        text = re.sub('(s{2,})', ' ', text)
        return text

    def cleaningPenulis(self, text):
        text = text.title()
        text = re.sub("\\n", " ", text)
        text = re.sub("(s{2,})", " ", text)
        return text