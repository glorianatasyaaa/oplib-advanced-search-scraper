import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
from bs4 import BeautifulSoup

# from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
# from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

def cleaningAbstrak(text):

    #Membuat stemmer sastrawi
    # factory = StemmerFactory()
    # stemmer = factory.create_stemmer()

    # # #Membuat stopword sastrawi
    # factory = StopWordRemoverFactory()
    # stopword = factory.create_stop_word_remover()

    text = str(text)

    # Menghapus tag HTML
    text = BeautifulSoup(text, "html.parser").get_text()

    # Mengubah setiap kata menjadi lowercase
    text =  text.lower()

    # Menghapus Link Dengan Pattern http/https
    text = re.sub(r'http\S+', '', text)

    # Menghapus hashtag dan username
    text = re.sub('(@\w+|#\w+)', '', text)

    # Menghapus Karakter Selain Huruf a-z dan A-Z
    text = re.sub('[^a-zA-Z]', ' ', text)

    # Mengganti baris baru (enter) dengan spasi
    text = re.sub("\n", " ", text)

    # #Menghapus kata stopword dengan library sastrawi
    # text = stopword.remove(text)

    # #Melakukan stemming dengan library sastrawi
    # text = stemmer.stem(text)

    # Menghapus Spasi Yang Lebih Dari Satu
    text = re.sub('(s{2,})', ' ', text)

    # Mengembalikan Hasil Preprocessing Text
    return text

def cleaningJudul(text):
    text = str(text)

    # Menghapus tag HTML
    text = BeautifulSoup(text, "html.parser").get_text()

    # Mengubah setiap kata menjadi lowercase
    text =  text.title()

    # Mengganti baris baru (enter) dengan spasi
    text = re.sub("\n", " ", text)

    # Menghapus Spasi Yang Lebih Dari Satu
    text = re.sub('(s{2,})', ' ', text)

    # Mengembalikan Hasil Preprocessing Text
    return text


def cleaningPenulis(text):
  text = text.title()

  text = re.sub("\n"," ", text)

  text = re.sub("(s{2,})"," ", text)

  return text

if __name__ == "__main__":
    try:
        df = pd.read_json("scrappingOplib/contoh hasil keluaran_skripsi.json")

        df = df.rename(columns={'title': 'Judul', 'author':'Penulis1','lecturer':'Penulis2','publish_year':'Tahun','abstract':'Abstrak'})
        df = df[["Judul","Penulis1","Penulis2","Tahun","Abstrak"]]

        df = df.dropna()

        df['Abstrak'] = df['Abstrak'].apply(cleaningAbstrak)
        df['Judul'] = df['Judul'].apply(cleaningJudul)
        df["Penulis1"] = df["Penulis1"].apply(cleaningPenulis)
        df["Penulis"] = df["Penulis1"] + ", " + df["Penulis2"]
        df = df.drop(["Penulis1","Penulis2"],axis = 1)
        df = df[["Judul","Tahun","Abstrak","Penulis"]]
        df["Tahun"] = df["Tahun"].astype(int)

        df['Abstrak'] = df['Abstrak'].replace('', np.nan)
        df['Judul'] = df['Judul'].replace('', np.nan)
        df = df.dropna()

        df = df[["Judul","Penulis","Tahun","Abstrak"]]

        df.to_json('preprocessOplib/df_oplib_skripsi_nolabel.json', orient='records')

    except Exception as e:
        print("Terjadi error:",str(e))

