#!/usr/bin/env python3

from oplib import OpenLibrary, AdvancedSearchType
import pandas as pd
import json

if __name__ == "__main__":
    oplib = OpenLibrary()

    # TODO: Change the search options based on your needs
    start_day,start_month,start_year = 1,1,2023
    end_day,end_month,end_year = 5,1,2023
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
        print(f'Scraping {file}......')

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
        # file_name = f'{start_day}-{start_month}-{start_year}_{end_day}-{end_month}-{end_year}_{file}.xlsx'
        # df.to_excel(file_name, index=False)

        # print(f'\nFinish Scraping all {file} data!\nfile name :  {file_name}\n\n')

        #Save JSON File
        file_name = f'{start_day}-{start_month}-{start_year}_{end_day}-{end_month}-{end_year}_{file}.json'

        # Menyimpan data ke file JSON
        df.to_json(file_name, orient='records')

        print(f'\nFinish Scraping all {file} data!\nfile name :  {file_name}\n\n')
        


