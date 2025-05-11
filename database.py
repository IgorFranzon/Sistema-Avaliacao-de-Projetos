import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, host="localhost", user="root", password="Ar@58425873", database="avaliacao_de_projetos"):
        self.config = {
            'host': host,
            'user': user,
            'password': password,
            'database': database
        }
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print("Conexão ao MySQL estabelecida com sucesso!")
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()

    def cadastrar_avaliacao(self, nome_projeto, qualidade, prazo, inovacao, comentario):
        try:
            media = (qualidade + prazo + inovacao) / 3
            query = """
                INSERT INTO Avaliacao (nome_projeto, qualidade, prazo, inovacao, comentario, media)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (nome_projeto, qualidade, prazo, inovacao, comentario, media)
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            print("Avaliação cadastrada com sucesso!")
            return True
        except Error as e:
            print(f"Erro ao cadastrar avaliação: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

    def verificar_projeto_existente(self, nome_projeto):
        try:
            query = "SELECT COUNT(*) FROM Avaliacao WHERE nome_projeto = %s"
            cursor = self.connection.cursor()
            cursor.execute(query, (nome_projeto,))
            count = cursor.fetchone()[0]
            return count > 0
        except Error as e:
            print(f"Erro ao verificar projeto: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

    def listar_avaliacoes(self):
        try:
            query = "SELECT * FROM Avaliacao"
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query)
            avaliacoes = cursor.fetchall()
            return avaliacoes
        except Error as e:
            print(f"Erro ao listar avaliações: {e}")
            return []
        finally:
            if cursor:
                cursor.close()

    def gerar_relatorio_por_id(self, id_avaliacao):
        try:
            query = "SELECT * FROM Avaliacao WHERE id_avaliacao = %s"
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, (id_avaliacao,))
            avaliacao = cursor.fetchone()
            return avaliacao
        except Error as e:
            print(f"Erro ao gerar relatório: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
