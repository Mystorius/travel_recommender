import sqlite3
from sqlite3 import Error
import gensim
from nltk import word_tokenize
import operator
import pickle

path = r"C:\Users\Mystorius\Desktop\travel_recommender"
db_path = r"C:\Users\Mystorius\Desktop\travel_recommender\sqlite.db"


## create table for similarity storage in sql db
def create_table():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        #cursor.execute("""DROP TABLE If exists similarity""")
        cursor.execute("""CREATE TABLE similarity(id INTEGER PRIMARY KEY, name TEXT, about BLOB, safety BLOB,
            terrorism BLOB, entry BLOB, health BLOB, history BLOB, culture BLOB, attractions BLOB,
            shopping BLOB, nightlife BLOB, getting_around BLOB)""")
        conn.commit()
    except Error as e:
        print(e)
    finally:
        conn.close()
#create_table()


## insert data into sql db
def insert_calculation(name1, about1, safety1, terrorism1, entry1, health1, history1, culture1,
                 attractions1, shopping1, nightlife1, getting_around1):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO similarity(name, about, safety, terrorism, entry, health,
                            history, culture, attractions, shopping, nightlife, getting_around)
                             VALUES(?,?,?,?,?,?,?,?,?,?,?,?)"""
                       , (name1, about1,safety1, terrorism1, entry1, health1, history1, culture1,attractions1, shopping1,
                         nightlife1, getting_around1))
        print("inserted data for %s" % name1)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        conn.close()

## querey db and give back a list
def query_db(query):
    result = []
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        output = cursor.execute(query)
        conn.commit()
    except Error as e:
        print(e)
    finally:
        for i in output:
            for j in i:
                result.append(j)
        conn.close()
        return result


## gets sim object to use for compare countries
def get_sim(col_id):
    compare_all = []
    for i in range(1,323):
        compare = query_db("""Select * from countries where id = {}""".format(i))
        compare_all.append(compare[col_id])

    gen_doc = [[w.lower() for w in word_tokenize(i)] for i in compare_all]
    dict = gensim.corpora.Dictionary(gen_doc)
    corpus = [dict.doc2bow(i) for i in gen_doc]
    tf_idf = gensim.models.TfidfModel(corpus)
    sim_measure = gensim.similarities.Similarity(path,tf_idf[corpus], num_features=len(dict))
    return sim_measure, tf_idf, dict


## compares tf_idf of input to dataset (sim)
def compare_to(id):
    global_list_result = []
    col_id_list = [2, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    ## get data from compare countrie
    compare = query_db("""Select * from countries where id = {}""".format(id))
    name = compare[1]

    ## do the calc for all entrys in database
    for col_id in col_id_list:
        sim_measure, tf_idf, dict = get_sim(col_id)
        compare_doc = [w.lower() for w in word_tokenize(compare[col_id])]
        compare_corpus = dict.doc2bow(compare_doc)
        compare_tf_idf = tf_idf[compare_corpus]
        sim = sim_measure[compare_tf_idf]

        list_result = []
        id = 1
        for i in sim:
            list_result.append([id, i])
            id +=1
        global_list_result.append(list_result)
    return global_list_result, name


## compares for each country and insert data in db
def Main():
    for i in range(1, 323):
        print("start with id: %s" % i)
        global_list_result, name = compare_to(i)
        insert_calculation(name,
                           pickle.dumps(global_list_result[0]),
                           pickle.dumps(global_list_result[1]),
                           pickle.dumps(global_list_result[2]),
                           pickle.dumps(global_list_result[3]),
                           pickle.dumps(global_list_result[4]),
                           pickle.dumps(global_list_result[5]),
                           pickle.dumps(global_list_result[6]),
                           pickle.dumps(global_list_result[7]),
                           pickle.dumps(global_list_result[8]),
                           pickle.dumps(global_list_result[9]),
                           pickle.dumps(global_list_result[10]))


if __name__ == '__main__':
        Main()


