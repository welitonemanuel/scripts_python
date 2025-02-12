# =============================================================================
# BAU PY
# =============================================================================

# CONVERTER CSV EM EXCEL
df_out = pd.read_csv('temp.csv',sep=';'
                      ,names = ['instalacao','inst_dt_ligacao','inst_dt_deslig','medidor','med_dt_desde','med_dt_ate','cc','med_material','med_equi_log']
                      ,dtype = {'instalacao': 'int64','inst_dt_ligacao': 'str','inst_dt_deslig': 'str','medidor': 'int64','med_dt_desde': 'str','med_dt_ate': 'str','cc': 'int64','med_material': 'int64','med_equi_log': 'str'}
                      ,parse_dates = ['inst_dt_ligacao','inst_dt_deslig','med_dt_desde','med_dt_ate']
                      ,engine = 'python'
                      )
writer = pd.ExcelWriter(
    "sap_clientes.xlsx",
    engine='xlsxwriter',
    datetime_format="dd/mm/yyyy",
    date_format="dd/mm/yyyy"
)
df_out.to_excel(writer, sheet_name='Planilha1', index=False)
writer.close()

# Outra forma de alterar formatação excel
workbook  = writer.book
worksheet = writer.sheets['Planilha1']
format = workbook.add_format({'num_format': 'dd/mm/yy'})
worksheet.set_column('B:B', 18, format)
writer.save()

# converter inteiro para string
def convert_to_str(x):
    try:
        y = str(int(x))
        return y
    except ValueError:
        return x
    df_serie['Serie'] = df_serie['Serie'].apply(lambda x: convert_to_str(x))
    df_serie['Serie'] = df_serie['Serie'].apply(lambda x: str(int(x)))


#import pyautogui
# Controle de teclado, mouse e tela
# pyautogui.click -> clique com o mouse
# pyautogui.write -> escrever um texto
# pyautogui.press -> apertar uma tecla
# pyautogui.hotkey -> apertar uma combinação de teclas (ex: Ctrl + D)


    # format_excel(r".wsmc\db\tb_rede.xlsx")
    # format_excel(r"C:\Users\u461539\OneDrive - IBERDROLA S.A\005.Scripts\wsmc\db\tb_rede.xlsx", True)
    # resultado = read_csv('reportStatusCutMeter')
    # print(f"A dt_update é {list(resultado.items())[0][1].strftime('%d/%m/%Y %H:%M:%S')}.")

# =============================================================================
# MARKDOWN - LABEL NO JUPYTER
# =============================================================================

# Função md - Markdown
# def md(texto, cor= 'black'):
#     estilo = f"color: {cor};"
#     display(Markdown(f"<span style='{estilo}'>{texto}</span>"))

# class label:
#     def __init__(self, texto: str, cor: str = 'black',tamanho: str = '10px', cor_fundo: str = ''):
#         self.texto = texto
#         self.cor = cor
#         self.tamanho = tamanho
#         self.cor_fundo = cor_fundo
#         self.estilo = f"color: {self.cor};"
    
#     def __str__(texto, cor='black', tamanho=None, cor_fundo=None):

#         if self.tamanho:
#             self.estilo += f"font-size: {self.tamanho};"
#         if self.cor_fundo:
#             self.estilo += f"background-color: {cor_fundo};"
#         return ipw.HTML(f"<span style='{self.estilo}'>{self.texto}</span>")
        
#função OK
# def md(texto, cor='black', tamanho=None, cor_fundo=None):
#     estilo = f"color: {cor};"
#     if tamanho:
#         estilo += f"font-size: {tamanho};"
#     if cor_fundo:
#         estilo += f"background-color: {cor_fundo};"
#     return display(ipw.HTML(f"<span style='{estilo}'>{texto}</span>"))

