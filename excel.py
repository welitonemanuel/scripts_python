import os
from datetime import date, time, datetime, timedelta
import pandas as pd
import openpyxl
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.worksheet.table import Table, TableStyleInfo

from openpyxl.styles import NamedStyle
# from openpyxl.styles import PatternFill, Font
# from openpyxl.worksheet.table import Table #, TableStyleInfo
#import IPython.display as ipy
# =============================================================================
# Funções
# =============================================================================
# =============================================================================
# LER CSV
# =============================================================================

def read_csv(file_name, log):
    if file_name == 'reportStatusCutMeter':
        #path = "C:\\Users\\u461539\\OneDrive - IBERDROLA S.A\\005.Scripts\\wsmc\\INPUT\\"
        path = ".\input\\"
        desconhecido = True
        for diretorio, subpastas, arquivos in os.walk(path):
            arquivos = sorted(arquivos, key=lambda x: os.path.getmtime(os.path.join(diretorio, x)), reverse=True)
            for arquivo in arquivos:
                if (arquivo[0:20] == file_name and desconhecido):
                    data_hora_str = arquivo.split('_')[1] + '_' + arquivo.split('_')[2].split('.')[0]   # Extrair a informação de data e hora do sufixo do arquivo
                    data_hora = datetime.strptime(data_hora_str, '%Y%m%d_%H%M%S')   # Converter a string para datetime
                    desconhecido = False
                    tabela = pd.read_csv(path + arquivo,sep=";", encoding='iso-8859-1', skiprows=2,names=["uc", "em",
                            "regiao", "agrupamento", "cs", "posicao", "tecnologia", "dt_ult_leitura","leitura_kwh",
                            "status_rele"])
                    tabela = tabela.replace({'\'': ''}, regex=True)  # retirar as aspas simples
                    tabela = tabela.astype({'em': 'string'})
                    tabela = tabela.astype({'agrupamento': 'string'})
                    tabela = tabela.astype({'cs': 'string'})
                    tabela = tabela.astype({'posicao': 'int'})
                    tabela = tabela.astype({'dt_ult_leitura': 'string'})
                    tabela = tabela.astype({'leitura_kwh': 'string'})
                    tabela = tabela.astype({'status_rele': 'string'})
                    if log:
                        print(f'Arquivo \'{arquivo}\' importado.')
#                 elif arquivo[0:20] == 'reportStatusCutMeter':
#                     os.remove(path + arquivo)
                    #print(f"O arquivo \'{arquivo}\' foi deletado com sucesso.")
                # else:
                    #print(f"O arquivo \'{arquivo}\' não é o alvo.")
        # Verificação se o arquivo foi encontrado
        try:
            dados = {"dt_update": data_hora, "tabela": tabela}      # Criar o dicionário com as informações desejadas
        except:
            raise FileNotFoundError("Arquivo 'reportStatusCutMeter' não encontrado.")
        return dados
    if file_name == 'ga_cliente':
        print('em construcao')


# # =============================================================================
# # ESCREVER EXCEL
# # =============================================================================
#
# def format_excel(file_name: str, redimensionar_colunas: bool = False):
#
#     # # Exportar o DataFrame para arquivo Excel
#     df = pd.read_excel(file_name, engine='openpyxl') #, sheet_name='Sheet')
#     # Converter a coluna 'N' para valores de data no Python
#     df['DT_ATIVO_AGRUPAMENTO'] = pd.to_datetime(df['DT_ATIVO_AGRUPAMENTO'], errors='ignore')  # 'coerce' trata valores inválidos como NaT
#     df['DT_CRIA'] = pd.to_datetime(df['DT_CRIA'], errors='ignore')  # 'coerce' trata valores inválidos como NaT
#
#     # # Criar um novo arquivo Excel
#     workbook = Workbook()
#     sheet = workbook.active
#     sheet.name = 'T'
#
#     # Preencher a planilha com os dados do DataFrame
#     for row in dataframe_to_rows(df, index=False, header=True):
#         sheet.append(row)
#
#     # Definir um formato de data personalizado
#     date_format = 'DD/MM/YYYY'
#
#     # Aplicar o formato de data
#     column_x = sheet['N']   # coluna 'N'  - dt_cria
#     for cell in column_x[1:]:  # Começar da segunda célula para evitar o cabeçalho
#         cell.number_format = date_format
#
#     column_x = sheet['O']   # coluna 'O'  - dt_deslig
#     for cell in column_x[1:]:  # Começar da segunda célula para evitar o cabeçalho
#         cell.number_format = date_format
#
#     # Criar a tabela
#     table = Table(displayName="Tabela1", ref=f"A1:{chr(ord('A') + len(df.columns) - 1)}{len(df) + 1}")
#     style = TableStyleInfo(name="TableStyleMedium2", showFirstColumn=False, showLastColumn=False,
#                            showRowStripes=True, showColumnStripes=False)
#     table.tableStyleInfo = style
#
#     # Adicionar a tabela à planilha
#     sheet.add_table(table)
#
#     # Redimensionar as colunas
#     if redimensionar_colunas:
#         for column in sheet.columns:
#             max_length = 0
#             column = [cell for cell in column]
#             for cell in column:
#                 try:
#                     if len(str(cell.value)) > max_length:
#                         max_length = len(cell.value)
#                 except:
#                     pass
#
#             adjusted_width = (max_length + 2) * 1.2
#
#             sheet.column_dimensions[column[0].column_letter].width = adjusted_width
#
#     # Salvar o arquivo Excel
#     workbook.save(file_name)

# =============================================================================
# DEBUG
# =============================================================================
if __name__ == "__main__":
    pass
