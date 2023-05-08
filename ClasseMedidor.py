from datetime import date

class Medidor:
    def __init__(self, instalacao: int, em: int, net: int, pos: int, cs: int, dt_ult_leitura: date, \
                 dt_leitura: date, leitura_kwh: int, status_rele: str, \
                 em_log: str, em_modelo: str, em_ano_construcao :int, em_codigo_sap: str, \
                 em_descricao_sap: str \
                 ):
        """
        Inicialização da classe Medidor

        Args:
            instalacao (int): instalação do cliente
            em (int): número do medidor; 10 digitos
            net (int): nome da rede associada ao medidor; 4 digitos
            cs (int): nome da CS associada ao medidor; 3 digitos
            pos (int): posição do medidor na cs; de 1 até 12
            dt_ult_leitura (date): data da última leitura do medidor
            dt_leitura (date): data da última leitura do medidor
            leitura_kwh (int): valor da última leitura do medidor em kWh; 7 digitos
            status_rele (str): indica o status do relé do medidor; 45 caracteres
            em_log (str): número lógico do medidor; 18 digitos
            em_modelo (str): modelo do medidor; 45 caracteres
            em_ano_construcao (int): ano de construção do medidor; 4 digitos
            em_codigo_sap (int): código do modelo do medidor no SAP; 7 digitos
            em_descricao_sap (str); 45 caracteres
        """

        #Teste de consistência
        # if (not isinstance(instalacao, int) and not instalacao is None) or not 1 <= len(str(instalacao)) <= 10:
        if (not isinstance(instalacao, int) or not 0 < instalacao < 999999999) and instalacao is not None:
            raise ValueError("A instalação deve ser um número inteiro ou vazio.")
        else:
            self._instalacao = instalacao

        if not isinstance(em, int) or len(str(em)) != 10:
            raise ValueError("O medidor deve ser um número inteiro de 10 digitos.")
        else:
            self._em = em

        if not isinstance(net, int) or not 1 <= net < 2000:
            raise ValueError("A rede deve ser um número inteiro entre 1 e 1999.")
        else:
            self._net = net

        if (not isinstance(cs, int) or not 0 <= cs <= 999) and cs is not None:
            raise ValueError("O ID CS deve ser um número inteiro entre 0 e 999 ou vazio.")
        else:
            self._cs = cs

        if (not isinstance(pos, list) or 0< len(pos) > 3) and pos is not None:
            raise ValueError("A posição deve ser um número inteiro entre 1 e 12 ou vazio.")
        else:
            self._pos = pos

        if not isinstance(dt_ult_leitura, date):
            raise ValueError("A data da ultima leitura ser uma data válida.")
        elif dt_ult_leitura is None:  #SEM CADASTRO HEMERA
            self._dt_ult_leitura = date(2014, 1, 1)
        else:
            self._dt_ult_leitura = dt_ult_leitura

        if not isinstance(dt_leitura, date):
            raise ValueError("A data da ultima leitura ser uma data válida.")
        else:
            self._dt_leitura = dt_ult_leitura

        # if (not isinstance(leitura_kwh, int) and not leitura_kwh is None) or not 1 <= len(str(leitura_kwh)) < 2000:
        if (not isinstance(leitura_kwh, int) or not 0 <= leitura_kwh <= 9999999) and leitura_kwh is not None:
            raise ValueError("A leitura deve ser um número inteiro de até 7 digitos ou vazio.")
        else:
            self._leitura_kwh = leitura_kwh

        if not isinstance(status_rele, str) or status_rele not in ['Ligado', 'Cortado', \
            'Provavelmente Cortado','Provavelmente Ligado','Desconhecido', 'Cortado abertura de porta']:
            raise ValueError("O status_rede informado não corresponde a entrada esperada.")
        else:
            self._status_rele = status_rele

        if not isinstance(em_log, str) or len(str(em_log)) != 18:
            raise ValueError("O numero lógico do medidor deve possuir 18 caracteres.")
        else:
            self._em_log = em_log

        if not isinstance(em_modelo, str) or not 0 < len(em_modelo) <= 45:
            raise ValueError("O modelo do medidor não é válido.")
        else:
            self._em_modelo = em_modelo

        if not isinstance(em_ano_construcao, int) or len(str(em_ano_construcao)) != 4:
            raise ValueError("O modelo do medidor não é válido.")
        else:
            self._em_ano_construcao = em_ano_construcao

        if not isinstance(em_codigo_sap, str) or len(em_codigo_sap) != 7:
            raise ValueError("O código SAP do medidor não é válido.")
        else:
            self._em_codigo_sap = em_codigo_sap

        if not isinstance(em_descricao_sap, str) or not 0 < len(em_descricao_sap) <= 45:
            raise ValueError("A descrição do medidor não é válida.")
        else:
            self._em_descricao_sap = em_descricao_sap


    def __str__(self):
        # Método especial que retorna uma string com informações do medidor
        instalacao_str = "" if self._instalacao is None else str(self._instalacao)
        cs_str = "" if self._cs is None else str(self._cs)
        pos_str = "" if self._pos is None else str(self._pos)
        dt_ult_leitura_str = "" if self._dt_ult_leitura is None else str(self._dt_ult_leitura)
        leitura_kwh_str = "" if self._leitura_kwh is None else str(self._leitura_kwh)
        return "Instalação: " + instalacao_str + "\n" + \
        "Medidor: " + str(self._em) + "\n" + \
        "Net: " + str(self._net) + "\n" + \
        "CS: " + cs_str + "\n" + \
        "Posição: " + pos_str + "\n" + \
        "Data da última leitura: " + dt_ult_leitura_str + "\n" + \
        "Data da leitura: " + str(self._dt_leitura) + "\n" + \
        "Leitura em kWh: " + leitura_kwh_str + "\n" + \
        "Status do Relê: " + str(self._status_rele) + "\n"

    def status_em(self, dias:int) -> str:
        """
        Método que retorna o status do relé do medidor em, baseado na diferença entre as últimas duas leituras.

        Se a diferença for menor que dias, retorna 'ON'. Se for maior que dias, retorna 'OFF'.
        Se dt_ult_leitura for nulo, retorna 'OFF'.

        :param dias: quantidade máxima de dias para a diferença entre as leituras ser considerada 'ON'
        :return: string indicando o status do relé do medidor em
        """
        if not dias:
            dias = 2
        try:
            dias = int(dias)
            if dias <= 0:
                raise ValueError("O número de dias deve ser positivo.")
        except ValueError:
            print("O número de dias informado não é um inteiro positivo.")
            return None
        if not self._dt_ult_leitura: return "OFF"
        diff = (self._dt_leitura - self._dt_ult_leitura).days
        if diff < dias:
            return "ON"
        else:
            return "OFF"

        # testes da classe
if __name__ == "__main__":
     m1 = Medidor(instalacao= 5678, \
                em = 1234567890, pos = [1, 2, 3], cs = 999, net = 1122, \
                dt_ult_leitura = date(2013,1,1), \
                dt_leitura = date(2022, 5, 7),\
                leitura_kwh = 12345,\
                status_rele = 'Ligado', \
                em_log = '123456789012345678', \
                em_modelo = 'MT200', \
                em_ano_construcao = 2014, \
                em_codigo_sap = '0123456', \
                em_descricao_sap = 'Texto teste', \
                  )
     print(m1)