# def md(texto, cor='black', tamanho=None, cor_fundo=None, modo=None):
#     estilo = f"color: {cor};"
#     if tamanho:
#         estilo += f"font-size: {tamanho};"
#     if cor_fundo:
#         estilo += f"background-color: {cor_fundo};"
#     if modo == 'display':
#         return display(Markdown(f"<span style='{estilo}'>{texto}</span>"))
#     elif modo == 'Box':
# #         return ipw.HTML(f"<span style='{estilo}'>{texto}</span>")
#         return ipw.HBox([ipw.HTML(str(Markdown(f"<span style='{estilo}'>{texto}</span>")))])
#     elif modo == 'Markdown':
#         return Markdown(f"<span style='{estilo}'>{texto}</span>")
#     else:
#         raise ValueError("Modo inválido. Escolha entre 'display', 'Box' ou 'Markdown'.")

# lbl_hemera_load = md('Hemera carregado:', cor='gray',cor_fundo='lightgreen',tamanho=20, modo='Box')


        # =============================================================================
        # 2.10 Exportar hemera.expurgo (Excel) e hemera.tb (pickle)
        #      Renomear hemera_2023 + DATA + .xlsx
        #      Exportar hemera_csv
        # =============================================================================
        
        # Exportar hemera (excel) - muito pesado
        rscm7.to_excel(r".\output\hemera.xlsx",sheet_name=dt_update.strftime('%Y-%m-%d_%H_%M_%S'),index=False)
        
        if self._log:
            print('exportado hemera.xlsx')
        
        # Formatação hemera (excel) - muito pesado
        wf.format_excel(r".\output\hemera.xlsx", True)
        
        if self._log:
            print('formatado hemera.xlsx')

        # Excluir rscm_2023.csv
        path = ".\output\\"
        desconhecido = True
        for diretorio, subpastas, arquivos in os.walk(path):
            for arquivo in arquivos:
                if ((arquivo[0:4] == 'rscm') & (arquivo[-4:] == '.csv') & desconhecido):
                    os.remove(path + arquivo)
                    #os.rename(path+arquivo,path+'rscm_'+dt_update.strftime('%Y-%m-%d_%Hh%Mm%Ss')+'.xlsx')
                    desconhecido = False
                    if self._log:
                        print(f"O arquivo \'{arquivo}\' foi excluído.")
        # Verificação se o arquivo foi encontrado
        if desconhecido:
            print("Arquivo 'rscm_2023*.csv' não encontrado.")
            # raise FileNotFoundError("Arquivo 'hemera.xlsx' não encontrado.")


## Abrindo e escrevendo arquivos CSV:
#Para ler arquivos CSV codificados em ISO
>>> pd.read_csv('nome_do_arquivo.csv', encoding='ISO-8859-1')

                # agr_novo = pd.DataFrame(rede.loc[rede['net'] == net_rscm.loc[row['index']]['net']])

            # if cell.column in [19, 20]:
            #     adjusted_width = (max_length + 6) * 1.2
            # else:
            #     adjusted_width = (max_length + 2) * 1.2                


