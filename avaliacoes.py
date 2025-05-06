from database import DatabaseConnection, Avaliacao

avaliacoes = []

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

    #CONECTA AO BANCO#
    db = DatabaseConnection()
    db.connect()
    avaliacao_crud = Avaliacao(db)

    while True:
        print("\n--- Cadastro de Avaliação ---")
        nome_projeto = ler_texto("Nome do projeto: ")
        qualidade = ler_nota("Nota para qualidade (0-10): ")
        prazo = ler_nota("Nota para prazo (0-10): ")
        inovacao = ler_nota("Nota para inovação (0-10): ")
        comentario = ler_texto("Comentário sobre o projeto: ")

        media = (qualidade + prazo + inovacao) / 3

        avaliacao = {
            "nome": nome_projeto,
            "qualidade": qualidade,
            "prazo": prazo,
            "inovacao": inovacao,
            "comentario": comentario,
            "media": media
        }

        avaliacoes.append(avaliacao)
        print("Avaliação cadastrada com sucesso!")

        #SALVAR NO BANCO DE DADOS#
        avaliacao_crud.create(
            nome_projeto,qualidade,prazo,inovacao,media,comentario
        )

        opcao = input("\nDeseja cadastrar outra avaliação? (s/n): ").lower()
        if opcao != 's':
            break

        #FECHA CONEXAO#
        db.close()

def listar_avaliacoes():
    while True:
        if not avaliacoes:
            print("\nNenhuma avaliação cadastrada.")
            break

        print("\n--- Lista de Avaliações ---")
        for idx, av in enumerate(avaliacoes, start=1):
            print(f"\nAvaliação {idx}:")
            print(f"Projeto: {av['nome']}")
            print(f"Qualidade: {av['qualidade']}")
            print(f"Prazo: {av['prazo']}")
            print(f"Inovação: {av['inovacao']}")
            print(f"Média Final: {av['media']:.2f}")
            print(f"Comentário: {av['comentario']}")

        print("\nPressione qualquer tecla para voltar ao menu principal...")
        input()
        break 

def gerar_relatorio():
    while True:
        if not avaliacoes:
            print("\nNão há avaliações cadastradas ainda.")
            print("Cadastre pelo menos uma avaliação antes de gerar o relatório.")
            break

        else:
            print("\n=== Relatório de Desempenho dos Projetos ===")
            for av in avaliacoes:
                status = "Aprovado" if av["media"] >= 7 else "Reprovado"
                print(f"\nProjeto: {av['nome']}")
                print(f"Média: {av['media']:.2f} - {status}")
                print(f"Comentário: {av['comentario']}")

            print("\nPressione qualquer tecla para voltar ao menu principal...")
            input() 
            break

def main():
    while True:
        print("\n=== Sistema de Avaliação de Projetos ===")
        print("1 - Cadastrar Avaliação")
        print("2 - Listar Avaliações")
        print("3 - Gerar Relatório de Desempenho")
        print("4 - Sair")
        print("5 - Ajuda")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            cadastrar_avaliacao()
        elif opcao == '2':
            listar_avaliacoes()
            db = DatabaseConnection()
            db.connect()
            avaliacao_crud = Avaliacao(db)
            avaliacao_crud.listar_todos()
            db.close()
        elif opcao == '3':
            gerar_relatorio()
            db = DatabaseConnection()
            db.connect()
            avaliacao_crud = Avaliacao(db)
            avaliacao_crud.relatorio_desempenho()
            db.close()
        elif opcao == '4':
            print("Saindo do sistema...")
            break
        elif opcao == '5':
            mostrar_ajuda()
        else:
            print("Opção inválida. Tente novamente.")    

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