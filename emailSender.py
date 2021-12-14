import smtplib
from Scrapper import Compare_Data, productList
import schedule



def generate_message():
    lower_prices=Compare_Data()[0]
    all_products=productList.keys()
    productslower=[]

    header=[]
    message=[]
    mess=''



    for prod in lower_prices :
        productslower.append(prod[2])
    prdset=set(productslower)
    uniqproduct=list(prdset)


    for product in all_products :

            if uniqproduct.count(product) > 0  :

               mess += '\n' + product + ' Przebity' + '\n' + '\n'

               for offer in lower_prices :
                    if offer[2]==product:
                         message.append('* ' + offer[0] + ' - ' + str(offer[1]))
                         mess+= '* ' + offer[0] + ' - ' + str(offer[1]) + '\n'

            else :

                header.append(product + ' NIE Przebity')
                mess+= '\n' + product + ' NIE Przebity' + '\n' + '\n'



    return mess




def send_email():

# here you can add your email with you want to send from
    sender_email = ""
    mailSubject = 'XXXX CENY XXXX'
    message = f'Subject: {mailSubject}\n\n{generate_message()}'

# here is the email adress with should recive message
    rec_email = ""


# here you need to input your email password
    password = ''

    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.starttls()
    server.login(sender_email, password)


    server.sendmail(sender_email, rec_email, message)
    print('Email send')







### here you can plan when to use your program and send an email with cheaper offers
### you need to also plan DB updates in DBsetup modules

schedule.every().day.at("12:30").do(send_email)
schedule.every().day.at("15:30").do(send_email)
schedule.every().day.at("17:00").do(send_email)
schedule.every().day.at("18:00").do(send_email)
schedule.every().day.at("22:00").do(send_email)


while True :
    schedule.run_pending()

