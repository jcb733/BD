from conexion.oracle_queries import OracleQueries
from controller.controller_ordens_servico import ControllerOrdemServico
from controller.controller_pecas import ControllerPeca
from model.ordens_servico import OrdemServico
from model.pecas import Peca
from model.pecas_utilizadas import PecaUtilizada


class ControllerPecaUtilizada:

    def __init__(self):
        self.ctrl_peca = ControllerPeca()
        self.ctrl_ordem_servico = ControllerOrdemServico()

    def inserir_peca_utilizada(self) -> PecaUtilizada:

        oracle = OracleQueries(can_write=True)
        oracle.connect()

        self.listar_ordens_servico(oracle, need_connect=True)
        ordem_id = int(input("Informe o nº da ordem de serviço que deseja buscar: "))
        ordem_servico = self.valida_ordem_servico(oracle, ordem_id)
        if ordem_servico == None:
            return None

        self.listar_pecas(oracle, need_connect=True)
        peca_id = int(input("Digite o ID da peca: "))
        peca = self.valida_peca(oracle, peca_id)
        if peca==None:
            return None
        
        var_codigo = int(input("Informe o código do conjunto de peças utilizadas: "))

        if self.verifica_existencia_peca_utilizada(oracle, var_codigo):

            preco_uni = float(input("Informe o preço da peça: "))
            quant_utilizada = int(input("Informe a quantidade de peças utilizadas: "))

            oracle.write(f"insert into pecas_utilizadas values('{var_codigo}', '{peca_id}', '{ordem_id}','{preco_uni}', '{quant_utilizada}')")

            df_peca_utilizada = oracle.sqlToDataFrame(f"select peca_utilizada_id, peca_id, ordem_id, preco_uni, quant_utilizada from pecas_utilizadas where peca_utilizada_id = {var_codigo}")

            nova_peca_utilizada = PecaUtilizada(df_peca_utilizada.peca_utilizada_id.values[0], peca, ordem_servico,
                                                df_peca_utilizada.preco_uni.values[0],
                                                df_peca_utilizada.quant_utilizada.values[0])
            print(nova_peca_utilizada.to_String())
            return nova_peca_utilizada
        else:
            print(f"O conjunto nº {var_codigo} já pertence a um conjunto de peças.")
            return None

    def atualizar_peca_utilizada(self) -> PecaUtilizada:
        oracle = OracleQueries(can_write=True)

        codigo = int(input("Informe o código da peça utilizada que será alterada: "))

        if not self.verifica_existencia_peca_utilizada(oracle, codigo):
            
            ordem_id = int(input("Informe o nº da ordem de serviço que deseja buscar: "))
            ordem_servico = self.valida_ordem_servico(oracle, ordem_id)
            if ordem_servico == None:
                return None
            
            peca_id = int(input("Digite o ID da peca: "))
            peca = self.valida_peca(oracle, peca_id)
            if peca == None:
                return None


            preco_uni = float(input("Informe o novo preço da peça: "))
            quant_utilizada = int(input("Informe a nova quantidade de peças utilizadas: "))

            oracle.write(f"update pecas_utilizadas set peca_utilizada_id = {codigo}, peca_id = {peca_id}, ordem_id = {ordem_id}, preco_uni = {preco_uni}, quant_utilizada = {quant_utilizada} where peca_utilizada_id = {codigo}")

            df_peca_utilizada = oracle.sqlToDataFrame(f"select peca_utilizada_id, peca_id, ordem_id, preco_uni, quant_utilizada from pecas_utilizadas where peca_utilizada_id = {codigo}")

            peca_utilizada_atualizada = PecaUtilizada(df_peca_utilizada.peca_utilizada_id.values[0], peca, ordem_servico,
                                                      df_peca_utilizada.preco_uni.values[0],
                                                      df_peca_utilizada.quant_utilizada.values[0])
            print(peca_utilizada_atualizada.to_String())
            
            return peca_utilizada_atualizada
        else:
            print(f"O código da peça utilizada, {codigo}, não existe")
            return None

    def excluir_peca_utilizada(self) -> PecaUtilizada:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        codigo = int(input("Informe o código da peça utilizada que será excluída: "))

        if not self.verifica_existencia_peca_utilizada(oracle, codigo):

            df_peca_utilizada = oracle.sqlToDataFrame(f"select peca_utilizada_id, peca_id, ordem_id, preco_uni, quant_utilizada from pecas_utilizadas where peca_utilizada_id = {codigo}")

            peca = self.valida_peca(oracle, df_peca_utilizada.peca_id.values[0])
            ordem_servico = self.valida_ordem_servico(oracle, df_peca_utilizada.ordem_id.values[0])

            opcao_excluir = input(f"Tem certeza que deseja excluir a peça utilizada código {codigo} (S|N)? ")

            if opcao_excluir.lower() == "s":

                oracle.write(f"delete from pecas_utilizadas where peca_utilizada_id = {codigo}")

                peca_utilizada_excluida = PecaUtilizada(df_peca_utilizada.peca_utilizada_id.values[0], peca, ordem_servico,
                                                        df_peca_utilizada.preco_uni.values[0],
                                                        df_peca_utilizada.quant_utilizada.values[0])
                print("Peças utilizadas excluídas com sucesso!")
                print(peca_utilizada_excluida.to_String())
            
        else:
            print(f"O código da peça utilizada, {codigo}, não existe")


    def verifica_existencia_peca_utilizada(self, oracle: OracleQueries, codigo: int = None) -> bool:
        df_peca_utilizada = oracle.sqlToDataFrame(f"select peca_utilizada_id, peca_id, ordem_id, preco_uni, quant_utilizada from pecas_utilizadas where peca_utilizada_id = '{codigo}'")
        return df_peca_utilizada.empty

    def listar_pecas(self, oracle: OracleQueries, need_connect: bool = False):
        query = """
                select p.peca_id
                    , p.nome
                    , p.preco_uni
                from LABDATABASE.peca p
                order by p.peca_id
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))

    def listar_ordens_servico(self, oracle: OracleQueries, need_connect: bool = False):
        query = """
                select o.ordem_id
                    , c.cliente_id 
                    , c.nome
                    , t.tecnico_id 
                    , o.data_abertura
                    , o.data_conclusao
                    , o.status_os
                    , o.solucao
                    , o.custo_total
                from LABDATABASE.ordem_servico o
                inner join LABDATABASE.clientes2 c
                on c.CLIENTE_ID = o.CLIENTE_ID
                inner join LABDATABASE.tecnico t
                on t.TECNICO_ID = o.TECNICO_ID
                order by o.ordem_id
                """
        if need_connect:
            oracle.connect()
        print(oracle.sqlToDataFrame(query))

    def valida_peca(self, oracle: OracleQueries, peca_id: int = None) -> Peca:
        if self.ctrl_peca.verifica_existencia_peca(oracle, peca_id):
            print(f"A peça, ID {peca_id}, não existe na base.")
            return None
        else:
            oracle.connect()

            df_peca = oracle.sqlToDataFrame(f"select peca_id, nome, preco_uni from peca where peca_id = '{peca_id}'")

            peca = Peca(df_peca.peca_id.values[0], df_peca.nome.values[0], df_peca.preco_uni.values[0])

            return peca

    def valida_ordem_servico(self, oracle: OracleQueries, ordem_id: int = None) -> OrdemServico:
        if self.ctrl_ordem_servico.verifica_existencia_ordem_servico(oracle, ordem_id):
            print(f"A ordem de serviço nº {ordem_id}, não foi encontrada na base.")
            return None
        else:
            oracle.connect()

            df_ordem_servico = oracle.sqlToDataFrame(f"select ordem_id, cliente_id, tecnico_id, data_abertura, data_conclusao, status_os, solucao, custo_total from ordem_servico where ordem_id = {ordem_id}")
            cliente = self.ctrl_ordem_servico.valida_cliente(oracle, df_ordem_servico.cliente_id.values[0])
            tecnico = self.ctrl_ordem_servico.valida_tecnico(oracle, df_ordem_servico.tecnico_id.values[0])

            ordem_servico = OrdemServico(df_ordem_servico.ordem_id.values[0], cliente, tecnico,
                                         df_ordem_servico.data_abertura.values[0],
                                         df_ordem_servico.data_conclusao.values[0], df_ordem_servico.status_os.values[0],
                                         df_ordem_servico.solucao.values[0], df_ordem_servico.custo_total.values[0])
            return ordem_servico