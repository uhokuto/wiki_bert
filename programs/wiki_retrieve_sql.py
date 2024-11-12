# -*- coding: utf-8 -*-
import mysql.connector

# MySQLに接続
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="jawiki_category",# database名
    charset='utf8'
    
)

# カーソルを取得
cursor = conn.cursor()
select_all_data_query = "SELECT * FROM  categorylinks"# table名

# データ取得
cursor.execute(select_all_data_query)

#one = cursor.fetchone()


# 結果を取得

result = cursor.fetchall()

# 結果を表示
for row in result:
    
    print(row[1].decode("utf8"))
    print(row[2].decode("utf8"))
    #print(one[3].decode("utf8"))
    print(row[4].decode("utf8"))
    
    print(row)
   
cursor.close()
conn.close()
