from conexion.oracle_queries import OracleQueries
from model.tecnicos import Tecnico


class ControllerTecnico:
    def __init__(self):
        pass

    def inserir_tecnico(self) -> Tecnico:

        oracle = OracleQueries(can_write=True)
        oracle.connect()

        tecnico_id = int(input("Informe o ID do técnico que será cadastrado: "))

        if self.verifica_existencia_tecnico(oracle, tecnico_id):
            nome = input("Nome: ")
            especialidade = input("Especialidade: ")
            email = input("E-mail: ")
            telefone = input("Telefone: ")

            oracle.write(f"insert into tecnico values('{tecnico_id}', '{nome}', '{especialidade}', '{email}', '{telefone}')")

            df_tecnico = oracle.sqlToDataFrame(f"select tecnico_id, nome, especialidade, email, telefone from tecnico where tecnico_id = '{tecnico_id}'")

            novo_tecnico = Tecnico(df_tecnico.tecnico_id.values[0], df_tecnico.nome.values[0], df_tecnico.especialidade.values[0], df_tecnico.email.values[0], df_tecnico.telefone.values[0])

            print(novo_tecnico.to_String())

            return novo_tecnico
        else:
            print(f"O ID {tecnico_id} já está cadastrado para um técnico.")
            return None

    def atualizar_tecnico(self) -> Tecnico:

        oracle = OracleQueries(can_write=True)
        oracle.connect()

        tecnico_id = int(input("Informe o ID do técnico que terá os dados atualizados: "))

        if not self.verifica_existencia_tecnico(oracle, tecnico_id):
            novo_nome = input("Novo nome: ")
            nova_especialidade = input("Atualização de especialidade: ")
            novo_email = input("Novo e-mail: ")
            novo_telefone = input("Novo telefone: ")

            oracle.write(f"update tecnico set nome = '{novo_nome}', especialidade = '{nova_especialidade}', email = '{novo_email}', telefone = '{novo_telefone}' where tecnico_id = {tecnico_id}")

            df_tecnico = oracle.sqlToDataFrame(f"select tecnico_id, nome, especialidade, email, telefone from tecnico where tecnico_id = '{tecnico_id}'")

            altercao_tecnico = Tecnico(df_tecnico.tecnico_id.values[0], df_tecnico.nome.values[0],
                                   df_tecnico.especialidade.values[0], df_tecnico.email.values[0],
                                   df_tecnico.telefone.values[0])

            print(altercao_tecnico.to_String())

            return altercao_tecnico
        else:
            print(f"O ID {tecnico_id} não foi encontrado em sistema para atualização.")
            return None

    def excluir_tecnico(self):

        oracle = OracleQueries(can_write=True)
        oracle.connect()

        tecnico_id = int(input("Informe o ID do técnico que terá os dados excluídos: "))

        if not self.verifica_existencia_tecnico(oracle, tecnico_id):

            df_tecnico = oracle.sqlToDataFrame(f"select tecnico_id, nome, especialidade, email, telefone from tecnico where tecnico_id = '{tecnico_id}'")

            oracle.write(f"delete from tecnico where tecnico_id = {tecnico_id}")

            tecnico_excluido = Tecnico(df_tecnico.tecnico_id.values[0], df_tecnico.nome.values[0],
                                       df_tecnico.especialidade.values[0], df_tecnico.email.values[0],
                                       df_tecnico.telefone.values[0])

            print("Tecnico excluído com sucesso!")
            print(tecnico_excluido.to_String())

        else:
            print(f"O ID {tecnico_id} não foi encontrado em sistema para exclusão.")

    def verifica_existencia_tecnico(self, oracle: OracleQueries, tecnico_id: int = None)-> bool:
        df_tecnico = oracle.sqlToDataFrame(f"select tecnico_id, nome, especialidade, email, telefone from tecnico where tecnico_id = '{tecnico_id}'")
        return df_tecnico.empty