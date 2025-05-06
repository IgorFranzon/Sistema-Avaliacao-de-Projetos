import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

#Pega Os dados do arquivo .env para facilitar#
load_dotenv()


class DatabaseConnection:
    def __init__(self):
        
        #Carrega as configurações diretamente das varaiavesi de ambiente#
        self.host = os.getenv('DB_HOST')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.database = os.getenv('DB_DATABASE')
        self.connection = None
        self.cursor = None
    
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database = self.database
            )
            self.cursor = self.connection.cursor()
            print(f"Conexão estabelecida com sucesso!")
        except Error as e:
            print(f"Conexão não foi estabelecida error!: {e}")



class Avaliacao:
    def __init__(self,db_connection):
        self.db_connection = db_connection

    def create(self,nome_projeto, qualidade, prazo, inovacao, media, comentario):
        try: 
            sql = """insert into Avaliacao(nome_projeto, qualidade, prazo, inovacao, media, comentario)
            values (%s,%s,%s,%s,%s,%s)"""

            values = (nome_projeto, qualidade, prazo, inovacao, media, comentario)
            self.db_connection.cursor.execute(sql,values)
            self.db_connection.connection.commit()
            print(f"Avaliação do projeto {nome_projeto} salvo com sucesso no Banco de dados ")
        except Error as e:
            print("Erro a salvar avaliação: {e}")
            self.db_connection.connection.rollback()

    def listar_todos(self):
        try:
            sql = "SELECT nome_projeto, qualidade, prazo, inovacao, media, comentario FROM Avaliacao"
            self.db_connection.cursor.execute(sql)
            resultados = self.db_connection.cursor.fetchall()
            print("\n=== Avaliações ===")
            for idx, row in enumerate(resultados, start=1):
                print(f"\nAvaliação {idx}:")
                print(f"Projeto: {row[0]}")
                print(f"Qualidade: {row[1]}")
                print(f"Prazo: {row[2]}")
                print(f"Inovação: {row[3]}")
                print(f"Média Final: {row[4]:.2f}")
                print(f"Comentário: {row[5]}")
        except Error as e:
            print(f"Erro ao buscar avaliações: {e}")

    def relatorio_desempenho(self):
        try:
            sql = "SELECT nome_projeto, media, comentario FROM Avaliacao"
            self.db_connection.cursor.execute(sql)
            resultados = self.db_connection.cursor.fetchall()
            
            if not resultados:
                print("\nNenhum projeto encontrado no banco de dados.")
                return

            print("\n=== Relatório de Desempenho dos Projetos ===")
            for projeto in resultados:
                nome, media, comentario = projeto
                status = "Aprovado" if media >= 7 else "Reprovado"
                print(f"\nProjeto: {nome}")
                print(f"Média: {media:.2f} - {status}")
                print(f"Comentário: {comentario}")
        except Error as e:
            print(f"Erro ao gerar relatório: {e}")

#Fecha a conexão com banco de dados#
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close() 
            print("A conexão foi fechada!")
            
if __name__ ==  "__main__":
    db = DatabaseConnection()
    db.connect()
    db.close()


        
