#!/usr/bin/env python3

from oplib import OpenLibrary, AdvancedSearchType
from preprocessOplib import PreprocessLibrary
import pandas as pd
import numpy as np
import datetime
import json

if __name__ == "__main__":
    oplib = OpenLibrary()
    preprocess = PreprocessLibrary()

    # TODO: Change the search options based on your needs

    # Get current date
    current_date = datetime.date.today()

    # Extract year, month, and day
    year = current_date.year
    month = current_date.month
    day = current_date.day

    one_month_ago = current_date - datetime.timedelta(days=90)

    year2 = one_month_ago.year
    month2 = one_month_ago.month
    day2 = one_month_ago.day
    
    start_day,start_month,start_year = day2,month2,year2
    end_day,end_month,end_year = day,month,year
    print(day,month,year)
    print(day2,month2,year2)
    publication_type =[AdvancedSearchType.SKRIPSI, 
                       AdvancedSearchType.TA,
                       #AdvancedSearchType.THESIS
                       ]

    for i in range(len(publication_type)):
        search_options = {
            'search[type]': publication_type[i],
            'search[number]': '',
            'search[title]': '',
            'search[author]': '',
            'search[publisher]': '',
            'search[editor]': '',
            'search[subject]': '',
            'search[classification]': '',
            'search[location]': '',
            'search[entrance][from][day]': start_day,
            'search[entrance][from][month]': start_month,
            'search[entrance][from][year]': start_year,
            'search[entrance][to][day]': end_day,
            'search[entrance][to][month]': end_month,
            'search[entrance][to][year]': end_year,
        }

        if publication_type[i] == 4 : 
            file = 'SKRIPSI' 
        elif publication_type[i] == 6 :
            file = 'TA'
        print(f'Scraping {file} at',day,month,year,'to ',day2,month2,year2,'......')

        content = oplib.get_all_data_from_range_date(**search_options)
        results = oplib.parse_results(content)
    
        df = pd.DataFrame({'title': [],
                        'classification' : [],
                        'type_publication' : [],
                        'subject' : [],
                        'abstract' : [],
                        'keywords' : [],
                        'author' : [],
                        'lecturer' : [],
                        'publisher' : [],
                        'publish_year' : []
        })

        for index, totals, data in results:
            df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
            # print(f"[{index}/{totals}]: {data['title']}")

        # #Save csv file 
        file_name = f'{start_day}-{start_month}-{start_year}_{end_day}-{end_month}-{end_year}_{file}.xlsx'
        df.to_excel(file_name, index=False)

        print(f'\nFinish Scraping all {file} data!\nfile name :  {file_name}\n\n')

        # Lakukan preprocess
        try:
            df = pd.read_json("contoh hasil keluaran_skripsi.json")
            df = df.rename(columns={'title': 'Judul', 'author': 'Penulis1', 'lecturer': 'Penulis2', 'publish_year': 'Tahun', 'abstract': 'Abstrak'})
            df = df[["Judul", "Penulis1", "Penulis2", "Tahun", "Abstrak"]]

            df = df.dropna()

            df['Abstrak'] = df['Abstrak'].apply(preprocess.cleaningAbstrak)
            df['Judul'] = df['Judul'].apply(preprocess.cleaningJudul)
            df["Penulis1"] = df["Penulis1"].apply(preprocess.cleaningPenulis)
            df["Penulis"] = df["Penulis1"] + ", " + df["Penulis2"]
            df = df.drop(["Penulis1", "Penulis2"], axis=1)
            df = df[["Judul", "Tahun", "Abstrak", "Penulis"]]
            df["Tahun"] = df["Tahun"].astype(int)

            df['Abstrak'] = df['Abstrak'].replace('', np.nan)
            df['Judul'] = df['Judul'].replace('', np.nan)
            df = df.dropna()

            df = df[["Judul", "Penulis", "Tahun", "Abstrak"]]

            # Save preprocessed JSON File
            preprocessed_file_name = f'preprocessedOplib_{start_day}-{start_month}-{start_year}_{end_day}-{end_month}-{end_year}_{file}.json'
            df.to_json("TestingData", orient='records')
            # print("Beres")
            print(f'\nFinish Preprocessing all {file} data!\nfile name : {preprocessed_file_name}\n\n')

        except Exception as e:
            print("Terjadi error:", str(e))
        #Save JSON File
        

