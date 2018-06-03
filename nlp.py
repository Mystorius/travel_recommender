import sqlite3
from sqlite3 import Error
import gensim
from gensim import models, similarities
import numpy as np
import matplotlib.pyplot as plt
import operator
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
import pickle

path = r"data"
db_path = r"sqlite.db"


## create table for similarity storage in sql db
def create_table():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""DROP TABLE If exists lsa_model""")
        cursor.execute("""CREATE TABLE lsa_model(id INTEGER PRIMARY KEY, name TEXT, about BLOB, safety BLOB,
            terrorism BLOB, entry BLOB, health BLOB, history BLOB, culture BLOB, attractions BLOB,
            shopping BLOB, nightlife BLOB, getting_around BLOB)""")
        conn.commit()
    except Error as e:
        print(e)
    finally:
        conn.close()
create_table()


## insert data into sql db
def insert_calculation(name1, about1, safety1, terrorism1, entry1, health1, history1, culture1,
                 attractions1, shopping1, nightlife1, getting_around1):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO lsa_model(name, about, safety, terrorism, entry, health,
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
    stop_words = set(stopwords.words("english"))
    stemmer = SnowballStemmer("english")
    #print(stop_words)
    #print(stemmer)
    for i in range(1,323):
        compare = query_db("""Select * from countries where id = {}""".format(i))
        compare_all.append(compare[col_id])
    #print(compare_all)
    #print("XXXXXXXXXXXXXXXXXXXXX")
    #gen_doc = [[w.lower() for w in word_tokenize(i)] for i in compare_all]
    gen_doc_new =  [[stemmer.stem(word) for word in document.lower().split() if (word not in stop_words)]
          for document in compare_all]

    #print("XXXXXXXXXXXXXXXXXXXXX")
    #dict = gensim.corpora.Dictionary(gen_doc)
    dict = gensim.corpora.Dictionary(gen_doc_new)
    #print(dict)
    #print("XXXXXXXXXXXXXXXXXXXXX")
    #corpus = [dict.doc2bow(i) for i in gen_doc]
    corpus = [dict.doc2bow(i) for i in gen_doc_new]
    #print(corpus)
    #print(corpus[3][:20])
    #print("XXXXXXXXXXXXXXXXXXXXX")
    tf_idf = gensim.models.TfidfModel(corpus)
    #print(tf_idf)
    #print("XXXXXXXXXXXXXXXXXXXXX")
    sim_measure = gensim.similarities.Similarity(path,tf_idf[corpus], num_features=len(dict))
    print(sim_measure)
    print("XXXXXXXXXXXXXXXXXXXXX")
    corpus_tfidf = tf_idf[corpus]
    #print(corpus_tfidf)
    #print("XXXXXXXXXXXXXXXXXXXXX")
    numpy_matrix = gensim.matutils.corpus2dense(corpus, num_terms=65764)
    #print(numpy_matrix)
    #print("XXXXXXXXXXXXXXXXXXXXX")
    s = np.linalg.svd(numpy_matrix, full_matrices=False, compute_uv=False)
    #print(s)
    #print("XXXXXXXXXXXXXXXXXXXXX")
    #plt.figure(figsize=(10, 5))
    #plt.hist(s[0], bins=100)
    #plt.xlabel('Singular values', fontsize=12)
    #plt.show()
    lsa = models.LsiModel(corpus_tfidf, id2word=dict, num_topics=95)
    print(lsa)
    print("XXXXXXXXXXXXXXXXXXXXX")
    #index = similarities.MatrixSimilarity(lsa[corpus_tfidf])
    index = similarities.Similarity(path,lsa[corpus_tfidf], num_features=len(dict))
    print(index)
    print("XXXXXXXXXXXXXXXXXXXXX")
    #return sim_measure, tf_idf, dict
    return index, tf_idf, dict
#get_sim(2)

#
#
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
        #print(sim)
        # vec_lsi = lsi[doc]
        # sims = index[vec_lsi]
        # total_sims = np.concatenate([total_sims, sims])
        # similarity = []

        list_result = []
        id = 1
        for i in sim:
            list_result.append([id, i])
            id +=1
        global_list_result.append(list_result)
    return global_list_result, name
global_list_result, name = compare_to(1)
print(global_list_result)
print("XXXXXXXXXXXXXXXXXXXXX")
about = global_list_result[2]
print(about)
print("XXXXXXXXXXXXXXXXXXXXX")
sorted = sorted(about, key=operator.itemgetter(1), reverse=True)
print(sorted)


#
# ## compares for each country and insert data in db
# def insert_data():
#     for i in range(1, 323):
#         print("start with id: %s" % i)
#         global_list_result, name = compare_to(i)
#         insert_calculation(name,
#                            pickle.dumps(global_list_result[0]),
#                            pickle.dumps(global_list_result[1]),
#                            pickle.dumps(global_list_result[2]),
#                            pickle.dumps(global_list_result[3]),
#                            pickle.dumps(global_list_result[4]),
#                            pickle.dumps(global_list_result[5]),
#                            pickle.dumps(global_list_result[6]),
#                            pickle.dumps(global_list_result[7]),
#                            pickle.dumps(global_list_result[8]),
#                            pickle.dumps(global_list_result[9]),
#                            pickle.dumps(global_list_result[10]))
# #insert_data()
#
