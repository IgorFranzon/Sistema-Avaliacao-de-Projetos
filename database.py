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

#Fecha a conexão com banco de dados#
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close() 
            print("A conexão foi fechada!")


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
      

if __name__ ==  "__main__":
    db = DatabaseConnection()
    db.connect()
    db.close()


        
