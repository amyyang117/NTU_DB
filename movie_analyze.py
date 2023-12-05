
import pymysql
import pandas as pd
from wordcloud import WordCloud
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import jieba
import jieba.analyse
from collections import Counter 
from config import DB_PASSWORD


config = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": DB_PASSWORD,
    "db": "Movie"
}

def check_movie_name(content):
    for name in movie_list:
        if name in content:
            return name

def connect_db():
    try:
        conn = pymysql.connect(**config)
        print('connect_success')
    except Exception as ex:
        print(ex)
    
    return conn

conn = connect_db()
with conn.cursor() as cursor:

    try:

        sql_tickets = '''SELECT DISTINCT name FROM Movie.tickets'''
        cursor.execute(sql_tickets)
        movie = cursor.fetchall()
        movie_list = [t[0] for t in movie]

        sql_dcard = '''SELECT * FROM db2023_hw5_dcard_movie'''
        cursor.execute(sql_dcard)
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        df_dcard = pd.DataFrame(results, columns=column_names)
        df_dcard.drop_duplicates(inplace=True)
        df_dcard['movie_name'] = df_dcard['title'].apply(check_movie_name)

        sql_ptt = '''SELECT * FROM db2023_hw5_ptt_movie'''
        cursor.execute(sql_ptt)
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        df_ptt = pd.DataFrame(results, columns=column_names)
        df_ptt.drop_duplicates(inplace=True)
        df_ptt['movie_name'] = df_ptt['title'].apply(check_movie_name)

    except Exception as ex:
        print(ex)

    finally:
        cursor.close()

conn.close()

def plot_cloud(text_data, title):
	
    plt.rcParams['font.sans-serif'] = ['Taipei Sans TC Beta']
    font_path = "PingFang.ttc"  # 字型檔

    jieba.set_dictionary("dict.txt")
    jieba.analyse.set_stop_words("stopwords.txt")
    for movie in movie_list:
        jieba.add_word(movie)

    tags = jieba.analyse.extract_tags(text_data, topK=20)

    seg_list = jieba.lcut(text_data, cut_all=False)
    dictionary = Counter(seg_list)

    freq = {}
    for ele in dictionary:
        if ele in tags:
            freq[ele] = dictionary[ele]

    wordcloud = WordCloud(background_color='white',font_path=font_path, width=1280, height=720).generate_from_frequencies(freq)

    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    plt.show()

# only好雷
txt = ','.join(df_ptt[df_ptt['title'].str.contains('好雷')]['title'])
txt = txt.replace('好雷', '')
txt = txt.replace('Re', '')
plot_cloud(txt, '好雷的文字圖')

# 負雷
txt = ','.join(df_ptt[df_ptt['title'].str.contains('負雷')]['title'])
txt = txt.replace('負雷', '')
txt = txt.replace('Re', '')
plot_cloud(txt, '負雷的文字圖')