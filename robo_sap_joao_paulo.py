from hdbcli import dbapi
import datetime
import pandas as pd
import win32com.client
from pywinauto import Desktop
#import pywinauto
import os
import time
#import shutil
#from bs4 import BeautifulSoup
from pathlib import Path
import tkinter as tk
#import pyautogui
import openpyxl
from openpyxl import load_workbook



caminho_automacao = os.path.join(Path.home(), "IBERDROLA S.A/Automacao - Documentos/")
os.chdir(caminho_automacao)


senhas = pd.read_csv(os.path.join(Path.home(), "IBERDROLA S.A\Automacao - Documentos\ArquivosAuxiliares\Senhas\senhas_ambientes.csv"), sep=";")

usuario = 'CLB961851'
usuarioccs = usuario
usuariohana = usuario

senha_ccs = senhas['senha_ccs'][senhas['usuario'] == usuario].values[0]
senha_hana = senhas['senha_hana'][senhas['usuario'] == usuario].values[0]
senha_rede = senhas['senha_rede'][senhas['usuario'] == usuario].values[0]


#Conexao
connection = dbapi.connect(
            address='brneo695',
            port='30015',
            user=usuariohana,
            password=senha_hana,
            databasename='BNP',
            sslValidateCertificate=False
        )


cursor = connection.cursor()

def convert_to_str(x):
    try:
        y = str(int(x))
        return y
    except ValueError:
        return x
       

def login_sap(transacao, titulo_transacao):
    ########## SAP #################
    #Se o sap estiver aberto essa parte do código é para derrubar o processo
    if (Desktop(backend='uia').window(title_re="^SAP.*730$",found_index=0).exists()) or (Desktop(backend='uia').window(title_re="^SAP.*740$",found_index=0).exists()) or (Desktop(backend='uia').window(title_re="^SAP.*750$",found_index=0).exists()):
        os.system('taskkill /f /im saplogon.exe')


    #Essa parte do código abre o sap diretamente na transação desejada (nesse caso a SE16N)
    os.system(f"start sapshcut -user={usuarioccs} -pw={senha_ccs} -client=401 -system=BSP -type=Transaction -command={transacao} -title={titulo_transacao}")


    #Essa parte é um teste para saber se o SAP está aberto, ele manda o comando de maximizar até que o comando seja executado.
    while (Desktop(backend='uia').window(title=titulo_transacao,found_index=0).exists()) == False:
            try:
                sap = Desktop(backend='uia').window(title=titulo_transacao, visible_only=False)
                sap.maximize()
            except:
                print('nao achou')
            else:
                print('achou')
                break


##### Origem dos dados:


df_origem = pd.read_excel('C:/Users/U470167/IBERDROLA S.A/Automacao - Documentos/Rotinas_Python/Teste_Robo_SMC/pasta origem/robo_SAP_SMC.xlsx', usecols=range(1, 14), header=1)



