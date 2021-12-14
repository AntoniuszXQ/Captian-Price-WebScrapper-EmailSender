from bs4 import BeautifulSoup
import requests
import sqlite3

header={'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 OPR/80.0.4170.91'}




connection = sqlite3.connect('prices.db')
cursor = connection.cursor()


### here you add products you want to check {product name : product url}
productList = {'Multipic35': 87856739 , 'Multipic24': 78944802, 'Multipic51': 111580327}


### function which will retrun prices and shop names in dictionary
def GetValues(Url):
        global productName , priceList , nameList
        html = requests.get('https://ceneo.pl/{}'.format(Url),headers=header).text
        soup = BeautifulSoup(html,'lxml')
        priceCard = soup.find_all('a',class_='product-price go-to-shop')
        offerCard = soup.find_all('div',class_='product-offer__details__toolbar')
        offerName = soup.find('div',class_='product-top__title')
        productName=offerName.find('h1').get_text()
        priceList = []
        namesList=[]


### Creating a list of shop names on site
        for names in offerCard :

                name=names.find('a',class_='link js_product-offer-link').get_text()
                name=name[10:16].replace('\n','')
                namesList.append(name)

### creating list of all prices on site
        for offer in priceCard :

                zlotowki= offer.find('span',class_='value').get_text()
                zlotowki=zlotowki.replace(' ','')

                grosze=offer.find('span',class_='penny').get_text()
                grosze=grosze.replace(',','')

                cena = zlotowki+'.'+ grosze
                cenaFloat=float(cena)

                priceList.append(cenaFloat)


        zipLists=zip(namesList,priceList)
        dictLists=dict(zipLists)
        return dictLists


### function which will check actual values from ceneo and return the list of dictionaries with data
def GetActualValues():
        ActualValuesList=[]
        for url in productList.values():
                dictOfProduct=GetValues(url)
                ListofTuples=list(dictOfProduct.items())
                ActualValuesList.append(ListofTuples)

        return ActualValuesList

### function which will get a data from db
def GetDbValues():
        DbValuesList=[]

        for table in productList.keys():
                        cursor.execute("SELECT * FROM {}".format(table))
                        db=cursor.fetchall()
                        DbValuesList.append(db)



        return DbValuesList


def GetData(lista):
        i=0
        DataDict={}
        products = list(productList.keys())


        for product in products :

                DataDict[product]= lista[i]
                i+=1

        return DataDict


### check if someone is cheaper than your shop and then check if there is same value in db, then return list of new cheaper offers
def Compare_Data():
        db_data=GetData(GetDbValues())
        actual_data=GetData(GetActualValues())
        ourShop=[]
        offerlist=[]
        offerlist1 = []
        lowerprices=[]
        lowerprices_=[]

        for key , value in actual_data.items():
                for element in value :
                        keyTuple=(key,)
                        offer =  list(element + keyTuple)
                        offerlist.append(offer)

                        #offer[0] must be equal to your shop name

                        if offer[0] =='faxtel' :
                                ourShop.append(offer)


        for faxtel in ourShop :
                for offer in offerlist :

                        if faxtel[2]== offer[2] and faxtel[1] > offer[1] :
                                lowerprices.append(offer)
                                lowerprices_.append(offer)



        for key1 , value1 in db_data.items() :
                for element1 in value1:
                        keyTuple1 = (key1,)
                        offer1 = list(element1 + keyTuple1)
                        offerlist1.append(offer1)


        for actprices in lowerprices :
                for dbprices in offerlist1 :
                        if actprices == dbprices :
                                lowerprices_.remove(actprices)

                                break

        return lowerprices_, ourShop
