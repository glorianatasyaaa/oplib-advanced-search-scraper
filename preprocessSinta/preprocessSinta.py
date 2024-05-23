import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re
import googletrans
from googletrans import Translator

from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory, StopWordRemover, ArrayDictionary
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

# Fungsi untuk mengubah list menjadi string
def list_to_string(lst):
    return ' '.join(lst)

# Menggabungkan nama pertama dan nama terakhir penulis
def cleaningPenulis(names):
    cleaned_names = []
    for name in names:
        parts = name.strip().split(',')
        if len(parts) == 2:  # Pastikan entri memiliki format yang diharapkan
            cleaned_names.append(parts[1].strip() + ' ' + parts[0].strip())
        else:
            # Jika tidak sesuai format, anggap hanya memiliki satu nama (nama pertama)
            cleaned_names.append(parts[0].strip())
    return cleaned_names

def cleaningAbstrakTahap1(text):
    text = str(text)

    # Mengubah setiap kata menjadi lowercase
    text = text.lower()

    # Menghapus teks setelah tanda ©
    text = re.sub(r'©.*', '', text)

    # Mengembalikan Hasil Preprocessing Text
    return text

def translate_text(text):
    try:
        translator = Translator()
        translated = translator.translate(text, dest='id')
        return translated.text
    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def cleaningAbstrakTahap2(text):

    #Membuat stemmer sastrawi
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()

    # #Membuat stopword sastrawi
    factory = StopWordRemoverFactory()
    stopword = factory.create_stop_word_remover()
    
    text = str(text)

    # Mengubah setiap kata menjadi lowercase
    text = text.lower()

    # Menghapus Link Dengan Pattern http/https
    text = re.sub(r'http\S+', '', text)

    # Menghapus hashtag dan username
    text = re.sub('(@\w+|#\w+)', '', text)

    # Menghapus Karakter Selain Huruf a-z dan A-Z
    text = re.sub('[^a-zA-Z]', ' ', text)

    # Menghapus kata-kata yang muncul secara bersamaan lebih dari 2 kali secara berturut-turut
    text = re.sub(r'\b(\w+)\s+\1\b', r'\1', text)

    # Menghapus kata stopword dengan library sastrawi
    text = stopword.remove(text)

    # Melakukan stemming dengan library sastrawi
    text = stemmer.stem(text)

    # Mengganti baris baru (enter) dengan spasi
    text = re.sub("\n", " ", text)

    # Menghapus Spasi Yang Lebih Dari Satu
    text = re.sub('(s{2,})', ' ', text)

    # Mengembalikan Hasil Preprocessing Text
    return text.strip()


def get_aspects(review):
  review = str(review)
  review_aspects = []

  aspects = {
    'SDG1' : ['Goal 1'],
    'SDG2' : ['Goal 2'],
    'SDG3' : ['Goal 3'],
    'SDG4' : ['Goal 4'],
    'SDG5' : ['Goal 5'],
    'SDG6' : ['Goal 6'],
    'SDG7' : ['Goal 7'],
    'SDG8' : ['Goal 8'],
    'SDG9' : ['Goal 9'],
    'SDG10' : ['Goal 10'],
    'SDG11' : ['Goal 11'],
    'SDG12' : ['Goal 12'],
    'SDG13' : ['Goal 13'],
    'SDG14' : ['Goal 14'],
    'SDG15' : ['Goal 15'],
    'SDG16' : ['Goal 16'],
    'SDG17' : ['Goal 17']
    }

  for aspect, keywords in aspects.items():
    for keyword in keywords:
      if re.search(fr'{re.escape(keyword)}', review):
        review_aspects.append(aspect)
        break
  return review_aspects

if __name__ == "__main__":
    try:
        df = pd.read_json("preprocessSinta/result.json")

        df['sdgs'] = df['sdgs'].apply(list_to_string)
        df['penulis'] = df['penulis'].apply(list_to_string)
        df['abstrak'] = df['abstrak'].apply(list_to_string)
        df['judul'] = df['judul'].apply(list_to_string)

        # Menghapus "Save all to author list" dari kolom penulis
        df['penulis'] = df['penulis'].apply(lambda x: x.replace('Save all to author list', ''))

        # Memisahkan nama-nama penulis berdasarkan pemisah ;
        df['penulis'] = df['penulis'].apply(lambda x: x.split(';'))

        df['penulis'] = df['penulis'].apply(cleaningPenulis)

        # Menyatukan nama-nama penulis dalam satu list
        df['penulis'] = df['penulis'].apply(lambda x: ', '.join(x))

        df = df.dropna()

        df['abstrak'] = df['abstrak'].apply(cleaningAbstrakTahap1)

        df['abstrak'] = df['abstrak'].apply(translate_text)

        df['abstrak'] = df['abstrak'].apply(cleaningAbstrakTahap2)

        df['aspects'] = df['sdgs'].apply(get_aspects)

        df['aspects'] = df['aspects'].apply(lambda y: np.nan if len(y)==0 else y)
        df = df.drop(["sdgs"],axis=1)

        df = df.rename(columns={'aspects': 'Aspects','judul':'Judul','penulis':'Penulis','abstrak':'Abstrak','tahun':'Tahun'})

        df_sinta = df.loc[df['Aspects'].isnull()]

        df_sinta = df.drop(['Aspects'],axis = 1)

        df_sinta.to_json('df_sinta_nolabel.json', orient='records')

        df = df.dropna()

        aspects = df['Aspects']

        # Membuat dataframe baru dengan kolom SDG yang berisi nilai 0 atau 1 sesuai dengan keberadaan goals pada setiap SDG
        sdgs_columns = ['SDG{}'.format(i) for i in range(1, 18)]  # Membuat nama kolom SDG
        for sdg_col in sdgs_columns:
            df[sdg_col] = df['Aspects'].apply(lambda x: 1 if sdg_col in x else 0)

        # Menghapus kolom 'goals' karena sudah tidak diperlukan lagi
        # df.drop(columns=['goals'], inplace=True)

        # Menampilkan dataframe
        aspectsList = df['Aspects']

        df = df.drop(['Aspects'],axis = 1)

        df.to_json('preprocessSinta/df_sinta_berlabel.json', orient='records')

    except Exception as e:
        print("Terjadi error:",str(e))

