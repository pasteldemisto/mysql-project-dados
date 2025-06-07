from database.connection import connect

# Conectando ao mysql
#connection = connect()

import mysql.connector
from mysql.connector import Error
import random


def connect_to_db():
    try:
        connection = connect()
        return connection
    except Error as e:
        print(f"Erro de conexão: {e}")
        return None

def gerar_dados_suprimento(qtd=1_000_000):
    nomes_base = [
        ("Seringa descartável", "Usada para aplicações intravenosas ou intramusculares"),
        ("Luvas cirúrgicas", "Utilizadas em procedimentos médicos para proteção"),
        ("Máscara N95", "Máscara de alta proteção contra partículas"),
        ("Álcool em gel", "Higienização das mãos"),
        ("Gaze estéril", "Utilizada para curativos e absorção de sangue"),
        ("Esparadrapo", "Fixa curativos na pele"),
        ("Soro fisiológico", "Solução salina para limpeza de feridas ou diluições"),
        ("Termômetro digital", "Mede a temperatura corporal"),
        ("Avental descartável", "Usado por profissionais em ambiente estéril"),
        ("Touca cirúrgica", "Cobertura descartável para os cabelos")
    ]
    for i in range(qtd):
        nome, descricao = random.choice(nomes_base)
        yield (f"{nome}", descricao)

def popular_suprimentos():
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("START TRANSACTION;")
            insert_sql = "INSERT INTO suprimento (nome, descricao) VALUES (%s, %s)"

            batch_size = 10000
            buffer = []

            for i, dado in enumerate(gerar_dados_suprimento()):
                buffer.append(dado)
                if len(buffer) == batch_size:
                    cursor.executemany(insert_sql, buffer)
                    print(f"{i+1} registros inseridos...")
                    buffer = []

            if buffer:
                cursor.executemany(insert_sql, buffer)

            connection.commit()
            print("Inserção finalizada com sucesso!")
        except Error as e:
            print(f"Erro ao inserir dados: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

popular_suprimentos()
