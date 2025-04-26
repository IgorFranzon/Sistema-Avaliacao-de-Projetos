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
    print("\n--- Cadastra de Avaliação ---")
    nome_projeto = ler_texto("Nome do projeto: ")
    qualidade = ler_nota("Nota para qualidade (0-10): ")
    prazo = ler_nota("Nota para prazo (0-10): ")
    inovacao = ler_nota("Nota para inovação (0-10): ")
    comentario = ler_texto("Comentário sobre o projeto: ")

    media = (qualidade + prazo + inovacao)/3

    avaliacao = {
        "nome": nome_projeto,
        "qualidade": qualidade,
        "prazo": prazo,
        "inovacao": inovacao,
        "comentario": comentario,
        "media": media
    }

    avaliacoes.append(avaliacao)
    print("Avaliação cadastra com sucesso!")

def listar_avaliacoes():
    if not avaliacoes:
        print("\nNenhuma avaliação cadastrada.")
        return
    
    print("\n--- Lista de Avaliações ---")
    for idx, av in enumerate(avaliacoes, start=1):
        print(f"\nAvaliação {idx}:")
        print(f"Projeto: {av['nome']}")
        print(f"Qualidade: {av['qualidade']}")
        print(f"Prazo: {av['prazo']}")
        print(f"Inovação: {av['inovacao']}")
        print(f"Média Final: {av['media']:.2f}")
        print(f"Comentário: {av['comentario']}")

def gerar_relatorio():
    if not avaliacoes:
        print("\nNão há avaliações cadastradas ainda.")
        print("Cadastre pelo menos uma avaliação antes de gerar o relatório.")
        return

    print("\n=== Relatório de Desempenho dos Projetos ===")
    for av in avaliacoes:
        status = "Aprovado" if av["media"] >= 7 else "Reprovado"
        print(f"\nProjeto: {av['nome']}")
        print(f"Média: {av['media']:.2f} - {status}")
        print(f"Comentário: {av['comentario']}")

def main():
    while True:
        print("\n=== Sistema de Avaliação de Projetos ===")
        print("1 - Cadastrar Avaliação")
        print("2 - Listar Avaliações")
        print("3 - Gerar Relatório de Desempenho")
        print("4 - Sair")
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
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()