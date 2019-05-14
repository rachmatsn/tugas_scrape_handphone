# -*- coding: utf-8 -*-
#rachmat_sn

import sqlite3
import json

conn = sqlite3.connect('handphoneOLX.db')
c = conn.cursor()

data = {} #dictionary
city = "Bandung Kota"
kondisi = ["Baru", "Bekas"]
#brand = ['honda', 'yamaha', 'suzuki', 'kawasaki']

#mendapatkan brand terbanyak yang dijual
brand = []
query = c.execute("SELECT brand FROM handphone WHERE (city == '"+city+"') GROUP BY brand ORDER BY COUNT(brand) DESC LIMIT 5")
ftch = c.fetchall()
for i in range (len(ftch)):
    brand.append(ftch[i][0])
data['labels'] = brand
print (brand)

#mendapatkan jumlah hp baru dan bekas 
for i in range(len(brand)):
    result = []
    for j in range(len(kondisi)):
        query = c.execute("SELECT count(brand) FROM handphone WHERE (brand == '"+brand[i]+"' and city =='"+city+"' and label == '"+kondisi[j]+"') GROUP BY brand ORDER BY COUNT(brand) DESC LIMIT 5")
        ftch = c.fetchall()
        if not ftch:
            hsl = 0
        else:
            hsl = int(ftch[0][0])
        result.append(hsl)
    data["k"+str(i+1)] = result

print(data)

#simpan file
with open('dictionary_handphone.txt', 'w') as fp:
    json.dump(data, fp)
    
c.close()
conn.close()