#Extração ROBO_SMC
def extract_SMC(df_nt_SMC):

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
   
    #EXTRAÇÃO_NUM_SÉRIE
    df_nt_SMC['Serie'].to_clipboard(excel=True, sep=None, index=False, header=1)
    session.findById("wnd[0]").maximize()
    session.findById("wnd[0]/usr/ctxt[0]").text = "v_equi"
    session.findById("wnd[0]/usr/ctxt[0]").caretPosition = 6
    session.findById("wnd[0]").sendVKey (0)
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").columns.elementAt(5).width = 8
    session.findById("wnd[0]").sendVKey (18)
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,1]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,1]").setFocus()
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 3
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 9
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 12
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 21
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 24
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 27
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 30
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,13]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/btn[4,13]").setFocus()
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/btn[4,13]").press()
    session.findById("wnd[1]/tbar[0]/btn[24]").press()
    session.findById("wnd[1]/tbar[0]/btn[8]").press()
    session.findById("wnd[0]").sendVKey (8)
   
    session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").pressToolbarContextButton ("&MB_EXPORT")
    session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").selectContextMenuItem ("&PC")
    session.findById("wnd[1]/usr/sub/2/sub/2/1/rad[4,0]").select()
    session.findById("wnd[1]/usr/sub/2/sub/2/1/rad[4,0]").setFocus()
    session.findById("wnd[1]/tbar[0]/btn[0]").press()
    session.findById("wnd[0]").sendVKey (12)
   
    #Criar DataFrame N_Série
    df_serie = pd.read_clipboard(sep='|', skiprows=3, skipinitialspace=True)
    df_serie = df_serie.iloc[:,1:3]
    df_serie.columns = ['Serie', 'Equipamento']
    df_serie = df_serie.loc[~df_serie['Serie'].isnull()]
    df_serie['Serie'] = df_serie['Serie'].apply(lambda x: convert_to_str(x))
    df_serie['Serie'] = df_serie['Serie'].apply(lambda x: str(int(x)))


    #EXTRAÇÃO V_EQUI
    df_serie['Equipamento'].to_clipboard(excel=True, sep=None, index=False, header=None)
    session.findById("wnd[0]/usr/ctxt[0]").text = "V_EQUI"
    session.findById("wnd[0]/usr/ctxt[0]").caretPosition = 6
    session.findById("wnd[0]").sendVKey (0)
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 15
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 12
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 0
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").columns.elementAt(5).width = 8
    session.findById("wnd[0]").sendVKey (18)
   
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,1]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,1]").setFocus()
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 3
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,19]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,19]").setFocus()
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 6
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 9
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,17]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,18]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,18]").setFocus()
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 12
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 15
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 18
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 21
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 24
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 27
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,15]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,16]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,16]").setFocus()
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 30
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 33
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 36
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 39
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 42
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 45
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 48
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 51
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 54
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 57
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 60
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 63
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 66
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 72
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 75
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 81
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 84
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 90
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 93
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 96
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 99
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 105
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 111
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,7]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,7]").setFocus()
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 0
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/btn[4,1]").setFocus()
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/btn[4,1]").press()
    session.findById("wnd[1]/tbar[0]/btn[24]").press()
    session.findById("wnd[1]").sendVKey (8)
    session.findById("wnd[0]").sendVKey (8)
   
    session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").pressToolbarContextButton ("&MB_EXPORT")
    session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").selectContextMenuItem ("&PC")
    session.findById("wnd[1]/usr/sub/2/sub/2/1/rad[4,0]").select()
    session.findById("wnd[1]/usr/sub/2/sub/2/1/rad[4,0]").setFocus()
    session.findById("wnd[1]/tbar[0]/btn[0]").press()
    session.findById("wnd[0]/tbar[0]/btn[3]").press() #voltar pra aba principal

    #Criar DataFrame V_EQUI
    df_v_equi = pd.read_clipboard(sep='|', skiprows=3, skipinitialspace=True)
    df_v_equi = df_v_equi.iloc[:,1:8]
    df_v_equi.columns = ['Equipamento', 'Fabricante', 'Modelo', 'AnoC', 'Material', 'Nº série', 'Denominação do objeto técnico']
    df_v_equi = df_v_equi.loc[~df_v_equi['Equipamento'].isnull()]
    df_v_equi['Equipamento'] = df_v_equi['Equipamento'].apply(lambda x: convert_to_str(x))
    df_v_equi['Equipamento'] = df_v_equi['Equipamento'].apply(lambda x: str(int(x)))
   

    #EXTRAÇÃO ETDZ
    df_nt_SMC['Equipamento'].to_clipboard(excel=True, sep=None, index=False, header=None)
    session.findById("wnd[0]").maximize()
    session.findById("wnd[0]/usr/ctxt[0]").text = "etdz"
    session.findById("wnd[0]/usr/ctxt[0]").caretPosition = 4
    session.findById("wnd[0]").sendVKey (0)
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").columns.elementAt(5).width = 8
    session.findById("wnd[0]").sendVKey (18)
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,1]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,5]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/ctxt[2,3]").text = "31.12.9999"
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/btn[4,1]").setFocus()
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/btn[4,1]").press()
    session.findById("wnd[1]/tbar[0]/btn[24]").press()
    session.findById("wnd[1]").sendVKey (8)
    session.findById("wnd[0]").sendVKey (8)
   
    session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").pressToolbarContextButton ("&MB_EXPORT")
    session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").selectContextMenuItem ("&PC")
    session.findById("wnd[1]/usr/sub/2/sub/2/1/rad[4,0]").select()
    session.findById("wnd[1]/usr/sub/2/sub/2/1/rad[4,0]").setFocus()
    session.findById("wnd[1]/tbar[0]/btn[0]").press()
    session.findById("wnd[0]/tbar[0]/btn[3]").press() #voltar pra aba principal
   
    #Criar DataFrame ETDZ
    df_etdz = pd.read_clipboard(sep='|', skiprows=3, skipinitialspace=True)
    df_etdz = df_etdz.iloc[:,1:3]
    df_etdz.columns = ['equi','reg.log']
    df_etdz = df_etdz.loc[~df_etdz['equi'].isnull()]
    df_etdz['equi'] = df_etdz['equi'].apply(lambda x: str(int(x)))
    df_etdz['reg.log'] = df_etdz['reg.log'].apply(lambda x: str(int(x)))

    df_merge1 = df_v_equi.merge(df_etdz, how='left', left_on='Equipamento', right_on='equi')
       
   
    #EXTRAÇÃO EASTS
    df_merge1['reg.log'].to_clipboard(excel=True, sep=None, index=False, header=None)
    session.findById("wnd[0]").maximize
    session.findById("wnd[0]/usr/ctxt[0]").text = "EASTS"
    session.findById("wnd[0]/usr/ctxt[0]").caretPosition = 5
    session.findById("wnd[0]").sendVKey (0)
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").columns.elementAt(5).width = 8
    session.findById("wnd[0]").sendVKey (18)
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,1]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,2]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/ctxt[2,3]").text = "31.12.9999"
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/btn[1,5]").setFocus()
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/btn[1,5]").press()
    session.findById("wnd[1]/usr/cntlGRID/shellcont/shell").currentCellRow = 2
    session.findById("wnd[1]/usr/cntlGRID/shellcont/shell").selectedRows = "2"
    session.findById("wnd[1]/usr/cntlGRID/shellcont/shell").doubleClickCurrentCell()
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/ctxt[2,5]").text = "x"
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/ctxt[2,7]").text = "EAT10"
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/btn[4,2]").setFocus()
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/btn[4,2]").press()
    session.findById("wnd[1]/tbar[0]/btn[24]").press()
    session.findById("wnd[1]").sendVKey (8)
    session.findById("wnd[0]").sendVKey (8)
   
    session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").pressToolbarContextButton ("&MB_EXPORT")
    session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").selectContextMenuItem ("&PC")
    session.findById("wnd[1]/usr/sub/2/sub/2/1/rad[4,0]").select()
    session.findById("wnd[1]/usr/sub/2/sub/2/1/rad[4,0]").setFocus()
    session.findById("wnd[1]/tbar[0]/btn[0]").press()
    session.findById("wnd[0]").sendVKey (12)
   
    #Criar DataFrame EASTS
    df_easts = pd.read_clipboard(sep='|', skiprows=3, skipinitialspace=True)
    df_easts = df_easts.iloc[:,1:3]
    df_easts.columns = ['inst', 'reg.log']
    df_easts = df_easts.loc[~df_easts['reg.log'].isnull()]
    df_easts['reg.log'] = df_easts['reg.log'].apply(lambda x: str(int(x)))
    df_easts['inst'] = df_easts['inst'].apply(lambda x: str(int(x)))
   
    df_merge2 = df_merge1.merge(df_easts, how='right', left_on='reg.log', right_on='reg.log')
   
   
    #EXTRAÇÃO EANL
    df_merge2['inst'].to_clipboard(excel=True, sep=None, index=False, header=None)
    session.findById("wnd[0]").maximize()
    session.findById("wnd[0]/usr/ctxt[0]").text = "eanl"
    session.findById("wnd[0]/usr/ctxt[0]").caretPosition = 4
    session.findById("wnd[0]").sendVKey (0)
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").columns.elementAt(5).width = 8
    session.findById("wnd[0]").sendVKey (18)
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,1]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,3]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,7]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,9]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,9]").setFocus()
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 3
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 6
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,14]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,16]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,16]").setFocus()
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 3
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 0
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/btn[4,1]").setFocus()
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/btn[4,1]").press()
    session.findById("wnd[1]/tbar[0]/btn[24]").press()
    session.findById("wnd[1]/tbar[0]/btn[8]").press()
    session.findById("wnd[0]").sendVKey (8)
   
    session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").pressToolbarContextButton ("&MB_EXPORT")
    session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").selectContextMenuItem ("&PC")
    session.findById("wnd[1]/usr/sub/2/sub/2/1/rad[4,0]").select()
    session.findById("wnd[1]/usr/sub/2/sub/2/1/rad[4,0]").setFocus()
    session.findById("wnd[1]/tbar[0]/btn[0]").press()
    session.findById("wnd[0]/tbar[0]/btn[3]").press() #voltar pra aba principal

    #Criar DataFrame EALN
    df_ealn = pd.read_clipboard(sep='|', skiprows=3, skipinitialspace=True)
    df_ealn = df_ealn.iloc[:,1:7]
    df_ealn.columns = ['Instalação', 'Loc.consum','Nív.tensão','TpIns','Dt.criação','Modificado em']
    df_ealn = df_ealn.loc[~df_ealn['Instalação'].isnull()]
    #df_ealn['Loc.consum'] = df_ealn['Loc.consum'].apply(lambda x: str(int(x)))
    df_ealn['Instalação'] = df_ealn['Instalação'].apply(lambda x: str(int(x)))
    df_ealn['Loc.consum'] = df_ealn['Loc.consum'].apply(lambda x: str(int(x)))
    df_ealn['Nív.tensão'] = df_ealn['Nív.tensão'].apply(lambda x: str(int(x)))

    df_merge3 = df_merge2.merge(df_ealn, how='left', left_on = 'inst', right_on = 'Instalação')
   
   
    #EXTRAÇÃO EVBS
    df_merge3['Loc.consum'].to_clipboard(excel=True, sep=None, index=False, header=None)
    session.findById("wnd[0]").maximize()
    session.findById("wnd[0]/usr/ctxt[0]").text = "evbs"
    session.findById("wnd[0]/usr/ctxt[0]").caretPosition = 4
    session.findById("wnd[0]").sendVKey (0)
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").columns.elementAt(5).width = 8
    session.findById("wnd[0]").sendVKey (18)
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,1]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,2]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,6]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,19]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,19]").setFocus()
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 3
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 6
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 9
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,20]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,20]").setFocus()
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 12
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 15
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,19]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/chk[5,20]").selected = True
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 18
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 21
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC").verticalScrollbar.position = 0
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/btn[4,1]").setFocus ()
    session.findById("wnd[0]/usr/tblSAPLSE16NSELFIELDS_TC/btn[4,1]").press ()
    session.findById("wnd[1]/tbar[0]/btn[24]").press ()
    session.findById("wnd[1]/tbar[0]/btn[8]").press ()
    session.findById("wnd[0]").sendVKey (8)
   
    session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").pressToolbarContextButton ("&MB_EXPORT")
    session.findById("wnd[0]/usr/cntlRESULT_LIST/shellcont/shell").selectContextMenuItem ("&PC")
    session.findById("wnd[1]/usr/sub/2/sub/2/1/rad[4,0]").select()
    session.findById("wnd[1]/usr/sub/2/sub/2/1/rad[4,0]").setFocus()
    session.findById("wnd[1]/tbar[0]/btn[0]").press()
    session.findById("wnd[0]/tbar[0]/btn[3]").press() #voltar pra aba principal

    #Criar DataFrame EVBS
    df_evbs = pd.read_clipboard(sep='|', skiprows=3, skipinitialspace=True)
    df_evbs = df_evbs.iloc[:,1:6]
    df_evbs.columns = ['Local de consumo', 'Objeto de ligação','Detalhes da Localização','Nº do Poste','Tipo de Medição']
    df_evbs = df_evbs.loc[~df_evbs['Local de consumo'].isnull()]
    df_evbs['Local de consumo'] = df_evbs['Local de consumo'].apply(lambda x: str(int(x)))


    df_merge4 = df_merge3.merge(df_evbs, how='left', left_on = 'Loc.consum', right_on = 'Local de consumo')
    return df_merge4


df_nt_SMC = df_origem


if df_nt_SMC.size > 0:
    login_sap(transacao = 'SE16N', titulo_transacao = 'Exibição geral de tabela')
    df_SMC = extract_SMC(df_nt_SMC)
    df_SMC.to_excel('C:/Users/U470167/IBERDROLA S.A/Automacao - Documentos/Rotinas_Python/Teste_Robo_SMC/Extracao_SMC.xlsx', sheet_name='Planilha1', index=False)