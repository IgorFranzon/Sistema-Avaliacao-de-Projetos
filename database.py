import mysql.connector
from mysql.connector import Error

def padronizar_nome_projeto(nome):
    # Converter para minúsculas
    nome = nome.lower()
    # Remover espaços e caracteres não alfanuméricos
    nome = ''.join(c for c in nome if c.isalnum())
    return nome

class Database:
    def __init__(self, host="localhost", user="root", password="sua_senha", database="nome_do_BD"):
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
            if not self.connection.is_connected():
                raise Error("Falha ao verificar conexão com Mysql")
        except Error as e:
            print(f"Erro ao conectar ao MySQL: {e}")
            self.connection = None 
            raise

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
            nome_projeto_padronizado = padronizar_nome_projeto(nome_projeto)
            query = """SELECT COUNT(*) 
            FROM Avaliacao 
            WHERE REGEXP_REPLACE(LOWER(nome_projeto), '[^a-z0-9]', '') = %s"""
            cursor = self.connection.cursor()
            cursor.execute(query, (nome_projeto_padronizado,))
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

    def salvar_relatorio(self, id_avaliacao, conteudo_relatorio):
        try:
            query = """INSERT INTO Relatorios (id_avaliacao, conteudo_relatorio)
                       VALUES (%s, %s)"""
            values = (id_avaliacao, conteudo_relatorio)
            cursor = self.connection.cursor()
            cursor.execute(query, values)
            self.connection.commit()
            return True
        except Error as e:
            print(f"Erro ao salvar relatório: {e}")
            return False
        finally:
            if cursor is not None:
                cursor.close()            

    def listar_relatorio(self, id_avaliacao):
        try:
            query = """SELECT id_relatorio, id_avaliacao, conteudo_relatorio,data_geracao
            FROM Relatorios
            WHERE id_avaliacao = %s
            ORDER BY data_geracao DESC
            """
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, (id_avaliacao,))
            relatorios = cursor.fetchall()
            return relatorios
        except Error as e:
            print(f"Erro ao listar relatórios: {e}")
            return []
        finally:
            if cursor is not None:
                cursor.close()

    def verificar_relatorio_existente(self, id_avaliacao):
        try:
            query = "SELECT COUNT(*) FROM Relatorios WHERE id_avaliacao = %s"
            cursor = self.connection.cursor()
            cursor.execute(query, (id_avaliacao,))
            count = cursor.fetchone()[0]
            return count > 0
        except Error as e:
            print(f"Erro ao verificar relatório: {e}")
            return False
        finally:
            if cursor:
                cursor.close()

    def verificar_credenciais(self, RM, senha):
        try:
            query = "SELECT id_usuario FROM Usuario WHERE RM = %s AND senha = %s"
            cursor = self.connection.cursor()
            cursor.execute(query, (RM,senha))
            usuario = cursor.fetchone()
            return usuario is not None
        except Error as e:
            print(f"Erro ao verificar credenciais: {e}")
            return False
        finally: 
            if cursor:
                cursor.close()