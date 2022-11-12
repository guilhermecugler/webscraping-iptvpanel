#   Esse arquivo faz o scrap do painel de iptv, 
#   e gera um arquivo de texto com a url pronta para 
#   enviar mensagem para os clientes que
#   vencem em menos de 2 dias

from http import client
from textwrap import indent
import datetime
from bs4 import BeautifulSoup
import pandas as pd
import json
import requests
import re
from datetime import datetime
from datetime import date
from dotenv import load_dotenv
import os
import ast
import pywhatkit
from env import *
import pywhatkit as py

cookies1 = cookies

url = urlPanel

headers = {
    'authority': url,
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'en-US,en;q=0.9,pt;q=0.8,ja;q=0.7',
    'referer': url,
    'sec-ch-ua': '"Chromium";v="106", "Google Chrome";v="106", "Not;A=Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
}

data = {
    'draw': '3',
    'columns[0][data]': '0',
    'columns[0][name]': '',
    'columns[0][searchable]': 'true',
    'columns[0][orderable]': 'true',
    'columns[0][search][value]': '',
    'columns[0][search][regex]': 'false',
    'columns[1][data]': '1',
    'columns[1][name]': '',
    'columns[1][searchable]': 'true',
    'columns[1][orderable]': 'true',
    'columns[1][search][value]': '',
    'columns[1][search][regex]': 'false',
    'columns[2][data]': '2',
    'columns[2][name]': '',
    'columns[2][searchable]': 'true',
    'columns[2][orderable]': 'true',
    'columns[2][search][value]': '',
    'columns[2][search][regex]': 'false',
    'columns[3][data]': '3',
    'columns[3][name]': '',
    'columns[3][searchable]': 'true',
    'columns[3][orderable]': 'true',
    'columns[3][search][value]': '',
    'columns[3][search][regex]': 'false',
    'columns[4][data]': '4',
    'columns[4][name]': '',
    'columns[4][searchable]': 'true',
    'columns[4][orderable]': 'true',
    'columns[4][search][value]': '',
    'columns[4][search][regex]': 'false',
    'columns[5][data]': '5',
    'columns[5][name]': '',
    'columns[5][searchable]': 'true',
    'columns[5][orderable]': 'true',
    'columns[5][search][value]': '',
    'columns[5][search][regex]': 'false',
    'columns[6][data]': '6',
    'columns[6][name]': '',
    'columns[6][searchable]': 'true',
    'columns[6][orderable]': 'true',
    'columns[6][search][value]': '',
    'columns[6][search][regex]': 'false',
    'columns[7][data]': '7',
    'columns[7][name]': '',
    'columns[7][searchable]': 'true',
    'columns[7][orderable]': 'true',
    'columns[7][search][value]': '',
    'columns[7][search][regex]': 'false',
    'columns[8][data]': '8',
    'columns[8][name]': '',
    'columns[8][searchable]': 'true',
    'columns[8][orderable]': 'true',
    'columns[8][search][value]': '',
    'columns[8][search][regex]': 'false',
    'columns[9][data]': '9',
    'columns[9][name]': '',
    'columns[9][searchable]': 'true',
    'columns[9][orderable]': 'true',
    'columns[9][search][value]': '',
    'columns[9][search][regex]': 'false',
    'order[0][column]': '4',
    'order[0][dir]': 'asc', #ordernar por data
    'start': '0',
    'length': '10', #quantos clientes pesqusar
    'search[value]': '',
    'search[regex]': 'false',
    'filter_value': 'active', #filtrar pora tivo ou hastagh para todos
    'reseller_id': '-1',
}



urlClients = url+'/clients/api/?get_clients'

responseClients = requests.post(urlClients, cookies=cookies1, headers=headers, data=data)

soup = BeautifulSoup(responseClients.content, 'html.parser') 

clientsRaw = re.sub(r"\s+", "", soup.text, flags=re.UNICODE) #remover \n e espaços

clientsJson = json.loads(clientsRaw)

for client in clientsJson['data']: #remove itens do json não necessários
    del client[2]
    del client[2]
    del client[3]
    del client[3]
    del client[3]
    del client[3]
    del client[3]
    del client[3]
    del client[3]
   
    client[2] = client[2][:10] + " " + client[2][10:]
    client[2] = datetime.strptime(client[2], '%d/%m/%Y %H:%M')

    with open('clientes_ativos.json', 'w') as f:
        json.dump(clientsJson, f, indent=2, default=str)

for clientId in clientsJson['data']:
    urlClient = url+'/clients/edit/'+clientId[0]
    responseClient = requests.get(urlClient, cookies=cookies1)
    soupClient = BeautifulSoup(responseClient.content, 'html.parser') 
    telefone = soupClient.find("input", {'name': "phone_number"}).attrs['value']
    expiredate = clientId[2].date()
    delta = expiredate - date.today()
    strexpiredate = clientId[2].strftime("%d/%m/%Y+às+%H:%M")

    if(delta.days <= 2 and telefone!=""):
        urlWA = f"https://web.whatsapp.com/send/?phone=55{telefone}&text=Ol\xe1,+seus+canais+vencem+dia+*{strexpiredate}*&type=phone_number&app_absent=0"
        print(urlWA)
        with open('urlWhatsApp.txt', 'a', encoding='utf-8') as outfile:
            outfile.write(urlWA+"\n")




#print(json.dumps(clientsJson, indent=2))

#whatsapp://send/?phone=55{telefone}&text=Ol\xe1,+seus+canais+vencem+dia+*{strexpiredate}*&type=phone_number&app_absent=0
