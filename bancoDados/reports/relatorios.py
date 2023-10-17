
from conexion.oracle_queries import OracleQueries

class Relatorio:
    def __init__(self):
        # Abre o arquivo com a consulta e associa a um atributo da classe
        with open("/home/labdatabase/Workplace/bancoDados/sql/relatorio_cliente.sql") as f:
            self.query_relatorio_cliente = f.read()

        with open("/home/labdatabase/Workplace/bancoDados/sql/relatorio_tecnico.sql") as f:
            self.query_relatorio_tecnico = f.read()

        with open("/home/labdatabase/Workplace/bancoDados/sql/relatorio_peca.sql") as f:
            self.query_relatorio_peca = f.read()

        with open("/home/labdatabase/Workplace/bancoDados/sql/relatorio_ordem_servico.sql") as f:
            self.query_relatorio_ordem_servico = f.read()

        # Abre o arquivo com a consulta e associa a um atributo da classe
        with open("/home/labdatabase/Workplace/bancoDados/sql/relatorio_peca_utilizada.sql") as f:
            self.query_relatorio_pecas_utilizadas = f.read()

    def get_relatorio_cliente(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print(oracle.sqlToDataFrame(self.query_relatorio_cliente))
        input("Pressione Enter para Sair do Relatório de Clientes")

    def get_relatorio_tecnico(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print(oracle.sqlToDataFrame(self.query_relatorio_tecnico))
        input("Pressione Enter para Sair do Relatório de Técnicos")

    def get_relatorio_peca(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print(oracle.sqlToDataFrame(self.query_relatorio_peca))
        input("Pressione Enter para Sair do Relatório de Peças")

    def get_relatorio_ordem_servico(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print(oracle.sqlToDataFrame(self.query_relatorio_ordem_servico))
        input("Pressione Enter para Sair do Relatório de Ordem de Serviço")

    def get_relatorio_pecas_utilizadas(self):
        # Cria uma nova conexão com o banco que permite alteração
        oracle = OracleQueries()
        oracle.connect()
        # Recupera os dados transformando em um DataFrame
        print(oracle.sqlToDataFrame(self.query_relatorio_pecas_utilizadas))
        input("Pressione Enter para Sair do Relatório de Peças Utilizadas na Ordem de Serviço")