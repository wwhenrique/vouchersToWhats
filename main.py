from azul import Azul
from dotz import Dotz
import pandas as pd
from whats import Whatsapp


class DataFrame:

    def gerar_arquivo_excel(self, produtos_dotz, produtos_azul):
        print('\n\nGERANDO ARQUIVO EXCEL')
        print('-'*50)

        # tratamento Dotz
        df_dotz = pd.DataFrame(columns=['nome','link','pontos','valor','milheiro'])
        for produto in produtos_dotz:
            df_nova_linha = pd.DataFrame([produto])
            df_dotz = pd.concat([df_dotz, df_nova_linha])

        # tratamento Azul
        df_azul = pd.DataFrame(columns=['nome', 'link', 'pontos', 'valor', 'milheiro'])
        for categoria in produtos_azul.keys():
            for produto in produtos_azul[categoria]:
                df_nova_linha = pd.DataFrame([produto])
                df_azul = pd.concat([df_azul, df_nova_linha])

        # organizado em ordem decrescente do milheiro
        df_dotz = df_dotz.sort_values('milheiro', ascending=False)
        df_azul = df_azul.sort_values('milheiro', ascending=False)

        #cria o documento .xlsx
        writer = pd.ExcelWriter('vouchers.xlsx', engine='xlsxwriter')

        #armazena os dados na planilha
        df_dotz.to_excel(writer, sheet_name='Dotz', index=False)
        df_azul.to_excel(writer, sheet_name='Azul', index=False)

        # salva o arquvio
        writer.save()

        print('Arquivo gerado com sucesso!')


print('EXECUTANDO DOTZ')
print('*'*50)
dotz = Dotz()
vouchers_dotz = dotz.iniciar()

print('\n\nEXECUTANDO AZUL')
print('*'*50)
azul = Azul()
vouchers_azul = azul.start()


print('\n\nGRAVANDO ARQUIVOS EM EXCEL')
print('*'*50)
excel = DataFrame()
excel.gerar_arquivo_excel(vouchers_dotz, vouchers_azul)

print('\n\nENVIANDO DADOS PARA GRUPO DO WHATS')
print('*'*50)
whats = Whatsapp()
whats.iniciar()

quit()