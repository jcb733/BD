from utils import config
from utils.splash_screen import SplashScreen
from reports.relatorios import Relatorio
from controller.controller_clientes import ControllerCliente
from controller.controller_ordens_servico import ControllerOrdemServico
from controller.controller_pecas import ControllerPeca
from controller.controller_pecas_utilizadas import ControllerPecaUtilizada
from controller.controller_tecnicos import ControllerTecnico

tela_inicial = SplashScreen()
relatorio = Relatorio()
ctrl_cliente = ControllerCliente()
ctrl_tecnico = ControllerTecnico()
ctrl_peca = ControllerPeca()
ctrl_peca_utilizada = ControllerPecaUtilizada()
ctrl_ordem_servico = ControllerOrdemServico()

def reports(opcao_relatorio:int=0):

    if opcao_relatorio == 1:
        relatorio.get_relatorio_ordem_servico()            
    elif opcao_relatorio == 2:
        relatorio.get_relatorio_pecas_utilizadas()

def inserir(opcao_inserir:int=0):

    if opcao_inserir == 1:                               
        novo_cliente = ctrl_cliente.inserir_cliente()
    elif opcao_inserir == 2:
        novo_tecnico = ctrl_tecnico.inserir_tecnico()
    elif opcao_inserir == 3:
        nova_peca = ctrl_peca.inserir_peca()
    elif opcao_inserir == 4:
        nova_peca_utilizada = ctrl_peca_utilizada.inserir_peca_utilizada()
    elif opcao_inserir == 5:
        nova_ordem_servico = ctrl_ordem_servico.inserir_ordem_servico()

def atualizar(opcao_atualizar:int=0):

    if opcao_atualizar == 1:
        relatorio.get_relatorio_cliente()
        cliente_atualizado = ctrl_cliente.atualizar_cliente()
    elif opcao_atualizar == 2:
        relatorio.get_relatorio_tecnico()
        tecnico_atualizado = ctrl_tecnico.atualizar_tecnico()
    elif opcao_atualizar == 3:
        relatorio.get_relatorio_peca()
        peca_atualizada = ctrl_peca.atualizar_peca()
    elif opcao_atualizar == 4:
        relatorio.get_relatorio_pecas_utilizadas()
        peca_utilizada_atualizado = ctrl_peca_utilizada.atualizar_peca_utilizada()
    elif opcao_atualizar == 5:
        relatorio.get_relatorio_ordem_servico()
        ordem_servico_atualizada = ctrl_ordem_servico.atualizar_ordem_servico()

def excluir(opcao_excluir:int=0):

    if opcao_excluir == 1:
        relatorio.get_relatorio_cliente()
        ctrl_cliente.excluir_cliente()
    elif opcao_excluir == 2:                
        relatorio.get_relatorio_tecnico()
        ctrl_tecnico.excluir_tecnico()
    elif opcao_excluir == 3:                
        relatorio.get_relatorio_peca()
        ctrl_peca.excluir_peca()
    elif opcao_excluir == 4:                
        relatorio.get_relatorio_pecas_utilizadas()
        ctrl_peca_utilizada.excluir_peca_utilizada()
    elif opcao_excluir == 5:
        relatorio.get_relatorio_ordem_servico()
        ctrl_ordem_servico.excluir_ordem_servico()

def run():
    print(tela_inicial.get_updated_screen())
    config.clear_console()

    while True:
        print(config.MENU_PRINCIPAL)
        opcao = int(input("Escolha uma opção [1-5]: "))
        config.clear_console(1)
        
        if opcao == 1: # Relatórios
            
            print(config.MENU_RELATORIOS)
            opcao_relatorio = int(input("Escolha uma opção [1-2]: "))
            config.clear_console(1)

            reports(opcao_relatorio)

            config.clear_console(1)

        elif opcao == 2: # Inserir Novos Registros
            
            print(config.MENU_ENTIDADES)
            opcao_inserir = int(input("Escolha uma opção [1-5]: "))
            config.clear_console(1)

            inserir(opcao_inserir=opcao_inserir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 3: # Atualizar Registros

            print(config.MENU_ENTIDADES)
            opcao_atualizar = int(input("Escolha uma opção [1-5]: "))
            config.clear_console(1)

            atualizar(opcao_atualizar=opcao_atualizar)

            config.clear_console()

        elif opcao == 4:

            print(config.MENU_ENTIDADES)
            opcao_excluir = int(input("Escolha uma opção [1-5]: "))
            config.clear_console(1)

            excluir(opcao_excluir=opcao_excluir)

            config.clear_console()
            print(tela_inicial.get_updated_screen())
            config.clear_console()

        elif opcao == 5:

            print(tela_inicial.get_updated_screen())
            config.clear_console()
            print("Obrigado por utilizar o nosso sistema.")
            exit(0)

        else:
            print("Opção incorreta.")
            exit(1)

if __name__ == "__main__":
    run()