from conexion.oracle_queries import OracleQueries
from controller.controller_clientes import ControllerCliente
from controller.controller_tecnicos import ControllerTecnico
from model.clientes import Cliente
from model.ordens_servico import OrdemServico
from model.tecnicos import Tecnico

class ControllerOrdemServico:
    def __init__(self):
        self.ctrl_cliente = ControllerCliente()
        self.ctrl_tecnico = ControllerTecnico()

    def inserir_ordem_servico(self) -> OrdemServico:

        oracle = OracleQueries(can_write=True)
        oracle.connect()

        self.listar_clientes(oracle, need_connect=True)
        cliente_id = int(input("Digite o ID do cliente: "))
        cliente = self.valida_cliente(oracle, cliente_id)
        if cliente==None:
            return None

        self.listar_tecnicos(oracle, need_connect=True)
        tecnico_id = int(input("Digite o ID do técnico: "))
        tecnico = self.valida_tecnico(oracle, tecnico_id)
        if tecnico==None:
            return None

        var_ordem_id = int(input("Informe o número da ordem de serviço: "))

        if self.verifica_existencia_ordem_servico(oracle, var_ordem_id):

            data_abertura = input("Informe a data de abertura da Ordem de Serviço (DD/MM/AAAA): ")
            data_conclusao = input("Informe a data de conclusão da Ordem de Serviço (DD/MM/AAAA): ")
            status_os = str(input("Informe o status da Ordem de Serviço: "))
            solucao = str(input("Informe a solução da ordem de serviço: "))
            custo_total = float(input("Informe o custo total da ordem de serviço: "))

            oracle.write(f"insert into ordem_servico values('{var_ordem_id}', '{cliente_id}', '{tecnico_id}', '{data_abertura}', '{data_conclusao}', '{status_os}', '{solucao}', '{custo_total}')")

            df_ordem_servico = oracle.sqlToDataFrame(f"select ordem_id, cliente_id, tecnico_id, data_abertura, data_conclusao, status_os, solucao, custo_total from ordem_servico where ordem_id = {var_ordem_id}")

            nova_ordem_servico = OrdemServico(df_ordem_servico.ordem_id.values[0], cliente, tecnico,
                                              df_ordem_servico.data_abertura.values[0],
                                              df_ordem_servico.data_conclusao.values[0], df_ordem_servico.status_os.values[0],
                                              df_ordem_servico.solucao.values[0], df_ordem_servico.custo_total.values[0])

            print(nova_ordem_servico.to_string())
            return nova_ordem_servico
        else:
            print(f"O ID nº {var_ordem_id},já pertence a uma ordem de serviço.")
            return None

    def atualizar_ordem_servico(self) -> OrdemServico:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        ordem_id = int(input("Informe o número da ordem de serviço que será alterada: "))

        if not self.verifica_existencia_ordem_servico(oracle, ordem_id):

            cliente_id = int(input("Digite o ID do cliente: "))
            cliente = self.valida_cliente(oracle, cliente_id)
            if cliente == None:
                return None

            tecnico_id = int(input("Digite o ID do técnico: "))
            tecnico = self.valida_tecnico(oracle, tecnico_id)
            if tecnico == None:
                return None

            data_abertura = input("Informe a nova data de abertura da Ordem de Serviço (DD/MM/AAAA): ")
            data_conclusao = input("Informe a nova data de conclusão da Ordem de Serviço (DD/MM/AAAA): ")
            status_os = input("Informe o status novo da Ordem de Serviço: ")
            solucao = input("Informe a solução nova da ordem de serviço: ")
            custo_total = float(input("Informe o custo total da ordem de serviço: "))

            oracle.write(f"update ordem_servico set cliente_id = {cliente.get_cliente_id()}, tecnico_id = {tecnico.get_tecnico_id()}, data_abertura = {data_abertura}, data_conclusa = {data_conclusao}, status_os = {status_os}, solucao = {solucao}, custo_total = {custo_total} where ordem_id = {ordem_id}")

            df_ordem_servico = oracle.sqlToDataFrame(f"select ordem_id, data_abertura, data_conclusao, status_os, solucao, custo_total from ordem_servico where ordem_id = {ordem_id}")

            ordem_servico_atualizada = OrdemServico(df_ordem_servico.ordem_id.values[0], cliente, tecnico,
                                            df_ordem_servico.data_abertura.values[0],
                                            df_ordem_servico.data_conclusao.values[0], df_ordem_servico.status_os.values[0],
                                            df_ordem_servico.solucao.values[0], df_ordem_servico.custo_total.values[0])

            print(ordem_servico_atualizada.to_string())
            return ordem_servico_atualizada
        else:
            print(f"A ordem de serviço nº, {ordem_id}, não existe. ")

    def excluir_ordem_servico(self) -> OrdemServico:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        ordem_id = int(input("Informe o número da ordem de serviço que será excluída: "))

        if not self.verifica_existencia_ordem_servico(oracle, ordem_id):

            df_ordem_servico = oracle.sqlToDataFrame(f"select ordem_id, cliente_id, tecnico_id, data_abertura, data_conclusao, status_os, solucao, custo_total from ordem_servico "f"where ordem_id = {ordem_id}")

            cliente = self.valida_cliente(oracle, df_ordem_servico.cliente_id.values[0])
            tecnico = self.valida_tecnico(oracle, df_ordem_servico.tecnico_id.values[0])

            opcao_excluir = input(f"Tem certeza que deseja excluir a ordem de serviço nº {ordem_id} (S|N)? ")

            if opcao_excluir.lower() == "s":

                oracle.write(f"delete from ordem_servico where ordem_id = {ordem_id}")

                ordem_servico_excluida = OrdemServico(df_ordem_servico.ordem_id.values[0], cliente, tecnico,
                                                      df_ordem_servico.data_abertura.values[0],
                                                      df_ordem_servico.data_conclusao.values[0],
                                                      df_ordem_servico.status_os.values[0],
                                                      df_ordem_servico.solucao.values[0],
                                                      df_ordem_servico.custo_total.values[0])
                
                print(ordem_servico_excluida.to_string())
                print("Ordem de serviço excluída com sucesso!")
            

        else:
            print(f"A ordem de serviço nº, {ordem_id}, não existe. ")


    def verifica_existencia_ordem_servico(self, oracle: OracleQueries, ordem_id: int = None)-> bool:
        df_ordem_servico = oracle.sqlToDataFrame(f"select ordem_id, cliente_id, tecnico_id, data_abertura, data_conclusao, status_os, solucao, custo_total from ordem_servico where ordem_id = {ordem_id}")
        return df_ordem_servico.empty

    def listar_clientes(self, oracle: OracleQueries, need_connect: bool = False):
        query = """
                select c.cliente_id
                    , c.nome
                    , c.endereco
                    , c.email
                    , c.telefone
                    
                from clientes2 c
                order by c.cliente_id
                """

        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))

    def listar_tecnicos(self, oracle: OracleQueries, need_connect: bool = False):
        query = """
                select t.tecnico_id
                    , t.nome
                    , t.especialidade
                    , t.email
                    , t.telefone

                from LABDATABASE.tecnico t
                order by t.tecnico_id
                """

        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))

    def valida_cliente(self, oracle: OracleQueries, var_cliente_id: int = None) -> Cliente:
        if self.ctrl_cliente.verifica_existencia_cliente(oracle, var_cliente_id):
            print(f"O ID do cliente informado, {var_cliente_id}, não existe na base.")
            return None
        else:
            oracle.connect()

            df_cliente = oracle.sqlToDataFrame(f"select cliente_id, nome, endereco, email, telefone from clientes2 where cliente_id = '{var_cliente_id}'")

            cliente = Cliente(df_cliente.cliente_id.values[0], df_cliente.nome.values[0],
                              df_cliente.endereco.values[0], df_cliente.email.values[0],
                              df_cliente.telefone.values[0])
            return cliente

    def valida_tecnico(self, oracle: OracleQueries, tecnico_id: int = None) -> Tecnico:
        if self.ctrl_tecnico.verifica_existencia_tecnico(oracle, tecnico_id):
            print(f"O ID do tecnico informado, {tecnico_id}, não existe na base.")
            return None
        else:
            oracle.connect()

            df_tecnico = oracle.sqlToDataFrame(f"select tecnico_id, nome, especialidade, email, telefone from tecnico where tecnico_id = '{tecnico_id}'")

            tecnico = Tecnico(df_tecnico.tecnico_id.values[0], df_tecnico.nome.values[0],
                              df_tecnico.especialidade.values[0], df_tecnico.email.values[0],
                              df_tecnico.telefone.values[0])
            return tecnico