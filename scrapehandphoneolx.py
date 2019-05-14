# -*- coding: utf-8 -*-
#rachmat_sn
# scrapy runspider scrapeolx.py

import scrapy
import sqlite3

count = 0
page_url = []

#SQLITE3
dbname = 'handphoneOLX.db'
conn = sqlite3.connect(dbname)
c = conn.cursor()

def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS handphone(ad_id TEXT, img TEXT, txt TEXT, brand TEXT, label TEXT, city TEXT, price INTEGER, UNIQUE(ad_id))")
    c.execute("DELETE FROM handphone")

#SCRAPY
def textBeautify(data):
    return list(map(lambda s: s.strip(), data))

def textBeautifyBrand(data):
    return list(map(lambda s: s.strip()[12:], data))

def rupiahToNumber(rupiah):
    noRp = rupiah[3:]
    noDot = noRp.replace(".", "")
    if noDot == '':
        return ''
    else:
        integer = int(noDot)
        return integer

def generate_page_url():
    numofpage = 400
    for i in range(1,numofpage):
        if i==1:
            page_url.append('https://www.olx.co.id/elektronik-gadget/handphone/?view=list')
        else:
            page_url.append('https://www.olx.co.id/elektronik-gadget/handphone/?view=list&page='+str(i))
    return page_url
        
class ScrapeolxSpider(scrapy.Spider):
    name = 'scrapehandphoneolx'
    create_table()
    page_url = generate_page_url()
    #print(page_url)
    
    def start_requests(self):
        for url in page_url:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):        
        print('test')
        ad_id = textBeautify(response.css('td.offer>table>tbody>tr::attr(data-ad-id)').extract())
        img = textBeautify(response.css('td.offer>table>tbody>tr>td>span>a>img.fleft::attr(src)').extract())
        txt = textBeautify(response.css('td.offer>table>tbody>tr>td>h2>a::text').extract())
        
        #brand################################
        BR = response.css('td.offer>table>tbody>tr>td>p>small.breadcrumb::text').extract() #brand
        brand = []
        for i in range (0, len(BR),3):
            brand.append(BR[i])
        brand = textBeautifyBrand(brand)
        
        label = textBeautify(response.css('td.offer>table>tbody>tr>td>p>small.breadcrumb>label::text').extract())
        city = textBeautify(response.css('td.offer>table>tbody>tr>td>p>small.breadcrumb>span::text').extract())
        price = textBeautify(response.css('td.offer>table>tbody>tr>td>div>p.price>strong::text').extract())    
        
#        print(ad_id)
#        print(img)
#        print(txt)
#        print(brand)
#        print(city)
#        print(label)
#        print(price)
        #cari yg panjangnya paling kecil untuk acuan
        jum_data_per_iter = min([len(ad_id), len(img), len(txt), len(brand), len(label), len(city), len(price)])
        for it in range(jum_data_per_iter):
            scraped_info = {
                'ad_id': ad_id[it],
                'img': img[it],
                'txt': txt[it],
                'brand': brand[it],
                'label': label[it],
                'city': city[it],
                'price': rupiahToNumber(price[it]), 
            }
            
            #commit jika semua data tidak kosong '' DAN brand bukan 'Lain-lain'
            if(scraped_info['ad_id']!='' and scraped_info['img']!='' and scraped_info['txt']!='' and scraped_info['brand']!='' and scraped_info['label']!='' and scraped_info['city']!='' and scraped_info['price']!='' and scraped_info['brand']!='Lain-lain'):
                c.execute("INSERT OR IGNORE INTO handphone (ad_id, img, txt, brand, label, city, price) VALUES(?,?,?,?,?,?,?)",
                      (scraped_info['ad_id'],scraped_info['img'], scraped_info['txt'], scraped_info['brand'], scraped_info['label'], scraped_info['city'], scraped_info['price']))
                conn.commit()
                
            yield scraped_info