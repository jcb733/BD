from conexion.oracle_queries import OracleQueries
from model.clientes import Cliente

class ControllerCliente:
    def __init__(self):
        pass

    def inserir_cliente(self) -> Cliente:

        oracle = OracleQueries(can_write=True)
        oracle.connect()

        var_cliente_id = int(input("Informe o ID do novo cliente: "))

        if self.verifica_existencia_cliente(oracle, var_cliente_id):
            nome = input("Nome: ")
            endereco = input("Endereço: ")
            email = input("E-mail: ")
            telefone = input("Telefone: ")

            oracle.write(f"insert into clientes2 values('{var_cliente_id}', '{nome}', '{endereco}', '{email}', '{telefone}')")

            df_cliente = oracle.sqlToDataFrame(f"select cliente_id, nome, endereco, email, telefone from clientes2 where cliente_id = '{var_cliente_id}'")

            novo_cliente = Cliente(df_cliente.cliente_id.values[0], df_cliente.nome.values[0], df_cliente.endereco.values[0], df_cliente.email.values[0], df_cliente.telefone.values[0])

            print(novo_cliente.to_String())

            return novo_cliente
        else:
            print(f"O ID {var_cliente_id} já pertence a um cliente")
            return None

    def atualizar_cliente(self) -> Cliente:
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        var_cliente_id = int(input("Informe o ID do cliente que terá os dados alterados: "))

        if not self.verifica_existencia_cliente(oracle, var_cliente_id):
            novo_nome = input("Novo nome: ")
            novo_endereco = input("Novo endereço: ")
            novo_email = input("Novo e-mail: ")
            novo_telefone = input("Novo telefone: ")

            oracle.write(f"update clientes2 set nome = '{novo_nome}', endereco = '{novo_endereco}', email = '{novo_email}', telefone = '{novo_telefone}' where cliente_id = {var_cliente_id}")

            df_cliente = oracle.sqlToDataFrame(f"select cliente_id, nome, endereco, email, telefone from clientes2 where cliente_id = '{var_cliente_id}'")

            alteracao_cliente = Cliente(df_cliente.cliente_id.values[0], df_cliente.nome.values[0],
                                        df_cliente.endereco.values[0], df_cliente.email.values[0],
                                        df_cliente.telefone.values[0])

            print(alteracao_cliente.to_String())

            return alteracao_cliente
        else:
            print(f"O ID {var_cliente_id} não foi encontrado para ser atualizado.")
            return None

    def excluir_cliente(self):
        oracle = OracleQueries(can_write=True)
        oracle.connect()

        var_cliente_id = int(input("ID do cliente que deseja excluir: "))

        if not self.verifica_existencia_cliente(oracle, var_cliente_id):
            df_cliente = oracle.sqlToDataFrame(f"select cliente_id, nome, endereco, email, telefone from clientes2 where cliente_id = '{var_cliente_id}'")

            oracle.write(f"delete from clientes2 where cliente_id = {var_cliente_id}")

            cliente_excluido = Cliente(df_cliente.cliente_id.values[0], df_cliente.nome.values[0], df_cliente.endereco.values[0], df_cliente.email.values[0], df_cliente.telefone.values[0])
            print("Cliente removido com sucesso")
            print(cliente_excluido.to_String())
        else:
            print(f"O ID {var_cliente_id} não foi encontrado para exclusão.")

    def verifica_existencia_cliente(self, oracle: OracleQueries, var_cliente_id: int = None) -> bool:
        df_cliente = oracle.sqlToDataFrame(f"select cliente_id, nome, endereco, email, telefone from clientes2 where cliente_id = '{var_cliente_id}'")
        return df_cliente.empty