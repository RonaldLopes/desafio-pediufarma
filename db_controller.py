from datetime import date
import mysql.connector
from mysql.connector import errorcode

class DatabaseController:
    def __init__(self,user,password,database='desafio'):
        try:
            self.nome_database = database
            self.db_connection = mysql.connector.connect(host='localhost', user=user, password=password, database=database)
            print("Conexão com o banco realizada")
        except mysql.connector.Error as error:
            if error.errno == errorcode.ER_BAD_DB_ERROR:
                print("Banco de dados inexistente")
                # self.db_connection = mysql.connector.connect(host='localhost', user=user, password=password,)
                # print('Criando um novo banco de dados com nome: %s'%(database))
                # self.cria_database(nome_database=database)
                self.__init__(user,password,database)
            elif error.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Usuario ou senha invalidos!")
            else:
                print(error)

    def cria_database(self,nome_database):

        cursor = self.db_connection.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS %s;'%(nome_database))
        cursor.execute('USE %s;'%(nome_database))
        print('Banco criado com sucesso')

    def busca_estoque(self):
        cursor = self.db_connection.cursor()
        str = ('''
        SELECT CASE
        WHEN validade is null THEN pmc
        WHEN promocao is null THEN pmc
        WHEN validade > curdate() THEN promocao
        WHEN validade = curdate() THEN promocao
        WHEN validade < curdate() THEN IF(pmc is null, promocao, pmc)
        END AS preco_final, barra, quantidade FROM desafio.estoque where quantidade>0 and pmc is not null; 
        ''')
        cursor.execute(str)
        media = cursor.fetchall()
        cursor.close()
        return media



