#conexão BD
from database import Database

db = Database()

def ler_nota(mensagem):
    while True:
        try:
            nota = float(input(mensagem))
            if 0 <= nota <= 10:
                return nota
            else:
                print("A nota deve estar entre 0 e 10.")
        except ValueError:
            print("Digite um número válido.")



def ler_texto(mensagem):
    while True:
        texto = input(mensagem).strip()
        if texto:
            return texto
        else:
            print("Este campo é obrigatório.")


def cadastrar_avaliacao():
    while True:
        print("\n--- Cadastro de Avaliação ---")
        nome_projeto = ler_texto("Nome do projeto: ")
        
        # Verificar se o projeto já existe
        if db.verificar_projeto_existente(nome_projeto):
            print(f"\nJá existe uma avaliação para o projeto '{nome_projeto}'.")
            while True:
                resposta = input("\n Deseja tentar outro nome? (S/N): ").strip().upper()
                if resposta in ('S', 'N'):
                    break
                print("\n Por favor, digite apenas 'S' ou 'N'.")
            if resposta == 'N':
                break
            continue

        qualidade = ler_nota("Nota para qualidade (0-10): ")
        prazo = ler_nota("Nota para prazo (0-10): ")
        inovacao = ler_nota("Nota para inovação (0-10): ")
        comentario = ler_texto("Comentário sobre o projeto: ")
        
        if db.cadastrar_avaliacao(nome_projeto, qualidade, prazo, inovacao, comentario):

            while True:
                resposta = input("\n Você gostaria de cadastrar um novo projeto? (S/N): ").strip().upper()
                if resposta in ('S', 'N'):
                    break
                print("\n Por favor, digite apenas 'S' ou 'N'.")
        
            if resposta == 'N':
                break

#Tela de Login
def tela_login():
    print("\n=== Tela de Login ===")
    tentativas = 3

    while tentativas > 0:
        RM = input("RM(Usuário): ").strip()
        senha = input("Senha (mínimo 8 caracteres): ").strip()

        # Validar o tamanho da senha
        if len(senha) < 8:
            print("A senha deve ter pelo menos 8 caracteres.")
            tentativas -= 1
            print(f"Tentativas restantes: {tentativas}")
            continue
        elif len(senha) > 12:
            print("A senha não pode ter mais de 12 caracteres.")

        if db.verificar_credenciais(RM, senha):
            print(f"\n Login bem-sucedido! Bem-vindo(a), Administrador.")
            return True
        else:
            tentativas -= 1
            print(f"RM ou senha incorretos. Tentativas restantes: {tentativas}")
    
    print("\nVocê excedeu o número de tentativas. Encerrando o sistema.")
    return False


def listar_avaliacoes():
        avaliacoes = db.listar_avaliacoes()

        if not avaliacoes:
            print("\nNenhuma avaliação cadastrada.")
            return

        print("\n--- Lista de Avaliações ---")
        for av in avaliacoes:
            status = "Aprovado" if av['media'] >= 7 else "Reprovado"
            print(f"\nAvaliação: {av['id_avaliacao']}")
            print(f"Projeto: {av['nome_projeto']}")
            print(f"Qualidade: {av['qualidade']}")
            print(f"Prazo: {av['prazo']}")
            print(f"Inovação: {av['inovacao']}")
            print(f"Média Final: {av['media']:.2f}")
            print(f"Comentário: {av['comentario']}")
            print(f"Status: {status}")
        
        input("\n Pressione Enter para voltar ao menu principal")


