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

    if(x > y):
        print('diminuiu: ')
        variacaoStatus = (f'desvalorização de {((x - y) * 100) / x}%')
        print(((x - y) * 100) / x)        # desconto

    elif(y > x):
        print('aumentou: ')
        variacaoStatus = (f'valorização de {((y - x) * 100) / x}%')
        print(((y - x) * 100) / x)        # aumento
    
    elif(x==y):
        print('sem variacao')
        variacaoStatus = 'variação de 0%'

    return variacaoStatus

def variacaoFinal(x,y):

    if(x > y):
        
        print(f'[PETR4] Variação da ação no dia de {((x - y) * 100) / x}% - valor inicial: R${x} - valor final: R${y}')

        logger.info(f'[PETR4] Variação da ação no dia de {((x - y) * 100) / x}% - valor inicial: R${x} - valor final: R${y}\n')
        

    elif(y > x):
        
        print(f'[PETR4] Variação da ação no dia de {((y - x) * 100) / x}% - valor inicial: R${x} - valor final: R${y}')
        logger.info(f'[PETR4] Variação da ação no dia de {((y - x) * 100) / x}% - valor inicial: R${x} - valor final: R${y}\n')
        
    
    elif(x==y):

        print(f'[PETR4] Variação da ação no dia de 0% - valor inicial: R${x} - valor final: R${y}')
        logger.info(f'[PETR4] Variação da ação no dia de 0% - valor inicial: R${x} - valor final: R${y}\n')
        

    return variacaoStatus    


#schedule.every(5).seconds.do(cotacaopetr4)
#schedule.every(10).minutes.at("10:00").until("13:00").do(cotacaopetr4)

novoCotacao = cotacaopetr4()
cont = 0
primeraCotacao = 0
ultimaCotacao = 0

while True:
   # schedule.run_pending()


    print(novoCotacao)
    

    c_cotacao = cotacaopetr4()

    #variacao(novoCotacao,c_cotacao)

    variacaoStatus = variacao(novoCotacao,c_cotacao)

    print(f'\n [PETR4] Valor atual {c_cotacao}, {variacaoStatus}  \n')

    #logger.info(' [PETR4] Valor atual %.2f, <valorização OU desvalorização> de <porcentagem da variação em relação ao valor anterior>   \n' %(c_cotacao))

    logger.info(f'[PETR4] Valor atual {c_cotacao}, {variacaoStatus}  \n')

    novoCotacao = c_cotacao

    cont = cont + 1

    if (cont == 1): primeraCotacao = c_cotacao

    #LEMBRAR DE MUDAR ESSE IF PARA CADA TESTE

    if (cont == 24): 
        
        ultimaCotacao = c_cotacao

        variacaoFinal(primeraCotacao,ultimaCotacao)



    # o codigo ira executar por 4 horas(14400 segundos), o laço é executado com intervalo de 10 minutos(600 segundos), ou sejá 24 vezes.
    
    if (cont == 24): break
    

   
    time.sleep(10)



#----------CODIGOS QUE POSSAM SER UTEIS-----------------


#blocoInfo = json.loads(response.text)

#print('\n O ip da minha rede é: ' + blocoInfo["ip"] +'\n')

#print('\n Você está conectado em ' + blocoInfo["city"] +  ' no estado de ' +blocoInfo["region"] + '\n')

#headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36' }

#response = requests.get(url, headers=headers)

#response = requests.get(url, headers=headers)

#soup = BeautifulSoup(content, 'html.parser')

#blocoInfo = soup.find('div', attrs={'class': 'home-ip-details'})

#print(blocoInfo["ip"])