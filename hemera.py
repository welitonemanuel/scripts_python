# =============================================================================
# Biblioteca
# =============================================================================
import time     # Facilita desenvolvimento envolvendo tempo, tempo de espera, etc
import pandas as pd
# pd.set_option('max_columns', None)
#pd.set_option('display.max_rows', None) #visualizar todas as colunas
# pd.set_option('max_columns', None)
# pd.set_option('max_columns') voltar ao normal; quantidade de colunas visualizadas
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import glob # busca de arquivos em um diretório usando padrões de nome de arquivo.
import os
import shutil #Para mover um arquivo para outra pasta, você pode usar a função shutil.move() do módulo shutil.
from datetime import datetime
import sys
sys.path.insert(1, '../../wfuncoes py')
import keys as k
import excel as we
import hana as wh
# pip install pandas --proxy=http://array
# =============================================================================
# Classe
# =============================================================================
class Hemera:
    """
    ETL do relatório Situação de Status dos Medidores do Hemera - RSCM
        Args:
            log: Se quer a saída de log
    Etapas:
     1. Extrair
     2. Transformar
     3. Carregar
    Functions
        __rede_input: #Lê o arquivo '.\Database\rede.xlsx'
        __rede_update: #Caso haja modificação, atualizar o arquivo '.\Database\rede.xlsx'
        carregar: Carregar dados pickle
    """
    __slots__ = ['_log', '_tb', '_dt_update']   # proteger os atributos;
                        # não permitir que usuários de nossas classes criem outros atributos Economiza memória RAM

    def __init__(self, log: bool = False):
        self._log = log
        self._tb = pd.DataFrame()
        self._dt_update =  datetime(year=1, month=1, day=1, hour=0, minute=0, second=0)

    def __str__(self):
        return f"hemera.dt_update: {self._dt_update}\nhemera.tb: {self._tb.shape[0]} rows x {self._tb.shape[1]} columns"

    #Metodos GET e SET
    @property
    def log(self):
        return self._log
    @log.setter
    def log(self,log):
        if isinstance(log,bool):
            self._log = log
        else:
            print("Erro! o parâmetro não é tipo bool True/False")

    @property
    def tb(self):
        return self._tb
    @tb.setter
    def tb(self,tb):
        print("Erro! não é possível alterar este parâmetro")

    @property
    def dt_update(self):
        return self._dt_update
    @dt_update.setter
    def dt_update(self, dt_update):
        print("Erro! não é possível alterar este parâmetro")


    def extrair(self,usuario: str, senha: str):
        """
        Automação de acessar Hemera, baixar arquivo e salvar em pasta específica
        Sub etapas:
        1.01 Acessar o Hemera Coelba
        1.02 Baixar Relatório de Situação de Status dos Medidores
            Args:
            local: 'monitor_coelba','monitor_casa' ou 'notebook' default; informar para que o robô seja efetivo
        """
        # # =============================================================================
        # # 1.01 Login Hemera Coelba
        # # =============================================================================
        if self._log:
            print("=== Begin: 1 ===")
            print("=== Begin: 1.01 Acessar o Hemera Coelba ===")
        wait = 0.2
        link = "http://10.0.65.114:8080/hemera_coelba/loginHemera.jsp"

        chrome_opt = webdriver.ChromeOptions()
        prefs = {"credentials_enable_service": False,"profile.password_manager_enabled": False}
        chrome_opt.add_experimental_option("prefs", prefs)
        chrome_opt.add_experimental_option('excludeSwitches', ['enable-automation']) # Desabilita notificação de navegador
        
        nav = webdriver.Chrome(chrome_options=chrome_opt)
        nav.get(link)
        time.sleep(wait)
        
        campo_usuario = WebDriverWait(nav, 15).until(EC.presence_of_element_located((By.XPATH, "//input[@name='username']")))
        campo_usuario.send_keys(usuario)
        time.sleep(wait)
        
        campo_senha = WebDriverWait(nav, 5).until(EC.presence_of_element_located((By.XPATH, "//input[@name='password']")))
        campo_senha.send_keys(senha)
        time.sleep(wait)

        # Escolha de domínio (COSERN - full XPath: /html/body/div[3]/div/div[3])
        campo_dominio =WebDriverWait(nav,3).until(EC.presence_of_element_located((By.XPATH,
                                             '/html/body/div[1]/div[2]/div[2]/div[1]/div[1]/form/div/div[5]/div/div/input[2]')))

        campo_dominio.click()
        time.sleep(wait)
        # Selecionar DOMÍNIO COELBA
        combo_lista_item_coelba = WebDriverWait(nav, 5).until(EC.presence_of_element_located((By.XPATH,
                                                                                                 '/html/body/div[3]/div/div[1]')))
        combo_lista_item_coelba.click()
        time.sleep(wait)

        botao_login = WebDriverWait(nav, 5).until(EC.presence_of_element_located((By.ID, 'divCenterButton')))
        botao_login.click()

        # Espera frame carregar
        WebDriverWait(nav, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'iframe')))
        # Pega o XPath do iframe da página inicial
        iframe_pg_inicial = nav.find_element(By.TAG_NAME, 'iframe')
        # Muda o foco para o iframe
        nav.switch_to.frame(iframe_pg_inicial)
        
        #Fechar pop-up de dicas
        try:
            botao_fechar_pop_up = WebDriverWait(nav, 2).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[3]/div[4]/div')))
            botao_fechar_pop_up.click()
        except:
            #             print("Não tem tela de dica")
                pass

        time.sleep(wait)

        if self._log:
            print("=== End: 1.01 ===")
        # =============================================================================
        # 1.02 Baixar Relatório de Situação de Status dos Medidores
        # =============================================================================    
        if self._log:
            print("=== Begin: 1.02 Baixar o Relatório de Situação de Status dos Medidores ===")

        # Click Relatório Grupo B - menu
        botao_grupo_B_superior = WebDriverWait(nav, 5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ext-gen85"]/span')))
        botao_grupo_B_superior.click()
        time.sleep(wait)
        # Click Relatório Situação de Status dos medidores
        botao_rel_rscm = WebDriverWait(nav, 5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="mnu_relat"]/li[9]/a')))
        botao_rel_rscm.click()
        time.sleep(wait)
        time.sleep(wait)
        # Muda o foco para o iframe
        nav.switch_to.default_content()
        iframe_pg_inicial = nav.find_element(By.TAG_NAME, 'iframe')
        nav.switch_to.frame(iframe_pg_inicial)
        time.sleep(wait)
        # click exportar
        botao_exportar_csv = WebDriverWait(nav, 15).until(EC.presence_of_element_located((By.XPATH,'//*[@id="ext-gen34"]')))
        botao_exportar_csv.click() 

        # Aguardar finalizar download
        pasta_padrao_downloads_edge = r"C:\Users\u461539\Downloads"
        data_atual = datetime.now()
        data_formatada = data_atual.strftime('%Y%m%d')
        padrao_nome_arquivo = f"reportStatusCutMeter_{data_formatada}_*.csv"
#         print(padrao_nome_arquivo)
        caminho_arquivo = os.path.join(pasta_padrao_downloads_edge, padrao_nome_arquivo)

        if self._log:
            print("Download iniciado!")

        while len(glob.glob(caminho_arquivo)) == 0:
            # Aguardar um tempo antes de verificar novamente
            time.sleep(2)

        if self._log:
            print("Download concluído!")
        # pegar arquivo e mover para ./input:
        time.sleep(2)
        list_of_files = glob.glob(caminho_arquivo) # * means all if need specific format then *.csv
#         list_of_files = glob.glob(os.path.join(pasta_padrao_downloads_edge, "*.csv")) # * means all if need specific format then *.csv
        latest_file = max(list_of_files, key=os.path.getctime)
        pasta_root = r"C:\Users\u461539\OneDrive - IBERDROLA S.A\005.Scripts\wsmc\input"
#         display(latest_file)
#         display(novo_caminho)
        novo_caminho = os.path.join(pasta_root, os.path.basename(latest_file))
        shutil.move(latest_file, novo_caminho)
        time.sleep(1)
        if self._log:
            print("arquivo movido!")

        nav.close()         # Fechar navegador

        if self._log:
            print("=== End: 1.02 ===")
            print("=== End: 1 ===")
            print('')
        # =============================================================================
        # 2 transformada_rscm
        # =============================================================================
        # async
    def transformar(self):
        """
        Importar arquivo CSV e realizar as transformadas do RSCM
        Sub etapas:
        2.01 Carregar dados
        2.02 Delete columns e rows desnecessárias & Expurgos
        2.03 Formatar colunas dt_ult_leitura, leitura_kwh GRN e LNG
        2.04 Criar coluna net
        2.05 Atualizar Rede a partir das net's em Hemera
            Função rede_input
            Check de integridade tb_rede
        2.06 Expurgar medidores duplicados na mesma posição
        2.07 Expurgar medidores duplicados em posição diferente
        2.08 Expurgar medidores diferentes em mesma net_cs_posicao
        2.09 Exportar rscm e rscm_expurgo
            Exportar para Hana
            Exportar para Excel
            Exportar para pickle

        Args:
            local: 'monitor_coelba','monitor_casa' ou 'notebook' default; informar para que o robô seja efetivo
        """
        # =============================================================================
        # 2.01 Carregar dados
        # =============================================================================
        if self._log:
            print("=== Begin: 2 ===")
            print("=== Begin: 2.01 Carregar dados === ")

        arq = we.read_csv("reportStatusCutMeter",self._log)
        dt_update = arq['dt_update']
        rscm = arq['tabela']
        rscm.columns =rscm.columns.str.lower()

        if self._log:
            print(rscm.shape, "rscm")
            print("=== End: 2.01 ===")
            print('')
        # =============================================================================
        # 2.02 Delete columns e rows desnecessárias & Expurgos
        # =============================================================================
        if self._log:
            print("=== Begin: 2.02 Delete columns e rows desnecessárias ===")

        rscm_expurgo = rscm.loc[rscm['regiao'] == 'Elektro']  # agrupamento Elektro
        rscm_expurgo = rscm_expurgo.assign(tipo_erro=[f'regiao elektro' for i in range(len(rscm_expurgo))])
        rscm = rscm.loc[rscm['regiao'] != 'Elektro'].copy()
        if self._log:
            print(rscm_expurgo.shape, "rscm_expurgo: agrupamento Elektro")
        rscm_expurgo = rscm_expurgo.loc[rscm_expurgo['regiao'] != 'Elektro'].copy()  # agrupamento Elektro

        # rscm_expurgo: agrupamentos não inicia com G ou L
        rscm_expurgo_new = rscm.loc[
            ~(rscm['agrupamento'].str.startswith('G') | rscm['agrupamento'].str.startswith('L'))]
        rscm_expurgo_new = rscm_expurgo_new.assign(
            tipo_erro=[f'agrupamento não inicia com G ou L' for i in range(len(rscm_expurgo_new))])
        rscm_expurgo = pd.concat([rscm_expurgo, rscm_expurgo_new])
        rscm = rscm.loc[rscm['agrupamento'].str.startswith('G') | rscm['agrupamento'].str.startswith('L')].copy()
        if self._log:
            print(rscm_expurgo_new.shape, "rscm_expurgo: agrupamentos não inicia com G ou L")
        rscm_expurgo = rscm_expurgo.loc[
            rscm_expurgo['agrupamento'].str.startswith('G') | rscm_expurgo['agrupamento'].str.startswith('L')].copy()

        # rscm_expurgo: medidores sem leitura
        rscm_expurgo_new = rscm.loc[rscm['dt_ult_leitura'] == '']
        rscm_expurgo_new = rscm_expurgo_new.assign(
            tipo_erro=[f'medidores sem leitura' for i in range(len(rscm_expurgo_new))])
        rscm_expurgo = pd.concat([rscm_expurgo, rscm_expurgo_new])
        rscm = rscm.loc[rscm['dt_ult_leitura'] != ''].copy()
        if self._log:
            print(rscm_expurgo_new.shape, "rscm_expurgo: medidores sem leitura")

        # rscm_expurgo: medidores maior que 10 digitos
        rscm_expurgo_new = rscm.loc[rscm.em.apply(lambda x: len(x)) > 10]
        rscm_expurgo_new = rscm_expurgo_new.assign(
            tipo_erro=[f'medidores maior que 10 digitos' for i in range(len(rscm_expurgo_new))])
        rscm_expurgo = pd.concat([rscm_expurgo, rscm_expurgo_new])
        rscm = rscm.loc[~(rscm.em.apply(lambda x: len(x)) > 10)].copy()
        if self._log:
            print(rscm_expurgo_new.shape, "rscm_expurgo: medidores maior que 10 digitos")

        # rscm_expurgo: medidores menor que 10 digitos
        rscm_expurgo_new = rscm.loc[rscm.em.apply(lambda x: len(x)) < 10]
        rscm_expurgo_new = rscm_expurgo_new.assign(
            tipo_erro=[f'medidores menor que 10 digitos' for i in range(len(rscm_expurgo_new))])
        rscm_expurgo = pd.concat([rscm_expurgo, rscm_expurgo_new])
        # display(rscm_expurgo_new)
        rscm = rscm.loc[~(rscm.em.apply(lambda x: len(x)) < 10)].reset_index(drop=True).copy()
        # display(rscm)
        if self._log:
            print(rscm_expurgo_new.shape, "rscm_expurgo: medidores menor que 10 digitos")

        # rscm_expurgo: medidores fora da faixa
        rscm_expurgo_new = rscm[~rscm['em'].between('1000000000', '1299999999')]
        rscm_expurgo_new = rscm_expurgo_new.assign(
            tipo_erro=[f'num patrimonio fora da faixa 1.000.000.000 e 1.299.999.999' for i in
                       range(len(rscm_expurgo_new))])
        rscm_expurgo = pd.concat([rscm_expurgo, rscm_expurgo_new])
        rscm = rscm.loc[rscm['em'].between('1000000000', '1299999999')].copy()
        if self._log:
            print(rscm_expurgo_new.shape, "rscm_expurgo: num patrimonio fora da faixa")

        # exclui as colunas uc, regiao e tecnologia
        rscm = rscm[['em', 'agrupamento', 'cs', 'posicao', 'dt_ult_leitura', 'leitura_kwh', 'status_rele']].copy()

        if self._log:
            print(rscm_expurgo.shape, "rscm_expurgo")
            print(rscm.shape, "rscm")
            print("=== End: 2.02 ===")
            print('')
        # =============================================================================
        # 2.03 Formatar colunas dt_ult_leitura, leitura_kwh GRN e LNG,
        # =============================================================================
        if self._log:
            print("=== Begin: 2.03 Formatar colunas dt_ult_leitura, leitura_kwh GRN e LNG ===")

        # Convertendo a coluna "leitura_kwh" para um tipo numérico adequado
        rscm.loc[:, 'dt_ult_leitura'] = pd.to_datetime(rscm['dt_ult_leitura'], format='%d/%m/%Y')
        rscm2 = rscm.copy()
        rscm2['leitura_kwh'] = rscm2['leitura_kwh'].str.replace('[\.,-]', '', regex=True).str[:-4]
        # rscm2['leitura_kwh'] = rscm2['leitura_kwh'].replace([',', '\.', '-'], ['', '', ''], regex=True).str[:-4]  # .astype(float)
        # Substituir valores na coluna 'leitura_kwh' de acordo com a inicial da coluna 'agrupamento'
        rscm2['leitura_kwh'] = rscm2.apply(
            lambda row: 0 if row['agrupamento'].startswith('G') and len(row['leitura_kwh']) < 1 else \
                (0 if row['agrupamento'].startswith('L') and len(str(row['leitura_kwh'])) <= 3 else \
                     row['leitura_kwh'][:-3] if row['agrupamento'].startswith('L') and row['leitura_kwh'].isdigit() else \
                         row['leitura_kwh']), axis=1).astype(int)
        # print(rscm2)
        if self._log:
            print(rscm2.info())
            print("=== End: 2.03 ===")
            print('')
        # =============================================================================
        # 2.04 Criar coluna net
        # =============================================================================
        if self._log:
            print("=== Begin: 2.04 Criar coluna net ===")

        rscm3 = rscm2.copy()
        try:
            rscm3['net'] = rscm3['agrupamento'].str[4:8].astype(int)
        except:
            print("Erro 2.04: Tem agrupamento em formatação indevida.")
            return
        rscm3 = rscm3[['net', 'cs', 'em', 'posicao', 'dt_ult_leitura', 'leitura_kwh', 'status_rele',
                       'agrupamento']].copy().sort_values(by=['net', 'cs', 'posicao', 'em'])
        if self._log:
            print(rscm3.keys())
            print("===End: 2.04 ===")
            print('')
        # =============================================================================
        # 2.05 Atualização das redes
        # =============================================================================
        if self._log:
            print("=== Begin: 2.05 Atualizar tb_rede ===")

        net_rscm4 = rscm3.loc[:, ['net', 'agrupamento']].drop_duplicates(subset=['net', 'agrupamento']).sort_values(
            by=['net', 'agrupamento']).reset_index(drop=True)

        self.__rede_input(net_rscm4)    # rotina que adiciona em rede as novas redes ou novos agrupamentos (de net existente)

        if self._log:
            print("===End: 2.05 ===")
            print('')
        # =============================================================================
        # 2.06 Expurgar medidores duplicados na mesma posição
        #   Expurgar medidores duplicados mesma posição-> saída rscm_expurgo
        #   Retirar de rscm as linhas duplicadas
        # =============================================================================
        if self._log:
            print("=== Begin: 2.06 Expurgar medidor duplicado em net_cs_pos igual ===")

        rscm4 = rscm3[['net', 'cs', 'posicao', 'em', 'dt_ult_leitura', 'leitura_kwh', 'status_rele',
                       'agrupamento']].copy().sort_values(by=['net', 'cs', 'posicao', 'em'])
        duplicatas = rscm4.duplicated(subset=['net', 'cs', 'em', 'posicao', 'dt_ult_leitura', 'leitura_kwh'],
                                      keep='first')

        rscm_expurgo_new = rscm4[duplicatas].drop_duplicates()
        try:
            rscm_expurgo_new.loc[:, 'tipo_erro'] = 'medidor duplicado em net_cs_pos igual'
        except Exception as e:
            print(f"Não encontrado 'medidor duplicado em net_cs_pos igual': {e}")

        if self._log:
            print(rscm_expurgo_new.shape, 'rscm_expurgo medidor duplicado em net_cs_pos igual')
        rscm_expurgo = pd.concat([rscm_expurgo, rscm_expurgo_new], ignore_index=True)
        if self._log:
            print(rscm_expurgo.shape, 'rscm_expurgo final')
        # tirar de rscm as linhas duplicadas
        rscm4 = rscm4.drop_duplicates(subset=['net', 'cs', 'em', 'posicao', 'dt_ult_leitura', 'leitura_kwh']).copy()
        if self._log:
            print(rscm4.shape, 'rscm4')
            print(rscm_expurgo.shape, 'rscm_expurgo')
            print("===End: 2.06 ===")
            print('')

        # =============================================================================
        # 2.07 Expurgar medidores duplicados em posição diferente
        #   Expurgar medidores duplicados em posição diferente -> saída rscm_expurgo
        #   Retirar de rscm as linhas duplicadas
        # =============================================================================
        if self._log:
            print("=== Begin: 2.07 Expurgar medidor duplicado em net_cs_pos diferente ===")

        rscm6 = rscm4.copy().sort_values(by=['em', 'dt_ult_leitura', 'net', 'cs', 'posicao'],
                                         ascending=[True, False, True, True, True]).reset_index(drop=True)
        duplicatas = rscm6.duplicated(subset=['em'], keep=False)
        rscm_duplicatas = rscm6[duplicatas].reset_index(drop=True)
        try:
            rscm_duplicatas.loc[:, 'tipo_erro'] = 'medidor duplicado em net_cs_pos diferente'
        except Exception as e:
            print(f"Não encontrado 'medidor duplicado em net_cs_pos diferente': {e}")

        if self._log:
            print(rscm_duplicatas.shape, 'rscm_expurgo medidor duplicado em net_cs_pos diferente')
        rscm_expurgo = pd.concat([rscm_expurgo, rscm_duplicatas], ignore_index=True)
        if self._log:
            print(rscm_expurgo.shape, 'rscm_expurgo final')
        # tirar de rscm as linhas duplicadas
        rscm6 = rscm6.drop_duplicates(subset=['em']).copy()
        if self._log:
            print(rscm6.shape, 'rscm6')
            print("===End: 2.07 ===")
            print('')
        # =============================================================================
        # 2.08 Expurgar medidor diferente na mesma net_cs_pos
        #   Selecionar medidores diferentes em mesma net_cs_posicao -> saída rscm_expurgo
        #   Manter rscm
        # =============================================================================
        if self._log:
            print("=== Begin: 2.08 Expurgar medidores diferentes na mesma net_cs_pos ===")

        rscm7 = rscm6.copy().sort_values(by=['net', 'cs', 'posicao', 'dt_ult_leitura'],
                                         ascending=[True, True, True, False]).reset_index(drop=True)
        duplicatas = rscm7.duplicated(subset=['net', 'cs', 'posicao'], keep=False)
        rscm_duplicatas = rscm7[duplicatas].reset_index(drop=True)
        rscm_duplicatas.loc[:, 'tipo_erro'] = 'medidores diferentes na mesma net_cs_pos'
        if self._log:
            print(rscm_duplicatas.shape, 'rscm_expurgo medidores diferentes na mesma net_cs_pos')
        rscm_expurgo = pd.concat([rscm_expurgo, rscm_duplicatas], ignore_index=True)

        if self._log:
            print(rscm7.shape, 'rscm7')
            print(rscm_expurgo.shape, 'rscm_expurgo')
            print("===End: 2.08 ===", end='\n')
            print('')

        # =============================================================================
        # 2.09 Exportar rscm e rscm_expurgo e dt_update
        #   Exportar para Excel
        #   Exportar para Hana
        #   Exportar pickle
        #   Excluir pickle repetido do mês
        #   Excluir rscm.csv já tratado
        # =============================================================================
        if self._log:
            print("=== Begin: 2.09 Exportar ao HANA: RSCM, dt_update, rscm_expurgo ===")

        # Exportar Excel
        rscm7.to_csv(r'.\output\rscm.csv', sep=';', index=False)
        rscm_expurgo.to_excel(".\output\\rscm_expurgo.xlsx", sheet_name='Plan1',index=False)
        if self._log:
            print('exportado Excel rscm.csv e rscm_expurgo.xlsx')

        # Exportar Hana
        wh.hana_insert(rscm7, 'tb_rscm', self._log)
        wh.hana_insert(rscm_expurgo, 'aux_rscm_expurgo', self._log)
        wh.hana_update(dt_update, 'dt_update_rscm', self._log)

        # Exportar pickle
        pd.to_pickle([dt_update, rscm7], './pickle/rscm/rscm_' + dt_update.strftime(
            '%Y-%m-%d_%H_%M_%S') + '.pkl')
        if self._log:
            print('exportado rscm pickle')

        #excluir reportStatusCutMeter
        file_name = 'reportStatusCutMeter_'+dt_update.strftime('%Y%m%d_%H%M%S')+'.csv'
        path = './input/'+file_name
        try:
            os.remove(path)
            if self._log:
                print(f"O arquivo \'{file_name}\' foi excluído")
        except:
            if self._log:
                print(f"Atenção. Erro ao excluir o arquivo \'{file_name}\'. O mesmo não foi excluído")

        #excluir pickle repetido no mês!!!
        file_name =  'rscm_' + dt_update.strftime('%Y-%m-%d_%H_%M_%S') + '.pkl'
        path = './pickle/rscm/' + file_name
        #todo fazer estrutura de varredura e remover arquivo repetido no mes!!!

        self._tb = rscm7
        self._dt_update = dt_update
        if self._log:
            print("===End: 2.09 ===", end='\n')
            print('')

    def carregar(self):
        # =============================================================================
        # Carregar tb_rscm do HANA
        # =============================================================================
        if self._log:
            print("=== Begin: 3.01 Carregar rscm ao hana ===")

        rscm = pd.DataFrame()
        rscm = wh.hana_read('select * from clb152269.tb_rscm',self._log)
        self._tb = rscm

        # obj = datetime(year=1, month=1, day=1, hour=0, minute=0, second=0)
        obj = wh.hana_read('select dt_update_rscm from clb152269.aux_config LIMIT 1', self._log)
        self._dt_update =  obj.dt_update_rscm[0]

    def __rede_input(self, net_rscm: object):
        """
        Rotina que adicionar em rede as novas redes ou atualiza novos agrupamentos de net's existentes
        Sub etapas:
            1. Criar dataframe rede
            2. Identifica net e agrupamentos não contidos em rede
            3. Inserir os novos dados em rede
            4. Exporta Rede para o Excel
            Args:
            net_rscm: net's e agrupamentos de uma dataframe rscm
        """
        # =============================================================================
        # rede_input
        # =============================================================================
        # sub etapa 1
        rede = pd.DataFrame()
        rede = wh.hana_read('select * from clb152269.tb_rede',self._log)
        hana_i = pd.DataFrame(columns=rede.columns)  # colecionar as linhas que serão inseridas ao HANA
        hana_u = pd.DataFrame(columns=rede.columns)  # colecionar as linhas que serão inseridas ao HANA
        # hana_u = pd.DataFrame(columns=['set', 'value_set','where','value_where'])  # colecionar as linhas que serão atualizadas no HANA

        # sub etapa 2 - Identificar as redes novas ou nomenclatura de agrupamento modificado
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
                    dt_ativo_agrupamento= '9999-12-31',
                    dt_cria_hemera=datetime.now().date().strftime('%Y-%m-%d'),
                    construtor='#PENDENTE#',
                    referencia='#PENDENTE#',
                    trafo='#PEND',
                    poste='#PEND')
                hana_i = pd.concat([hana_i, net_nova])
            else:  # net existente; alteração de agrupamento
                print('Agrupamento atualizado: ' + net_rscm.iloc[row['index']]['agrupamento'])
                condition = ((rede['net'] == net_rscm.loc[row['index'], 'net']) & (rede['dt_ativo_agrupamento'] == '9999-12-31')) # seleção da linha do agrupamento da rede ativa;
                agr_i = rede.loc[condition].copy()
                agr_u = pd.DataFrame()
                agr_u['agrupamento'] = agr_i['agrupamento']
                agr_u['dt_ativo_agrupamento'] = datetime.now().date().strftime('%Y-%m-%d')
                agr_u['dt_update'] = datetime.now()
                hana_u = pd.concat([hana_u, agr_u])
                agr_i['agrupamento'] = net_rscm.iloc[row['index']]['agrupamento']
                agr_i['dt_cria'] = None
                agr_i['dt_update'] = None
                hana_i = pd.concat([hana_i, agr_i])
                # hana_u = hana_u.append({'set':'dt_ativo_agrupamento','value_set':datetime.now().date().strftime('%Y-%m-%d'),'where':'agrupamento','value_where':agr_novo['agrupamento'].values[0]},ignore_index=True)
                # agr_novo['agrupamento'] = net_rscm.iloc[row['index']]['agrupamento']        # Atualização do agrupamento

        if len(hana_i) > 0:
            wh.hana_insert(hana_i,'tb_rede', self._log)
            if len(hana_u) > 0:
                wh.hana_update(hana_u, 'tb_rede', self._log)
        else:
            if self._log:
                print("Não houve nova rede nem agrupamento renomeado.", end='\n')
                print(" ", end='\n')

        # Integridade tb_rede - Somente 1 net ativa (net_desativada nulo)
        if self._log:
            print("Check de integridade tb_rede", end='\n')
        rede = pd.DataFrame()
        rede = wh.hana_read('select * from clb152269.tb_rede order by net, dt_cria desc',self._log)
        rede['dt_ativo_agrupamento'] = rede['dt_ativo_agrupamento'].astype('string')
        duplicates = rede[rede.duplicated(subset='net', keep='first') & (rede['dt_ativo_agrupamento'] == '9999-12-31')]    # Encontrar as duplicatas
        if len(duplicates) > 0:
            print('!!! ALERTA !!!')
            print('ALERTA: Verificar a(s) rede(s) ' + str(rede.loc[duplicates.index, 'net'].values) + '. Mais de uma net/rede com dt_ativo_agrupamento 9999-12-31. Necessário intervenção.' )
            print('!!! ALERTA !!!')
            print('ATENÇÃO: O script interrompido.')
            sys.exit()

# =============================================================================
# DEBUG
# =============================================================================
if __name__ == "__main__":
    h1 = Hemera(True)
    h1.extrair(k.user_rede_u,k.pass_rede)
    # h1.transformar()
    # h1.carregar()
    # print(h1.tb.info())