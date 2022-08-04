import string
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from pprint import pprint
from time import time
import  pandas as pd


class Azul:

    def __init__(self):
        self.tempo_inicial = time()


    def start(self):
        categorias = self.get_categorias()
        vouchers = self.get_items(categorias)

        return vouchers


    def get_categorias(self):
        print('PEGANDO CATEGORIAS')
        print('_'*50)
        html = urlopen('https://shopping.tudoazul.com/categoria/71954/giftty?sta_nav=hm-parceiro-giftty-9')
        bs = BeautifulSoup(html, 'html.parser')

        dicionario = {}

        # pego todas tags a das categorias
        categorias = bs.find('div', {'class':'widget Categories'}).find_all('a')

        for categoria in categorias:
            lista = []
            try:
                html = urlopen(f"https://shopping.tudoazul.com{categoria.attrs['href']}")
                bs = BeautifulSoup(html, 'html.parser')
                paginas = bs.find('ul', {'class':'pagination'}).find_all('a')
                for pagina in paginas:
                    if pagina.text.strip() != '':
                        lista.append(f"https://shopping.tudoazul.com{pagina.attrs['href']}")
                dicionario[categoria.text.strip()] = lista
            except AttributeError as e:
                dicionario[categoria.text.strip()] = [f"https://shopping.tudoazul.com{categoria.attrs['href']}"]

        return dicionario


    def get_items(self, dict):

        dicionario = {}
        numero_paginas = 0
        for key in dict:
            lista = []

            print('\n', key.upper())
            print('_' * 50)

            for link in dict[key]:
                html = urlopen(link)
                bs = BeautifulSoup(html, 'html.parser')

                itens = bs.find('div', {'class':'layoutContainer'}).find_all('div', {'class':'col max-270 standard'})

                numero_paginas = numero_paginas+1
                print(f'PÁGINAS: {numero_paginas}', f' | MINUTOS: {round((time() - self.tempo_inicial) / 60, 2)}',
                      f' | {round(numero_paginas / 50 * 100, 2)}%')
                for item in itens:
                    #pega nome do item
                    nome = item.find('div', {'class':'title'}).h3.text.replace("'", "")

                    #tratamento de erro caso o item não possua valor em reais
                    if re.findall(r'[0-9,]+$', nome):
                        # pega o valor do item em reais
                        valor_reais = item.find('div', {'class':'title'}).h3.text
                        valor_reais = float(re.findall(r'[0-9,]+$', valor_reais)[0].replace(",", "."))

                        #pega o valor do item em pontos
                        valor_pontos = item.find('div',{'class':'promo-tudoazul-label container-footer'}).text
                        valor_pontos = int(re.findall(r'([0-9\.]+)', valor_pontos)[0].replace('.', ""))

                        #pega link do produto
                        link_produto = item.find('a').attrs['href']

                        milheiro = round(valor_reais/valor_pontos*1000, 2)
                        item_dict = {'nome':nome, 'valor':valor_reais, 'pontos':valor_pontos,
                                      'milheiro':milheiro, 'link':f"https://shopping.tudoazul.com{link_produto}"}

                        lista.append(item_dict)

            dicionario[key] = lista

        return dicionario