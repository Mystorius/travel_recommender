from calc_fit import calc_best_fit
from calc_fit import query_db


def Main():
    # id_list = []
    # for i in range(0,3):
    #     country_id = input("Please input country No. {} you like: ".format(i + 1))
    #     id_list.append(country_id)
    name = input("Please input country you like: ")
    country_id = query_db("""Select id from countries where name like "{}" """.format(name))
    type = input("Please input your favorite journey type. You get to choose from: culture, nightlife, activity: ")
    fit0, fit1, fit2 = calc_best_fit(country_id[0], type)
    print(fit0, fit1, fit2)

if __name__ == '__main__':
    while True:
        Main()

