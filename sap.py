# =============================================================================
# Biblioteca
# =============================================================================
import time     # Facilita desenvolvimento envolvendo tempo, tempo de espera, etc
import pandas as pd
from datetime import datetime
import winshell
from pywinauto import Desktop, Application
import win32com.client
import subprocess
import sys
sys.path.insert(1, '../../wfuncoes py')
import keys as k
from tqdm import tqdm # barra de progresso
import os

# pip install tqdm --proxy=http://array
# pip uninstall logging
# =============================================================================
# Variáveis Locais
# =============================================================================
segundos_login = 60
segundos_open = 10
segundos_table = 300
# =============================================================================
# Classe
# =============================================================================
class Sap:
    """
    Estrutura dos dados do SAP
        Args:
            log: Se quer a saída de log
    Etapas:
    1. Extrair
        1.1 DADOS EM do HANA
        1.2 DADOS EM do CCS
        1.3 INST_EM do CCS
        1.4 DT_DESLIG do CCS    -   EVER: Atualização da Base SAP: Instalação / CC / Data de deslig def
        1.5 UPDATE TB_EQUI com novos medidores
    2. Carregar
    """
    def __init__(self, log: bool = False):
        self._log = log
        self._tb = pd.DataFrame()
        self._dt_update = datetime(year=1, month=1, day=1, hour=0, minute=0, second=0)

    def __str__(self):
        return f"sap.dt_update: {self.dt_update}\nsap.tb: {self.tb.shape[0]} rows x {self.tb.shape[1]} columns"

# # =============================================================================
# # 1.01 Login SAP CCS
# # =============================================================================

    def aux_equi_insert(self,df_em=None):
        """
        Automação de acessar SAP CCS, baixar dados dos medidores e salvar em aux_equi
        Sub etapas:
        1.01 Acessar o SAP CCS
        1.02 IQ09 /WLEITE: EM -> EQUI_LOG
        """
        if df_em is None: #buscar tb_equi no HANA
            raise FileNotFoundError("Dataframe em branco.")

        # ccs_login(k.user_rede_clb,k.pass_rede)
        ccs_transacao('IQ09', 'SAP Easy Access  -  Menu usuário p/ WELITON EMANUEL SANT ANA L - \\Remote') # todo continuar

        # df_tb = ccs_extrair('equi',df_em,)
            # login_sap(transacao = 'SE16N', titulo_transacao = 'Exibição geral de tabela')
        # df_SMC = extract_SMC(df)
        # df_SMC.to_excel('C:/Users/U470167/IBERDROLA S.A/Automacao - Documentos/Rotinas_Python/Teste_Robo_SMC/Extracao_SMC.xlsx', sheet_name='Planilha1', index=False)
        print('')

    # def em_to_instalacao(self, usuario: str, senha: str, df: object):
        """
        Automação de acessar SAP CCS, baixar INSTALAÇÃO a partir do EM e salvar em tb_sap no HANA
        Sub etapas:
        1.01 Acessar o SAP CCS
        1.02 IQ09 /WLEITE: EM -> EQUI_LOG
        1.03 ETDZ wel_smc2: EQUI_LOG -> REG_LOG
        1.04 EASTS wel_smc3: REG_LOG -> INST
        Etapas abaixo, query do SAP HANA
        1.05 EANL wel_blin1: INST -> LOC.CONSUMO
            1.05.01 Tabela Nível de tensão
            1.05.02 Tabela Tipo de Instalação
        1.06 EVBS wel_blin2: LOC.CONSUMO -> POSTE, POSTO, TIPO MEDIÇÃO
        """
# =============================================================================
# Funções
# =============================================================================
def ccs_login(usuario, senha):
    # Verificar e fechar SAP Logon/Citrix em aberto
    # todo Ver se tem janela do SAP ABERTA. Se sim, derrubar sessoes do sap aberto! manter SAP LOGON
    # Abrir SAP pelo Citrix
    atalho = r"C:\Users\u461539\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Iberdrola Apps\Neoenergia Apps PROD\SAP Logon Virtual.lnk"
    destino = winshell.shortcut(atalho).path
    argumentos = ["-launch", "-reg",
                  r'"Software\Microsoft\Windows\CurrentVersion\Uninstall\neoenergia-ae963f53@@XD02.ASF FPM DEV SAP_s-2"',
                  "-startmenuShortcut"]
    arg_str = " ".join(argumentos)
    subprocess.Popen(f'"{destino}" {arg_str}',shell=True)
    [titulo, nome_classe] = ccs_open_window('SAP Logon 770',segundos_login)

    # Selecionar CCS 05.04  #todo tirar mensagem de alertar
    app = Application().connect(title=titulo,class_name=nome_classe)    # FUNCIONA embora exiba UserWarning 32 bits
    window = app.window(title=titulo)
    window.type_keys('05.04{ENTER}')
    [titulo, nome_classe] = ccs_open_window('SAP - ', segundos_open)

    # Inserir usuário e senha
    app = Application().connect(title=titulo,class_name=nome_classe)
    window = app.window(title=titulo)
    window.type_keys(usuario+'{TAB}'+senha+'{ENTER}')
    [titulo, nome_classe] = ccs_open_window('SAP Easy Access  -  Menu usuário', segundos_open)

    print(" ", end='\n')
    print('Conectado ao SAP CCS', end='\n')
    # # Listar os títulos das janelas ativas
    # for window in Desktop().windows():    print(window.window_text())
    # Imprimir as informações de identificação, incluindo class_name
    # app = Desktop().window(title=r'SAP Logon 770 - \\Remote')
    # app.print_control_identifiers()

