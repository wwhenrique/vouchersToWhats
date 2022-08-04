from bs4 import BeautifulSoup
from urllib.request import urlopen
from pprint import pprint
import re
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from urllib.parse import urlparse
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
from time import time
import pandas as pd
from selenium.webdriver.chrome.options import Options



class Dotz:


    def __init__(self):
        self.time_inicio = time()
        self.servico = Service(ChromeDriverManager().install())
        options = Options()
        options.headless = True
        self.navegador = webdriver.Chrome(options=options,service=self.servico)



    def iniciar(self):
        self.logar_no_site()
        dados = self.pegar_vale_compras()
        self.close_selenium()

        return dados


    def logar_no_site(self):

        print('ABRINDO SITE')
        print('-'*50)

        self.navegador.get('https://dotz.com.br')

        print('Aceitando Cookies')

        try:
            self.navegador.find_element(By.ID, 'onetrust-accept-btn-handler').click()
        except NoSuchElementException as e:
            print('Cookie já aceito')


    def verificar_url(self, url):
        print('Verificando URL')
        self.navegador.get(url)
        while url != self.navegador.current_url:
            self.navegador.get(url)
        return True


        return lista_categorias


    def clicar_ver_mais_resultados(self, url):
        print('Clicando em VER MAIS RESULTADOS')
        while True:
            try:
                self.navegador.find_element(By.ID, 'ver-mais-btn').click()
                sleep(1)
            except ElementNotInteractableException as e:
                print('Todos itens liberados')
                break
            except ElementClickInterceptedException as e:
                continue
            except NoSuchElementException as e:
                print('Erro no carregamento da pagina, reiniciando scraper')
                self.iniciar()


    def pegar_vale_compras(self):
        url = 'https://dotz.com.br/Busca/Categoria.aspx?category=591'

        lista_vale_compras = []

        if self.verificar_url(url):
            self.clicar_ver_mais_resultados(url)

            html = self.navegador.page_source
            bs = BeautifulSoup(html, 'html.parser')

            sopa_produtos = bs.find_all('div', {'class':'product-thumb ElasticResult'})

            for produto in sopa_produtos:
                href = produto.find('a', {'class':'product-thumb-elastic'}).attrs['href']
                link = f'https://dotz.com.br{href}'
                nome = produto.find('figcaption').text.strip().replace("'",'')
                pontos = int(re.findall(r'[0-9]+$',
                                    produto.find('div', {'class':'product-thumb-price'}).text.strip().replace('.',''))[0])
                valor = self.handler_preco_voucher(nome)
                milheiro = round((valor/pontos)*1000, 2)
                lista_vale_compras.append({'nome':nome, 'link':link, 'pontos':pontos, 'valor':valor, 'milheiro':milheiro})

        print('\nTempo de execução:',round(time()-self.time_inicio))

        return lista_vale_compras


    def handler_preco_voucher(self, nome):
        palavras = ['SALAS', 'Massagem', 'Nicephotos', 'ClickBus', 'eFootball']

        for palavra in palavras:
            if palavra in nome:
                return 0

        if re.findall(r'[R-r]\$[0-9,\.\s]+', nome):
            reais = re.findall(r'R\$[0-9,\.\s]+', nome)[0]
            reais = float(reais.strip().replace('R$','').replace('r$','').replace('.','').replace(',','.'))
            return reais
        elif re.findall(r'[0-9,\.\s]+$', nome):
            reais = re.findall(r'[0-9,\.\s]+$', nome)[0]
            reais = float(reais.strip().replace('R$','').replace('r$','').replace('.','').replace(',','.'))
            return reais
        else:
            return 0


    def close_selenium(self):
        'Fechando Selenium'
        self.navegador.quit()