#bau hemera.py
        # Convertendo as datas para o formato desejado; converte 31/12/9999 em NAT
        rede['dt_deslig'] = pd.to_datetime(rede['dt_deslig'], format='%Y-%m-%d %H:%M:%S', errors='coerce')  # 'coerce' trata valores inválidos como NaT
        rede['dt_deslig'] = rede['dt_deslig'].dt.strftime('%d/%m/%Y')
        rede['dt_cria'] = pd.to_datetime(rede['dt_cria'], format='%Y-%m-%d %H:%M:%S', errors='coerce')  # 'coerce' trata valores inválidos como NaT
        rede['dt_cria'] = rede['dt_cria'].dt.strftime('%d/%m/%Y')

        # Classificação de acordo com a net e net_desativada
        rede = rede.sort_values(by=['net', 'dt_deslig'], ascending=[True, False], na_position='first')

        agr_novo = ~net_rscm['agrupamento'].isin(rede['agrupamento'])
        net_novo = ~net_rscm['net'].isin(rede['net'])
        novos = pd.DataFrame({'agrupamento': agr_novo, 'net': net_novo})
        novos = novos[novos['agrupamento']].reset_index()  # Filtrar todas as linhas com valor False em ambas as colunas

        # sub etapa 3
        for index, row in novos.iterrows():  # interação sobre dataframe
            if row['net']:  # net nova
                print('Nova rede: ' + net_rscm.iloc[row['index']]['agrupamento'])
                net_nova = pd.DataFrame(net_rscm.iloc[row['index']]).copy().transpose()  # copiar nova net
                net_nova = net_nova.assign(
                    dt_deslig= None,
                    dt_cria=datetime.now().date(),
                    construtor='#TODO',
                    referencia='#TODO',
                    trafo='#TODO',
                    poste='#TODO')
                rede = pd.concat([rede, net_nova])  # adicionar a nova linha
            else:  # net existente; alteração de agrupamento
                print('Agrupamento atualizado: ' + net_rscm.iloc[row['index']]['agrupamento'])
                condition = ((rede['net'] == net_rscm.loc[row['index'], 'net']) & (rede['dt_deslig'].isna())) # seleção da linha do agrupamento da rede ativa;
                agr_novo = rede.loc[condition].copy()
                agr_novo['agrupamento'] = net_rscm.iloc[row['index']]['agrupamento']        # Atualização do agrupamento
                rede.loc[condition, 'dt_deslig'] = datetime.now().date()                   # Alterar net_desativada de nulo para hoje
                rede = pd.concat([rede, agr_novo])  # Armazenamento da nova rede

        # Classificação de acordo com a net e net_desativada
        rede = rede.sort_values(by=['net', 'dt_deslig','dt_cria'], ascending=[True, False,False], na_position='first')

        # check - Setar somente uma rede ativa (net_desativada nulo)
        duplicates = rede[rede.duplicated(subset='net', keep='first') & rede['dt_deslig'].isnull()]    # Encontrar as duplicatas com base na coluna 'net'
        rede.loc[duplicates.index, 'dt_deslig'] = datetime.now().date()        # Atualizar a coluna 'net_desativada' para as duplicatas filtradas

        #retornar para dt_deslig NAT para 31/12/9999
        rede['dt_deslig'].fillna('9999-12-31', inplace=True)

        # Substituir valores em branco em 'dt_deslig' por '31/12/9999'
        rede['dt_deslig'].replace('', '31/12/9999', inplace=True)



#     print(df.shape)     # dimensão (29434, 8)
    #     print(df.head)      # 5 primeiras linhas
    #     print(df.info())    # colunas com quantidade e tipo
    #     print(df.keys())    # Index(['net', 'cs', 'posicao', 'em', 'dt_ult_leitura', 'leitura_kwh','status_rele', 'agrupamento'],dtype='object')

=============================
# bay sap.py
#bau da criação da classe sap
=============================
    
    # # dados abortados
    # desktop = Desktop()
    # windows = desktop.windows()
    #
    # # Procurar a janela 'SAP Logon 770'
    # time.sleep(2)
    # sap_window = None
    # for window in windows:
    #     if window.window_text().startswith('SAP Logon 770'):
    #         sap_window = window
    #
    # # Janela encontrada
    # if sap_window:
    #     sap_window.maximize()
    #
    #     sap_window.set_focus()
    #
# SapGuiAuto = win32com.client.GetObject('SAPGUI')
# if not type(SapGuiAuto) == win32com.client.CDispatch:
#     return
# application = SapGuiAuto.GetScriptingEngine
# if not type(application) == win32com.client.CDispatch:
#     SapGuiAuto = None
#     return
# connection = application.Children(0)
# session = connection.Children(0)
# if not type(session) == win32com.client.CDispatch:
#     connection = None
#     application = None
#     SapGuiAuto = None
#     return
# pg.keyDown
# time.sleep(0.5)
# pg.keyDown
# janela.activate()



    #
    # # Verificar se janela está aberta
    # start = time.time()
    # i = 0
    # while True:
    #     win_sap = gw.getWindowsWithTitle('SAP Logon 770')
    #     if len(win_sap) == 1:
    #         print('SAP Logon aberto')
    #         break
    #     else:
    #         i += 2
    #         print(i)
    #         time.sleep(2)
    #
    #     if time.time() - start > 60:
    #         print('Erro: SAP Logon não abre após 60 segundos.')
    #         exit()
    #         break


    # descartado
    # janelas = gw.getWindowsWithTitle('SAP Logon 770')
    #     janela = janelas[0]





    =============================
    =============================