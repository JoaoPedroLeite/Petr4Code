#!/usr/bin/env python
import sched
import schedule
import time
import requests
import json
from bs4 import BeautifulSoup
import logging



log_format = '[%(asctime)s] %(message)s'


logging.basicConfig(filename = 'registro.log', filemode = 'w', level = logging.INFO, format = log_format)        #ATENÇÃO: o arquivo será criado na pasta onde o terminal está aberto

logger = logging.getLogger('root')


def cotacaopetr4():

    url = 'https://www.infomoney.com.br/cotacoes/petrobras-petr4/'

    response = requests.get(url)

    content = response.content

    soup = BeautifulSoup(content, 'html.parser')


    valor = soup.find('div', attrs={'class': 'quotes-header-info'})

    numero = valor.find('div', attrs={'class': 'value'})

    cotacao = numero.text[1:6].replace(",",".")           #------------------ERRO: Caso o site não mostre o contação

    c_cotacao = float(cotacao)

    return c_cotacao

def variacao(x,y):

    # x = int(input('x:'))
    # y = int(input('y:'))


    if(x > y):
        print('diminuiu: ')
        print(((x - y) * 100) / x)        # desconto

    elif(y > x):
        print('aumentou: ')
        print(((y - x) * 100) / x)        # aumento
    
    elif(x==y):
        print('sem variacao')

    


#schedule.every(5).seconds.do(cotacaopetr4)
#schedule.every(10).minutes.at("10:00").until("13:00").do(cotacaopetr4)

novoCotacao = cotacaopetr4()

while True:
   # schedule.run_pending()


    print(novoCotacao)
    

    c_cotacao = cotacaopetr4()

    variacao(novoCotacao,c_cotacao)

    print('\n [PETR4] Valor atual %.2f, <valorização OU desvalorização> de <porcentagem da variação em relação ao valor anterior>   \n' %(c_cotacao))

    logger.info(' [PETR4] Valor atual %.2f, <valorização OU desvalorização> de <porcentagem da variação em relação ao valor anterior>   \n' %(c_cotacao))

    novoCotacao = c_cotacao
    

   
    time.sleep(10)


#blocoInfo = json.loads(response.text)

#print('\n O ip da minha rede é: ' + blocoInfo["ip"] +'\n')

#print('\n Você está conectado em ' + blocoInfo["city"] +  ' no estado de ' +blocoInfo["region"] + '\n')



#headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36' }

#response = requests.get(url, headers=headers)

#response = requests.get(url, headers=headers)

#soup = BeautifulSoup(content, 'html.parser')

#blocoInfo = soup.find('div', attrs={'class': 'home-ip-details'})

#print(blocoInfo["ip"])