"""
Constellation data files (CSV) downloaded from the Google Spreadsheet (http://bit.ly/2FdYQNN)

==================
Source CSV columns
------------------
[constellation.csv]
--- Basic Fields from Wikipedia (Jan,2019)
 0. Constellation ID (IAU 3 alpha)
 1. Name
 2. Bayer designation
 3. Flamsteed designation
 4. Gould designation
 5. Variable star designation
 6. HD: Henry Draper Catalogue (candidate for primary key but missing more that 10%)
 7. HIP: Hipparcos Catalogue
 8. RA: Right Ascension (sexagesimal, ex, 03h 46m 02.89s)
 9. Dec: Declination    (sexagesimal, ex, +24° 31′ 40.8″)
10. vis: Apparent Magnitude
11. abs: Absolute Magnitude
12. Dist: Distance in Light Year
13. Sp. class: Spectrum Class (ex, A0Vn, K5, F7V, G9III, K0)
14. Notes
--- Extended Fields
15. Famous Name

[cst_boundaries.csv] (http://pbarbier.com/constellations/boundaries.html)

[deepsky.csv] * Other celestial objecsts such as nebulae, star clusters, and galaxies
- Messier objects (110): https://en.wikipedia.org/wiki/List_of_Messier_objects
  M42 Orion nebula, M31 Andromeda galaxy, M45 Pleiades star cluster
- Caldwell catalogue (109) by Patrick Moore: https://en.wikipedia.org/wiki/Caldwell_catalogue
  Hyades
- NGC(New General Catalogue): https://en.wikipedia.org/wiki/New_General_Catalogue

=======================
Intermediary JSON files
-----------------------
* Intermediary source files
[cst_stars_src.json]
- Constellation ID
- HD_hex (HD catalogue # converted to Hex, to cover numbers postfixed with 'A'~'F')
- RA, Dec in degree (finally required format is radian but degree is preferred for precision)
- Apparent Magnitude

[cst_lines_src.json]
- Constellation ID
- line width
- list of star HD_hex's (in a pen down and same line-width drawing)

[cst_illust.svg]
- constellations illustration artworks in svg (needs a drawing tool)

==========================
Destination JSON structure
--------------------------
[cst_comp.json] * Final compilation optimized for the runtime JS
Recipe
1. Remove HD_hex used as a foreign key to reference stars, use the serialized stars array index
2. Normalize Constellation ID, making a separate 88 constellations table and use the index
{
"Constellations": [
  ["AND"]
],
"Stars": [

],
"Lines": [

],
"Boundaries": [

],
"Illustrations": [

],
}


"""
import csv
##import json
##import os
##import math

'''
Hour Minute Second to Degree Converter
'''
def HMS2deg(ra='', dec=''):  # Right Ascension, Declination
    RA, DEC, rs, ds = '', '', 1, 1
    if dec:
        try:
            D, M, S = [float(i) for i in dec.split()]
        except ValueError:
            print("error in Dec:", dec)
            return
        if str(D)[0] == '-':
            ds, D = -1, abs(D)
        deg = D + (M/60) + (S/3600)
        DEC = deg*ds   # apply math.radians() if you want radian

    if ra:
        try:
            H, M, S = [float(i) for i in ra.split()]
        except ValueError:
            print("error in RA:", ra)
            return
        if str(H)[0] == '-':
            rs, H = -1, abs(H)
        deg = (H*15) + (M/4) + (S/240)
        RA = deg*rs

    if ra and dec:
        return (RA, DEC)
    else:
        return RA or DEC

'''
Constellation JSON
------------------
"cst": "PSC", 

"PSC":[[349.0633,0.3067,12.9],[21.0667,32.8108,13.44],...],

'''

with open('dataCSV/zodiac.csv', 'r', encoding='utf-8') as cf:
    in_data = csv.reader(cf, delimiter=',')
    print('{', end='')
    cstPrev = None
    for row in in_data:
        if (not row[0][:3].isalpha()):   # skip header part
            continue
        if (not row[8] or not row[9]):   # position data
            continue
        cst = row[0]  # constellation abbrev.
        # Henry Draper Catalogue, ex, 60179A (so need to be converted to hex)
        hd  = int(row[6], 16) if row[6] else 0
        ra  = row[8].replace('h', '').replace('m', '').replace('s', '')
        dec = row[9].replace('°', '').replace('′', '').replace('″', '').replace('−', '-')
        ra, dec = HMS2deg(ra, dec)
        if row[10]:
            try:
                mag = float(row[10])
            except ValueError:
                #print("error in mag:", row[10])
                mag = 10
        # if mag <= 6:
        if cst == cstPrev:
            print(',', end='')
        else:
            if cstPrev:      # not the beginning of data
                print('],')  # close the previous constellation group
            cstPrev = cst
            print('"' + cst + '":[', end='')  # start constellation
        print('[' + str(hd) + ',' \
                  + str(round(ra, 5)) + ',' \
                  + str(round(dec, 5)) + ','  \
                  + str(mag) \
                  + ']', end='')
    print(']}')
