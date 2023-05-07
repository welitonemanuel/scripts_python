class Medidor:
    def __init__(self, em, dt_leitura, leitura_kwh, autocad, status_rele, cs_associada, net_associada, cliente_associado, dt_ult_leitura=None):
        """
        Inicialização da classe Medidor

        Args:
            em (str): número do medidor
            dt_leitura (str): data da última leitura do medidor
            leitura_kwh (float): valor da última leitura do medidor em kWh
            autocad (bool): indica se o medidor está em autocadastro
            status_rele (bool): indica o status do relé do medidor
            cs_associada (str): nome da CS associada ao medidor
            net_associada (str): nome da rede associada ao medidor
            cliente_associado (str): nome do cliente associado ao medidor
            dt_ult_leitura (str): data da penúltima leitura do medidor (opcional)
        """
        self._em = em
        self._dt_leitura = dt_leitura
        self._leitura_kwh = leitura_kwh
        self._autocad = autocad
        self._status_rele = status_rele
        self._cs_associada = cs_associada
        self._net_associada = net_associada
        self._cliente_associado = cliente_associado
        self._dt_ult_leitura = dt_ult_leitura

    def __str__(self):
        """
        Método especial que retorna uma string com informações do medidor
        """
        return f"Medidor {self._em}: {self._leitura_kwh} kWh ({self._dt_leitura}), Cliente: {self._cliente_associado}, CS: {self._cs_associada}, Rede: {self._net_associada}, Status Relé: {'ON' if self._status_rele else 'OFF'}, {'Autocad' if self._autocad else ''}"

    def status_em_d2(self):
        """
        Verifica se o medidor está desconectado

        Returns:
            str: retorna "ON" se o medidor estiver conectado, "OFF" caso contrário
        """
        if not self._dt_ult_leitura:
            return "OFF"
        diferenca = (datetime.strptime(self._dt_leitura, '%d/%m/%Y') - datetime.strptime(self._dt_ult_leitura, '%d/%m/%Y')).days
        if diferenca < 2:
            return "ON"
        else:
            return "OFF"

    def obter_informacoes(self):
        """
        Método que imprime as informações do medidor
        """
        print(f"Medidor {self._em}: {self._leitura_kwh} kWh ({self._dt_leitura}), Cliente: {self._cliente_associado}, CS: {self._cs_associada}, Rede: {self._net_associada}, Status Relé: {'ON' if self._status_rele else 'OFF'}, {'Autocad' if self._autocad else ''}")
