from calc_fit import calc_best_fit
from calc_fit import query_db

'''This section is just a user based input and my given outputs'''

def Main():
    name = input("Please input country you like: ")
    country_id = query_db("""Select id from countries where name like '{}' """.format(name))
    type = input("Please input your favorite journey type. You get to choose from: culture, nightlife, activity: ")
    fit0, fit1, fit2 = calc_best_fit(country_id[0], type)
    print("Countries you might like to visit: {0}, {1} or {2}".format(fit0[0], fit1[0], fit2[0]))

if __name__ == '__main__':
    while True:
        Main()

