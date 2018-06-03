import sqlite3
from sqlite3 import Error
import pickle
import operator
from nlp import query_db

db_path = r"sqlite.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()


## create table in db
def create_table():
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""DROP TABLE If exists matrix""")
        cursor.execute("""CREATE TABLE matrix(id INTEGER PRIMARY KEY, about INTEGER, safety INTEGER, terrorism INTEGER,
                 entry INTEGER, health INTEGER, history INTEGER, culture INTEGER, attractions INTEGER, shopping INTEGER,
                nightlife INTEGER, getting_around INTEGER)""")
        conn.commit()
    except Error as e:
        print(e)
    finally:
        conn.close()
#create_table()


## insert matrix for activity types
def insert_matrix(v1, v2, v3, v4, v5, v6, v7, v8, v9 ,v10, v11):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""INSERT INTO matrix(about, safety, terrorism, entry, health, history, culture, attractions, shopping, nightlife, getting_around)
                                VALUES(?,?,?,?,?,?,?,?,?,?, ?)"""
                       , (v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11))
        print("inserted data done")
        conn.commit()
    except Error as e:
        print(e)
    finally:
        conn.close()


## creates matrix for activity types
def create_matrix():
    matrix_old = {"culture":   [0.7, 0.5, 0.5, 0.5, 0.3, 1, 1, 0.3, 0.7, 0.3, 0.5],
              "nightlife": [0.2, 0.5, 0.5, 0.5, 0.5, 0.3, 0.3, 1, 1, 1, 0.7],
              "activity":  [0.5, 0.5, 0.5, 0.5, 1, 0.5, 0.5, 0.7, 0.5, 0.5, 1]}
    matrix = {"culture":   [1,1,1,1,0,2,2,0,0,0,1],
              "nightlife": [0,1,1,1,1,0,0,1,1,2,1],
              "activity":  [1,1,1,1,1,0,1,2,2,1,2]}

    for key, items in matrix.items():
        insert_matrix(items[0],items[1],items[2],items[3],items[4],items[5],items[6],items[7],items[8],items[9],items[10])
#create_matrix()


## creates id for given type
def get_type_id(type):
    if type == "culture":
        type_id = 1
    elif type == "nightlife":
        type_id = 2
    elif type == "activity":
        type_id = 3
    else:
        print("You did not choose a valid type")
    return type_id


## gets the best fit for input country out of db and returns top 3 matches

def calc_best_fit_sim(id, type):
    country = query_db("""Select * from similarity where id = {}""".format(id))
    type_id = get_type_id(type)
    matrix = query_db("""Select * from matrix where id = {}""".format(type_id))
    about = pickle.loads(country[2])
    safety = pickle.loads(country[3])
    terrorism = pickle.loads(country[4])
    entry = pickle.loads(country[5])
    health = pickle.loads(country[6])
    history = pickle.loads(country[7])
    culture = pickle.loads(country[8])
    attractions = pickle.loads(country[9])
    shopping = pickle.loads(country[10])
    nightlife = pickle.loads(country[11])
    getting_around = pickle.loads(country[12])
    sum_list = []
    for about, safety, terrorism, entry, health, history, culture, attractions, shopping, nightlife, getting_around in zip(about, safety, terrorism, entry, health, history, culture, attractions, shopping, nightlife, getting_around):
        sum_list.append([about[0], (about[1]*matrix[1]+
                                    safety[1]*matrix[2]+
                                    terrorism[1]*matrix[3]+
                                    entry[1]*matrix[4]+
                                    health[1]*matrix[5]+
                                    history[1]*matrix[6]+
                                    culture[1]*matrix[7]+
                                    attractions[1]*matrix[8]+
                                    shopping[1]*matrix[9]+
                                    nightlife[1]*matrix[10]+
                                    getting_around[1]*matrix[11])])
    return sum_list

def calc_best_fit_lsa(id, type):
    country = query_db("""Select * from lsa_model where id = {}""".format(id))
    type_id = get_type_id(type)
    matrix = query_db("""Select * from matrix where id = {}""".format(type_id))
    about = pickle.loads(country[2])
    safety = pickle.loads(country[3])
    terrorism = pickle.loads(country[4])
    entry = pickle.loads(country[5])
    health = pickle.loads(country[6])
    history = pickle.loads(country[7])
    culture = pickle.loads(country[8])
    attractions = pickle.loads(country[9])
    shopping = pickle.loads(country[10])
    nightlife = pickle.loads(country[11])
    getting_around = pickle.loads(country[12])
    sum_list = []
    for about, safety, terrorism, entry, health, history, culture, attractions, shopping, nightlife, getting_around in zip(about, safety, terrorism, entry, health, history, culture, attractions, shopping, nightlife, getting_around):
        sum_list.append([about[0], (about[1]*matrix[1]+
                                    safety[1]*matrix[2]+
                                    terrorism[1]*matrix[3]+
                                    entry[1]*matrix[4]+
                                    health[1]*matrix[5]+
                                    history[1]*matrix[6]+
                                    culture[1]*matrix[7]+
                                    attractions[1]*matrix[8]+
                                    shopping[1]*matrix[9]+
                                    nightlife[1]*matrix[10]+
                                    getting_around[1]*matrix[11])])
    return sum_list

def calc_best_fit(id, type):
    sum_list1 = calc_best_fit_sim(id, type)
    sum_list2 = calc_best_fit_lsa(id, type)
    sum_list3 = []
    for i in sum_list2:
        sum_list3.append([i[0],i[1]*-1])
    sum_list = []
    for x,y in zip(sum_list1, sum_list2):
        sum_list.append([x[0], y[1]+y[1]])
    sum_list_sorted = sorted(sum_list3, key=operator.itemgetter(1), reverse=True)

    fit0 = query_db("""Select name from countries where id = {}""".format(sum_list_sorted[0][0]))
    fit1 = query_db("""Select name from countries where id = {}""".format(sum_list_sorted[1][0]))
    fit2 = query_db("""Select name from countries where id = {}""".format(sum_list_sorted[2][0]))
    return fit0, fit1, fit2