def ccs_open_window(title: str, seconds_to_break: int):
    '''Aguardar a janela ficar ativa para continuar'''
    desktop = Desktop()
    sap_window = None
    windows = None
    print(" ", end='\n')
    i = 0
    time.sleep(2)
    for i in tqdm(range(seconds_to_break), desc = 'Open '+title): #, leave = False): apaga a barra após terminar!
        if sap_window != None:  # sap_window.maximize() # Não funciona
            break
        try:
            windows = desktop.windows()
        except:
            pass
        for window in windows:
            if window.window_text().startswith(title):
                    sap_window = window
                    break
        time.sleep(1)
    if sap_window != None:
        time.sleep(2)
        return [sap_window.window_text(), sap_window.class_name()]
    else:
        print(" ", end='\n')
        print('Error: Time out!', end='\n')
        exit()

def ccs_transacao(transacao: str, titulo_transacao: str):
    # # Transação IQ09
    # todo continuar

    # SapGuiAuto = win32com.client.GetObject(Class='Transparent Windows Client')
    SapGuiAuto = win32com.client.GetObject('SAPGUI')
    if not type(SapGuiAuto) == win32com.client.CDispatch:
        return
    application = SapGuiAuto.GetScriptingEngine
    if not type(application) == win32com.client.CDispatch:
        SapGuiAuto = None
        return
    connection = application.Children(0)
    session = connection.Children(0)
    if not type(session) == win32com.client.CDispatch:
        connection = None
        application = None
        SapGuiAuto = None
        return

    print("")

    # Método alternativo que funciona
    # app = Application().connect(title=titulo,class_name=nome_classe)
    # window = app.window(title=titulo)
    # window.type_keys(usuario+'{TAB}'+senha+'{ENTER}')
    # [titulo, nome_classe] = ccs_open_window('SAP Easy Access  -  Menu usuário', segundos_open)


    #Acessar O SAP 5.04

# =============================================================================
# DEBUG
# =============================================================================
if __name__ == "__main__":
    df = [1140365021,1140402504,1150143035,1150153723,1150156110,1192420683,1192420799]
    s1 = Sap(True)
    # print(s1)
    s1.aux_equi_insert(df)
    # s1.extrair_ccs_instalacao(k.user_rede_clb,k.pass_rede,df)

    # 1. Medidor
    # Tabela V_EQUI
    #     1.1 Extrair do SAP
    #         1.1.a Medidores exclusivos SMC fora da base
    #         1.1.b Medidores do Hemera fora da base
    #     1.2 Transformadas
    #         Exportar (tb_sap_equipamento)
    # 2. Status Ligacao
    # Tabela EVER / WSMC
    #     2.1 Extrair do SAP
    #     2.2 Transformada
    #         Substituir "5 espaços" por (vazio)
    #         Substituir 31/12/9999 por (vazio)
    #         Classificar por INSTALAÇÃO, DT_DD desc, DT_CRIACAO desc, CC desc (na_position='first')
    #         Excluir Duplicados: INSTALAÇÃO
    #         Exportar
    # 3. Instalacao
    # Tabela ETDZ - EASTS - EANL - EVBS
    # Base SAP: Instalação / Medidor (par conjugado)
    #     3.1 Extrair do SAP
    #         3.1.a Hemera: Add Base Cliente a partir da base medidor Hemera
    #         3.1.b Medidor: Add Base Cliente a partir da base medidor
    #         3.1.c MRU: Add Base Cliente a partir da MRU R
    #         3.1.d Cliente: Extrair a partir da base cliente
    #     3.3 Transformada
    #         Análise dos medidores não telemedidos
    #         Realocações MRU
    #         Exportar
    #  3. Load


# Nív.tensão	TENSÃO
# 10	1x127 V
# 11	1x220 V
# 12	1x6900 V
# 13	1x7900 V
# 14	1x8050 V
# 15	1x19900 V
# 20	2x254/127 V
# 21	2x440/220 V
# 22	2x220/127 V
# 23	2x380/220 V
# 30	3x220/127 V
# 31	3x380/220 V
# 32	3x460/277 V
# 40	11500 V
# 41	11900 V
# 42	13800 V
# 43	34500 V
# 44	69000 V
# 45	138000 V
# 46	230000 V

# TpIns	TIPO INSTALAÇÃO
# CO	Comércio
# CP	Consumo Próprio
# EV	Ligação Eventual
# IN	Indústria
# IP	Iluminação Pública
# LP	Ligação Provisória
# OB	Obras
# OS	Obras SEINFRA
# PP	Poder Público
# PS	Prestação de Serviço
# RD	Residência
# RU	Rural
# SC	Serviço Comum Condomínio
# SF	Semáforo / Fotosensores
# SP	Serviço Público