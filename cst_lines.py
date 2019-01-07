"""
Constellation drawing data files (CSV) downloaded from the Google Spreadsheet ()

columns
 0. Constellation ID (3 alpha)
 1. Line width
 2. HD of the star
 ... list
"""
import csv
##import json
##import os
##import math

'''
Constellation JSON
------------------
"cst": "PSC", 

"PSC":[[],[],...],

'''

with open('dataCSV/zodiac_lines.csv', 'r', encoding='utf-8') as cf:
    in_data = csv.reader(cf, delimiter=',')
    print('{', end='')
    cstPrev = None
    for row in in_data:
        if (not row[0] or not row[0][:3].isalpha()):   # skip header part
            continue
        cst     = row[0]  # constellation abbrev.
        width   = row[1]
        hd_list = '';
        for i, hd in enumerate(row[1:]):
            if not hd:
                break
            if i == 0:
                hd_list = str(hd)   # actually this is the line width, not HD
            else:
                hd_list += ','
                # Henry Draper Catalogue, ex, 60179A (so need to be converted to hex)
                hd_list += str(int(hd, 16))
        if cst == cstPrev:
            print(',', end='')
        else:
            if cstPrev:      # not the beginning of the data
                print('],')  # close the previous constellation group
            cstPrev = cst
            print('"' + cst + '":[', end='')  # start constellation
        print('[' + hd_list + ']', end='')
    print(']}')
