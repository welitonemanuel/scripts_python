class Medidor:
    def __init__(self, em, dt_leitura, leitura_kwh, autocad, status_rele, cs_associada, net_associada, cliente_associado, dt_ult_leitura=None):
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
        self.instalacao = instalacao
        self.em = em
        self.net = net
        self.cs = cs
        self.dt_ult_leitura = dt_ult_leitura
        self.dt_leitura = dt_leitura
        self.status_rele = status_rele
        self.leitura_kwh = leitura_kwh
        self.autocad = autocad

    def __str__(self):
        # Método especial que retorna uma string com informações do medidor
        # return f"Medidor {self._em}: {self._leitura_kwh} kWh ({self._dt_leitura}), Cliente: {self._cliente_associado}, CS: {self._cs_associada}, Rede: {self._net_associada}, Status Relé: {'ON' if self._status_rele else 'OFF'}, {'Autocad' if self._autocad else ''}"
        print("Instalação: ", self._instalacao)
        print("Medidor: ", self._em)
        print("Net: ", self._net)
        print("CS: ", self._cs)
        print("Data da última leitura: ", self._dt_ult_leitura)
        print("Data da leitura: ", self._dt_leitura)
        print("Leitura em kWh: ", self._leitura_kwh)
        print("Status do Relê: ", self._status_rede)
        print("Autocadastro: ", self._autocad)

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
