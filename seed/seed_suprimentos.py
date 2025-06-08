from models.suprimento import Suprimento
from database.connection import connect
import random

TOTAL_SUPRIMENTOS = 500  
BATCH_SIZE = 10000  # Inserção em lotes

def gerar_dados_suprimento(qtd=TOTAL_SUPRIMENTOS):
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

def seed_suprimentos():
    # Gerando e inserindo dados
    connection = connect()
    cursor = connection.cursor()

    try:
        cursor.execute("START TRANSACTION;")
        insert_sql = "INSERT INTO suprimento (nome, descricao) VALUES (%s, %s)"

        buffer = []
        for i, dado in enumerate(gerar_dados_suprimento()):
            buffer.append(dado)
            if len(buffer) == BATCH_SIZE:
                cursor.executemany(insert_sql, buffer)
                print(f"{i+1} registros inseridos...")
                buffer = []

        # Inserir os dados restantes se houver
        if buffer:
            cursor.executemany(insert_sql, buffer)

        connection.commit()
        print("Inserção de suprimentos finalizada com sucesso!")

    except Exception as e:
        connection.rollback()
        print(f"Erro ao inserir dados de suprimento: {e}")
    finally:
        cursor.close()
        connection.close()
