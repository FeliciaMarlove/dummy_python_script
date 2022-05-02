from random import choice, random, randint

import requests #http requets library
import psycopg2 #postgres driver for python

url = 'server_url'


def pick_car():
    try:
        for _ in range(10):
            conn = psycopg2.connect(
                host="host_name",  # database server address e.g., localhost or an IP address
                database="db_name",
                user="db_user",
                password="db_pwd")
            # port: the port number that defaults to 5432 if it is not provided.
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM car c WHERE c.ongoing = true AND c.fuel != 4')
            valid_cars = cursor.fetchall()
            random_car_to_fill_up = choice(valid_cars)
            print(random_car_to_fill_up)
            post_fill_up(random_car_to_fill_up)
            cursor.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


def post_fill_up(random_car_to_fill_up):
    choose_discrepancy = randint(1, 10)

    plate = random_car_to_fill_up[0]
    cons = random_car_to_fill_up[1]
    fuel = random_car_to_fill_up[5]
    km = random_car_to_fill_up[6]

    random_km = randint(400, 600)

    # shooting wrong_fuel or before>after discrepancy with a randomly picked number
    if choose_discrepancy == 2:
        fuel = randint(0, 3)  # really dummy random because there's a chance it picks the same fuel
        new_km = km + random_km
    elif choose_discrepancy == 5:
        new_km = km - random_km
    else:
        new_km = km + random_km
    random_variant_percentage = randint(0, 25)
    dangerous_consumption = cons + ((cons / 100) * random_variant_percentage)
    random_liters = round((dangerous_consumption / 100) * random_km, 2)

    r = requests.post(url + '/api/fillup', json={"plateNumber": plate,
                                                 "fuelType": fuel,
                                                 "kmAfter": new_km,
                                                 "liters": random_liters})
    print('post request result ', r.status_code)


pick_car()
