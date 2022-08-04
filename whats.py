from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from time import sleep
import io
from random import randint
from pathlib import Path

class Whatsapp:
    def __init__(self):
        self.dir = str(Path('teste.py').absolute()).replace('teste.py', '')
        options = Options()
        options.add_argument(fr"--user-data-dir=C:\Users\USERUNAMEUSERNAME\AppData\Local\Google\Chrome\User Data")
        options.add_argument(r'--profile-directory=Profile 2')
        executable = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        self.servico = Service(ChromeDriverManager().install())
        self.navegador = webdriver.Chrome(options = options, service=self.servico)


    def iniciar(self):
        self.logar_no_site()
        self.enviar_mensagens()
        self.fechar()

    def logar_no_site(self):

        print('Acessando site')
        self.navegador.get(f'https://web.whatsapp.com/')

        while True:
            sleep(5)
            try:
                side = self.navegador.find_element(By.ID, 'side')

            except NoSuchElementException as e:
                print('Esperando ler QRCode')
            else:
                print('LOGADO')
                sleep(3)
                break


    def enviar_mensagens(self):

        # clicando no nome do grupo selecionado
        print('Selecionando grupo')
        # ALTERE O TILE PARA O NOME DO SEU GRUPO
        self.navegador.find_element(By.CSS_SELECTOR, "span[title='Teste Python']").click()
        sleep(1)

        try:
            # localiza clip de anexo
            clip = self.navegador.find_element(By.CSS_SELECTOR, "span[data-testid='clip']")
        except (NoSuchElementException, ElementNotInteractableException) as e:
            print('ERRO')
            self.enviar_mensagens()

        clip.click()
        sleep(2)

        print('Anexando arquivo')
        documento = self.navegador.find_element(By.CSS_SELECTOR, 'button[aria-label="Documento"]')
        documento.find_element(By.TAG_NAME, 'input').send_keys(rf'{self.dir}' + 'vouchers.xlsx')
        sleep(3)

        print('clicando em enviar')
        self.navegador.find_element(By.CSS_SELECTOR, 'span[data-testid="send"]').click()

    def fechar(self):
        print('Fechando Selenium em 5 segundos')
        sleep(5)
        self.navegador.close()


if __name__ == '__main__':
    whats = Whatsapp()
    whats.iniciar()