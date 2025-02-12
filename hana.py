# =============================================================================
# Biblioteca
# =============================================================================
from hdbcli import dbapi
from pathlib import Path
import openpyxl
from openpyxl import load_workbook
import math
import tkinter as tk
import win32com.client
import os
import datetime
import time
import numpy as np
import pandas as pd
import sys
import keys as k
# pip install pywin32 --proxy=http://array
# =============================================================================
# Funções
# =============================================================================
def hana_connect():
    # Conexão SAP HANA
    # print("Iniciar conexão com SAP HANA")
    global conn
    global cursor
    conn = dbapi.connect(
        address=k.servidor_hana,
        port=k.porta_hana,
        user=k.user_hana,
        password=k.pass_hana,
        databasename='BNP',
        sslValidateCertificate=False
    )
    cursor = conn.cursor()
    print('SAP HANA connected')

def hana_update(df,table,log:bool):
    hana_connect()
    inicio = time.time()

    if log:
        print('Em execução: UPDATE ' + table + ' as ' + time.strftime("%H:%M:%S", time.localtime(inicio)))
    #tb_rede
    if table == 'tb_rede':
        # Adequar estrutura
        df['dt_ativo_agrupamento'] = df['dt_ativo_agrupamento'].astype('string')

        # Substituir NaN por None, pois NaN não pode ser inserido em SQL
        df.replace({np.nan: None},inplace=True)
        if log:
            print('Em execução: UPDATE ' + table + 'as ' + time.strftime("%H:%M:%S",time.localtime(inicio)))
        if log:
            print('Em execução: UPDATE tb_rede')
        # Iterar sobre as colunas e valores desta linha
        for index, row in df.iterrows():
            set_parts = []
            # # Montar a lista de colunas dinamicamente desta linha
            [set_parts.append("{} = '{}'".format(coluna, valor)) for coluna, valor in row.items() if valor is not None and coluna != 'agrupamento'] # Obter os nomes das colunas do DataFrame
            # colunas = [set_parts.append("{} = '{}'".format(coluna, valor))
            #            for coluna, valor in row.items() if valor is not None and coluna != 'agrupamento']  # Obter os nomes das colunas do DataFrame

            # Montar a cláusula SET
            set_clause = ', '.join(set_parts)

            # Montar a cláusula WHERE
            where_clause = "{} = '{}'".format('agrupamento', row['agrupamento'])  # Assumindo que 'agrupamento' é uma string

            # Montar a query SQL dinamicamente
            query = "UPDATE CLB152269.TB_REDE SET {} WHERE {};".format(set_clause,where_clause)

        # Agora você pode executar a query SQL usando cursor.execute(query)
        cursor.execute(query)
    elif table == 'dt_update_rscm':         # df = df.strftime("%Y-%m-%d %H:%M:%S")
        query = "UPDATE CLB152269.AUX_CONFIG SET DT_UPDATE_RSCM='{}'".format(df.strftime("%Y-%m-%d %H:%M:%S"));
        cursor.execute(query)
        df = '1'

    conn.commit() # Este recurso sinaliza para o servidor de banco de dados que a aplicação já terminou o que queria realizar de alteração no banco.
    cursor.close()
    conn.close()
    if log:
        fim = time.time()
        duracao = fim - inicio
        duracao_m = int(duracao // 60) # parte inteira dos minutos
        duracao_s = int(duracao % 60) # resto da divisão
        print(str(len(df)) + " registro(s) inserido(s) em ", duracao_m," minutos e ", duracao_s, " segundos.")
    print(' ')

def hana_insert(df,table,log:bool):
    hana_connect()
    try:
        df = df.reset_index(drop=True)
    except:
        pass

    inicio = time.time()
    if 1:
        print('Em execução: INSERT ' + table + ' as ' + time.strftime("%H:%M:%S", time.localtime(inicio)))

    # tb_rede
    if table == 'tb_rede':
        # Adequar estrutura
        df['net'] = df['net'].astype('string')
        df['amp_sinal'] = df['amp_sinal'].astype('string')
        df['dt_cria_hemera'] = df['dt_cria_hemera'].astype('string')
        df['dt_ativo_agrupamento'] = df['dt_ativo_agrupamento'].astype('string')
        df.replace({np.nan: None},inplace=True)             # Substituir NaN por None, pois NaN não pode ser inserido em SQL

        for index, row in df.iterrows():            # Insert Dataframe into SQL Server:
            # Montar a lista de colunas dinamicamente desta linha
            colunas = [coluna for coluna, valor in row.items() if valor is not None]            # Obter os nomes das colunas do DataFrame

            # Montar a query SQL dinamicamente
            query = "INSERT INTO CLB152269.TB_REDE ({}) VALUES ({})".format(', '.join(colunas), ', '.join(
                ['?'] * len(colunas)))  # Para cada coluna, inserir um marcador de posição '?'

            # Montar a lista de valores dinamicamente desta linha
            valores = [row[coluna] for coluna in colunas]

            # Executar a instrução SQL para esta linha
            cursor.execute(query, valores) #tuple(row)

    elif table == 'ga_cliente':
        cursor.execute("DELETE FROM CLB152269.GA_CLIENTE WHERE dt_ref = CURRENT_DATE;")
        #cursor.execute('TRUNCATE TABLE CLB152269.'+table) # truncar tabela

        for index, row in df.iterrows():
            try:
                formatted_values = ", ".join([f"'{value}'" if isinstance(value, (str, pd.Timestamp)) else 'NULL' if pd.isna(value) else str(value) for value in row])
                formatted_query = f"INSERT INTO CLB152269.GA_CLIENTE (dt_ref, instalacao, dt_inst_desde, ctg_tar, set_indus, cl_cal, mru, mru_status, grupo_cliente, conta_contrato, PN, status_cliente, reg_log, equi_log, em, dt_em_desde, fat_reg, fat_calc, tp_medicao, em_fabri, em_modelo, em_ano, em_material, em_descricao) VALUES ({formatted_values})"
                cursor.execute(formatted_query)
            except Exception as e:
                conn.rollback()  # Reverter a transação em caso de erro
                print(f"Erro ao processar a linha {index}: {e}")
            else:
                conn.commit() # Este recurso sinaliza para o servidor de banco de dados que a aplicação já terminou o que queria realizar de alteração no banco.

            if index % 5000 == 0:
                print(f"Processando linha {index}...")
        print(f"Processando linha {len(df)}...FIM") #todo fazer uma barra de progresso

    elif table == 'SMC_HEMERA':
        # Adequar estrutura
        df['dt_ult_leitura'] = df['dt_ult_leitura'].astype('string')
        # Obter os nomes das colunas do DataFrame
        colunas = df.columns.tolist()
        # Montar a query SQL dinamicamente
        query = "INSERT INTO CLB152269."+table+" ({}) VALUES ({})".format(', '.join(colunas),', '.join(['?'] * len(colunas)))  # Para cada coluna, inserir um marcador de posição '?'
        for index, row in df.iterrows():    # Insert Dataframe into SQL Server:
            try:
                cursor.execute(query, tuple(row))   # Executar a instrução SQL para esta linha
            except Exception as e:
                conn.rollback()  # Reverter a transação em caso de erro
                print(f"Erro ao processar a linha {index}: {e}")
            else:
                conn.commit() # Este recurso sinaliza para o servidor de banco de dados que a aplicação já terminou o que queria realizar de alteração no banco.
    else:   # tb_rscm, aux_rscm_expurgo
        # Adequar estrutura
        if table == 'tb_rscm':
            df['dt_ult_leitura'] = df['dt_ult_leitura'].astype('string')
        elif table == 'aux_rscm_expurgo':
            df['dt_ult_leitura'] = df['dt_ult_leitura'].astype('string')
            df.drop(columns=['regiao', 'tecnologia', 'net'], inplace=True)
            df.replace({np.nan: None}, inplace=True)

        # Obter os nomes das colunas do DataFrame
        colunas = df.columns.tolist()

        # Montar a query SQL dinamicamente
        query = "INSERT INTO CLB152269."+table+" ({}) VALUES ({})".format(', '.join(colunas),', '.join(['?'] * len(colunas)))  # Para cada coluna, inserir um marcador de posição '?'
        # cursor.execute('TRUNCATE TABLE CLB152269.'+table) # truncar tabela
        for index, row in df.iterrows():    # Insert Dataframe into SQL Server:
            try:
                cursor.execute(query, tuple(row))   # Executar a instrução SQL para esta linha
            except Exception as e:
                conn.rollback()  # Reverter a transação em caso de erro
                print(f"Erro ao processar a linha {index}: {e}")
            else:
                conn.commit() # Este recurso sinaliza para o servidor de banco de dados que a aplicação já terminou o que queria realizar de alteração no banco.
    cursor.close()
    conn.close()
    if 1:
        fim = time.time()
        duracao = fim - inicio
        duracao_m = int(duracao // 60) # parte inteira dos minutos
        duracao_s = int(duracao % 60) # resto da divisão
        print(str(len(df)) + " registro(s) inserido(s) em ", duracao_m," minutos e ", duracao_s, " segundos.")
        print(' ')

def hana_read(query: str, log:bool):
    hana_connect()

    if log:
        inicio = time.time()

        # Localizar table
        a = query.find("clb152269.")
        b = query[a:].find(" ")
        if a != -1:
            a = a + len("clb152269.")
            if b != -1:
                b = b - len("clb152269.")
                table = query[a:a+b]
            else:
                table = query[a:]
        else:
            table = None
        print('Em execução: SELECT ' + table + ' as ' + time.strftime("%H:%M:%S", time.localtime(inicio)))

    #OBTER DADOS
    df = pd.read_sql_query(query, conn)
    conn.close()
    if log:
        fim = time.time()
        duracao = fim - inicio
        duracao_m = int(duracao // 60) # parte inteira dos minutos
        duracao_s = int(duracao % 60) # resto da divisão
        print(str(len(df)) + " registro(s) inserido(s) em ", duracao_m," minutos e ", duracao_s, " segundos.")
    print(' ')

    df.columns = df.columns.str.lower()
    if query == 'select * from clb152269.tb_rede':
        # Definir o tipo de dados
        df['dt_cria_hemera'] = df['dt_cria_hemera'].astype('string')
        df['dt_ativo_agrupamento'] = df['dt_ativo_agrupamento'].astype('string')
        #Classificação
        df = df.sort_values(by=['net', 'dt_ativo_agrupamento'], ascending=[True, False], na_position='first')
    return df