import numpy as np
import lxml.html
import glob
import unicodedata
import re
import pymongo
	

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["wiki"]
reviews_collection = db['jawiki2024']

def get_doc(path):
    #f = open('../text/AA/wiki_00', 'r', encoding='UTF-8')
    f = open(path, 'r', encoding='UTF-8')
    bodyHtml = f.read()

    root = lxml.html.fromstring(bodyHtml)
    #div class="rvw-item__visit-contents">
    x_path = root.xpath("//doc")

    documents = []
    for i,p in enumerate(x_path):
        doc = {}
        #print(p.text_content())
        
        # UNICODE標準化や改行削除などでクリーニング
        text = unicodedata.normalize('NFKC', p.text_content())
        text = text.replace('\n', '')
        text = re.sub(r'[“”]', '', text)
        text = re.sub(r'https?:\/\/.*?[\r\n ]', '', text)

        # ↓ここらへんでSQLまわりの処理を書く
        
        #print(p.get('title'))
        doc['id'] = p.get('id')
        doc['title'] = p.get('title')
        doc['body'] = text
        
        
        documents.append(doc)
        
    return documents
        
        
        
pathes = glob.glob('../text/*/wiki*')
       
for page,path in enumerate(pathes):

    docs = get_doc(path)
    print(docs)
    reviews_collection.insert_many(docs)
    
    
        