def gerar_relatorio():
    while True:
        print("\n--- Gerar ou Consultar Relatório ---")
        print("O que você deseja fazer?")
        print("1 - Gerar um novo relatório")
        print("2 - Consultar relatórios salvos")
        print("0 - Voltar ao menu principal")
        escolha = input("\nDigite 1, 2 ou 0: ").strip()

        if escolha == '0':
            break
        elif escolha == '1':  # Gerar novo relatório
            while True:
                id_avaliacao = ler_texto("\nDigite o ID da avaliação para o relatório: ")
                try:
                    id_avaliacao = int(id_avaliacao)
                    avaliacao = db.gerar_relatorio_por_id(id_avaliacao)
                    if not avaliacao:
                        print(f"\nNenhuma avaliação encontrada com ID {id_avaliacao}.")
                        while True:
                            resposta = input("\nDeseja tentar outro ID? S/N: ").strip().upper()
                            if resposta in ('S','N'):
                                break
                            print("\n Porfavor, digite apenas 'S' ou 'N'")
                        if resposta == 'N':
                            break
                        continue
                    

                # Verificar se já existe um relatório para este id_avaliacao
                    if db.verificar_relatorio_existente(id_avaliacao):
                        print(f"\nJá existe um relatório para a avaliação com ID {id_avaliacao}.")
                        while True:
                            resposta = input("\nDeseja tentar outro ID? S/N: ").strip().upper()
                            if resposta in ('S','N'):
                                break
                            print("\nPor favor, digite apenas 'S' ou 'N'")
                        if resposta == 'N':
                            break
                        continue

                    status = "Aprovado" if avaliacao['media'] >= 7 else "Reprovado"
                
                    conteudo_relatorio = (
                    f"\n=== Relatório de Desempenho do Projeto ===\n"
                    f"\nAvaliação: {avaliacao['id_avaliacao']}\n"
                    f"Projeto: {avaliacao['nome_projeto']}\n"
                    f"Qualidade: {avaliacao['qualidade']}\n"
                    f"Prazo: {avaliacao['prazo']}\n"
                    f"Inovação: {avaliacao['inovacao']}\n"
                    f"Comentário: {avaliacao['comentario']}\n"
                    f"Média: {avaliacao['media']:.2f} - {status}\n"
                    )

                    print ("\n" + conteudo_relatorio)
                    db.salvar_relatorio(id_avaliacao, conteudo_relatorio)
                    print("Relatório salvo com sucesso!")
                    input("\nPressione Enter para voltar ao menu principal")
                    break
                except ValueError:
                    print("ID inválido. Digite um ID válido.")
                    while True:
                        resposta = input("\nDeseja tentar outro ID? S/N:  ").strip().upper()
                        if resposta in ('S', 'N'):
                            break
                        print("\nPor favor, digite apenas 'S' ou 'N'.")
                    if resposta == 'N':
                        break
                    continue
            continue
    
        elif escolha == '2':  # Consultar relatórios salvos
            id_avaliacao = ler_texto("\nDigite o ID da avaliação para listar os relatórios salvos: ")
            try:
                id_avaliacao = int(id_avaliacao)
                relatorios = db.listar_relatorio(id_avaliacao)
                if not relatorios:
                    print(f"\nNenhum relatório encontrado para a avaliação com ID {id_avaliacao}.")
                    input("\nPressione Enter para tentar novamente")
                    continue

                print(f"\n--- Relatórios Salvos para Avaliação ID {id_avaliacao} ---")
                for relatorio in relatorios:
                    print(f"\nRelatório ID: {relatorio['id_relatorio']}")
                    print(f"Data de Geração: {relatorio['data_geracao']}")
                    print(relatorio['conteudo_relatorio'])
                    print("-" * 40)

                input("\nPressione Enter para voltar ao menu principal")
            except ValueError:
                print("ID inválido. Digite um ID válido.")
                input("\nPressione Enter para tentar novamente")
                continue
        else:
            print("Opção inválida. Digite 1, 2 ou 0.")
            input("\nPressione Enter para tentar novamente")
            continue

def main():
    if not tela_login():
        return

    try:
        while True:
            print("\n=== Sistema de Avaliação de Projetos ===")
            print("1 - Cadastrar Avaliação")
            print("2 - Listar Avaliações")
            print("3 - Gerar ou Consultar Relatório de Desempenho")
            print("4 - Sair")
            print("5 - Ajuda")
            opcao = input("Escolha uma opção: ")

            if opcao == '1':
                cadastrar_avaliacao()
            elif opcao == '2':
                listar_avaliacoes()
            elif opcao == '3':
                gerar_relatorio()
            elif opcao == '4':
                print("Saindo do sistema...")
                break
            elif opcao == '5':
                mostrar_ajuda()
            else:
                print("Opção inválida. Tente novamente.")
    finally:
        db.disconnect()     

def mostrar_ajuda():
    print("\n=== Guia de Ajuda ===")
    print("""
Este sistema permite avaliar projetos com base em critérios objetivos e comentários subjetivos.
A seguir, veja o que cada opção do menu faz:

1 - Cadastrar Avaliação:
    Permite inserir uma nova avaliação para um projeto.
    O sistema pedirá:
      - Nome do projeto
      - Notas de Qualidade, Prazo e Inovação (0 a 10)
      - Comentário geral
    Após o cadastro, a média será calculada automaticamente.

2 - Listar Avaliações:
    Exibe todas as avaliações cadastradas até o momento, com suas respectivas notas, comentários e média final.
    Pressione qualquer tecla para voltar ao menu principal.

3 - Gerar Relatório de Desempenho:
    Gera um relatório com a média de cada projeto e seu status (Aprovado ou Reprovado).
    Apenas disponível se houver avaliações registradas.
    Pressione qualquer tecla para voltar ao menu principal.

4 - Sair:
    Encerra o programa.

5 - Ajuda:
    Mostra esta tela com informações sobre as funcionalidades do sistema.
""")
    input("Pressione qualquer tecla para voltar ao menu principal...")

if __name__ == "__main__":
    main()