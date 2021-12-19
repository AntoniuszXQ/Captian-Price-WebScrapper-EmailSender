from bs4 import BeautifulSoup
import requests
import sqlite3

header={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 OPR/80.0.4170.91'}




connection = sqlite3.connect('prices.db')
cursor = connection.cursor()


### here you add products you want to check {product name : product url}
product_list = {'Multipic35': 87856739 , 'Multipic24': 78944802, 'Multipic51': 111580327}


### function which will retrun prices and shop names in dictionary
def get_values(Url):
        global product_name , price_list , name_list
        html = requests.get('https://ceneo.pl/{}'.format(Url),headers=header).text
        soup = BeautifulSoup(html,'lxml')
        price_card = soup.find_all('a', class_='product-price go-to-shop')
        offer_card = soup.find_all('div', class_='product-offer__details__toolbar')
        offer_name = soup.find('div', class_='product-top__title')
        product_name=offer_name.find('h1').get_text()
        price_list = []
        names_list=[]


### Creating a list of shop names on site
        for names in offer_card :

                name=names.find('a',class_='link js_product-offer-link').get_text()
                name=name[10:16].replace('\n','')
                names_list.append(name)

### creating list of all prices on site
        for offer in price_card :

                zloty= offer.find('span', class_='value').get_text()
                zloty=zloty.replace(' ', '')

                gr=offer.find('span', class_='penny').get_text()
                gr=gr.replace(',', '')

                price = zloty + '.' + gr
                price_float=float(price)

                price_list.append(price_float)


        zip_lists=zip(names_list, price_list)
        dict_lists=dict(zip_lists)
        return dict_lists


### function which will check actual values from ceneo and return the list of dictionaries with data
def get_actual_values():
        actual_values_list=[]
        for url in product_list.values():
                dict_of_product=get_values(url)
                list_of_tuples=list(dict_of_product.items())
                actual_values_list.append(list_of_tuples)

        return actual_values_list

### function which will get a data from db
def get_db_values():
        db_values_list=[]

        for table in product_list.keys():
                        cursor.execute("SELECT * FROM {}".format(table))
                        db=cursor.fetchall()
                        db_values_list.append(db)



        return db_values_list


def get_data(list):
        i=0
        data_dict={}
        products = list(product_list.keys())


        for product in products :

                data_dict[product]= list[i]
                i+=1

        return data_dict


### check if someone is cheaper than your shop and then check if there is same value in db, then return list of new cheaper offers
def compare_data():
        db_data=get_data(get_db_values())
        actual_data=get_data(get_actual_values())
        our_shop=[]
        offer_list=[]
        offer_list1 = []
        lower_prices=[]
        lower_prices_=[]

        for key , value in actual_data.items():
                for element in value :
                        key_tuple=(key,)
                        offer =  list(element + key_tuple)
                        offer_list.append(offer)

                        #offer[0] must be equal to your shop name

                        if offer[0] =='faxtel' :
                                our_shop.append(offer)


        for faxtel in our_shop :
                for offer in offer_list :

                        if faxtel[2]== offer[2] and faxtel[1] > offer[1] :
                                lower_prices.append(offer)
                                lower_prices_.append(offer)



        for key1 , value1 in db_data.items() :
                for element1 in value1:
                        key_tuple1 = (key1,)
                        offer1 = list(element1 + key_tuple1)
                        offer_list1.append(offer1)


        for actprices in lower_prices :
                for dbprices in offer_list1 :
                        if actprices == dbprices :
                                lower_prices_.remove(actprices)

                                break

        return lower_prices_, our_shop
