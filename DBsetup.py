import sqlite3
from Scrapper import GetValues, productList
import schedule


### lines needed to db working
connection = sqlite3.connect('prices.db')
cursor=connection.cursor()



def db_create_product(product):
    str = 'CREATE TABLE {} (shopName text , price real)'.format(product)
    cursor.execute(str)

# this will add actual values to db
def db_add_values():

    for table ,url in productList.items():

        valuesDict = GetValues(url)

        for key, value in valuesDict.items():

            str = 'INSERT INTO {} VALUES ("{}",{})'.format(table, key, value)

            cursor.execute(str)


# this function clear all rows in all tables in Db
def db_delete_values():
    for table in productList.keys():
        str = 'DELETE FROM {}'.format(table)
        cursor.execute(str)




def db_update_values():
    db_delete_values()
    connection.commit()

    db_add_values()
    connection.commit()
    print('Baza została zaaktualizowana ')



# it need to be schedule always couple minutes after send_email

schedule.every().day.at("12:32").do(db_update_values)
schedule.every().day.at("15:32").do(db_update_values)
schedule.every().day.at("17:02").do(db_update_values)
schedule.every().day.at("18:02").do(db_update_values)
schedule.every().day.at("22:02").do(db_update_values)

while True :
    schedule.run_pending()
