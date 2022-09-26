10                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
# imports
from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# ########################################### web scraping ######################################################

link = "https://???????????"  # base du lien
page = 1
max_pages = 4  # nombre maximum de pages sur le site
df = pd.DataFrame(columns=['offres', 'Lieux', 'Prix (£ ** CC/ mois)', 'lien pages'])
site = 'https://******.'  # lien principal
i = 0

while page <= max_pages:

    html = requests.get(link + f'?page={page}').text

    soup = BeautifulSoup(html, 'lxml')

    for item in soup.find_all('div', class_="ais-hits--item"):

        try:
            title = item.find('div', class_="title").text  # titre de l'offre

            sub_title = item.find('div', class_="sub-title").text  # localistaion

            lien = item.find('div', class_="item")['data-id']  # lien de l'offre

            prix = item.find('div', class_="neuf").span.text + item.find('div', class_="neuf").span.span.text

            df.loc[i] = [title.strip(), sub_title.strip(), prix[:4].strip(),
                         site + f"//location//{lien}" if float(prix[:4].strip()) < 1000 else np.nan]

        except:
            pass

        i += 1
        time.sleep(5)
    page += 1


df_table = df.sort_values(by='Prix (£ ** CC/ mois)', ignore_index=True)[:10]  # table des données suivant les prix
# du plus moins cher au plus cher.


# ################################ Envoie des alertes ##########################################

import smtplib

with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
    MSG = MIMEMultipart()
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()

    subject = ' Ofrres appartements'

    body = f"""
    <html>
    <head>
    </head>
    <body>
    <h2>
    Liste des 10 offres les plus moins chers
    </h2>
    {df_table.to_html()}
    </body>
    </html>"""
    MSG['Subject'] = subject
    MSG['From'] = '___mon_email____@gmail.com'  # email de l'envoyant

    body = MIMEText(body, 'html')

    MSG.attach(body)

    smtp.login('___mon_email____@gmail.com', '_____code_____autorisation___application')  # donner accès au programme
    # accès à notre boite
    # mail . code à récupérer manuellement

    smtp.sendmail('___mon_email____@gmail.com', ['email1', 'email2'], MSG.as_string())  # 'email1', 'email2' ,etc les
    # emails ui doivent recevoir le message

