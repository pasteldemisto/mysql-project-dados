from models.prescricao import Prescricao
from database.connection import connect
import random

TOTAL_PRESCRICOES = 1000
BATCH_SIZE = 10000

def seed_prescricoes():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT codigo_atendimento FROM atendimento")
    atendimentos = [row[0] for row in cursor.fetchall()]

    if not atendimentos:
        print("Você precisa cadastrar atendimentos antes de inserir prescrições.")
        return

    dosagens = ["1 comprimido", "2 ml", "50 mg", "10 gotas", "1 ampola"]
    duracoes = ["7 dias", "10 dias", "15 dias", "1 mês", "uso contínuo"]

    
    total_registros = 0
    for i in range(0, TOTAL_PRESCRICOES, BATCH_SIZE):
        prescricoes_batch = []
        for _ in range(BATCH_SIZE):
            prescricao = Prescricao.gerar_prescricao(atendimentos, dosagens, duracoes)
            prescricoes_batch.append(prescricao.to_tuple())

        try:
            cursor.execute("START TRANSACTION;")
            sql = """
                INSERT INTO prescricao (dosagem, duracao, codigo_atendimento)
                VALUES (%s, %s, %s)
            """
            cursor.executemany(sql, prescricoes_batch)
            connection.commit()
            total_registros += cursor.rowcount
            print(f"Batch {i // BATCH_SIZE + 1} inserido com sucesso, total de {total_registros} registros.")
        except Exception as e:
            connection.rollback()
            print("Erro ao inserir prescrições:", e)
            break

    cursor.close()
    connection.close()

    print(f"Total de {total_registros} prescrições inseridas com sucesso.")
