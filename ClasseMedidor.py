class Medidor:
    def __init__(self, instalacao, em, cs, net, dt_ult_leitura, dt_leitura, leitura_kwh, status_rele,autocad):
        """
        Inicialização da classe Medidor

        Args:
            em (int): número do medidor
            dt_leitura (date): data da última leitura do medidor
            leitura_kwh (int): valor da última leitura do medidor em kWh
            autocad (str): indica se o medidor está em autocadastro
            status_rele (str): indica o status do relé do medidor
            cs_associada (int(3)): nome da CS associada ao medidor
            net_associada (int(4)): nome da rede associada ao medidor
            cliente_associado (int(10)): nome do cliente associado ao medidor
            dt_ult_leitura (date): data da penúltima leitura do medidor (opcional)
        """
        self._instalacao = instalacao
        self._em = em
        self._cs = cs
        self._net = net
        self._dt_ult_leitura = dt_ult_leitura
        self._dt_leitura = dt_leitura
        self._leitura_kwh = leitura_kwh
        self._status_rele = status_rele
        self._autocad = autocad

    def __str__(self):
        # Método especial que retorna uma string com informações do medidor
        return "Instalação: " + str(self._instalacao) + "\n" + \
        "Medidor: " + str(self._em) + "\n" + \
        "Net: " + str(self._net) + "\n" + \
        "CS: " + str(self._cs) + "\n" + \
        "Data da última leitura: " + str(self._dt_ult_leitura) + "\n" + \
        "Data da leitura: " + str(self._dt_leitura) + "\n" + \
        "Leitura em kWh: " + str(self._leitura_kwh) + "\n" + \
        "Status do Relê: " + str(self._status_rele) + "\n" + \
        "Autocadastro: " + str(self._autocad)

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
        # try:
        #     dias = int(dias)
        #     if dias <= 0:
        #         raise ValueError("O número de dias deve ser positivo.")
        # except ValueError:
        #     print("O número de dias informado não é um inteiro positivo.")
        #     return None
        if not self._dt_ult_leitura: return "OFF"
        diff = (self.dt_leitura - self.dt_ult_leitura).days
        if diff < 2:
            return "ON"
        else:
            return "OFF"

        # testes da classe
if __name__ == "__main__":
     m1 = Medidor(123,456,999,9999,"01/01/2023","05/01/2023",32,"Ligado","SIM")
     print(m1)