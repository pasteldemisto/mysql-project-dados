from models.exame import Exame
from database.connection import connect
import random
from datetime import datetime, timedelta

TOTAL_EXAMES = 1000
BATCH_SIZE = 10000

def seed_exames():
    # Recuperando os atendimentos existentes
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT codigo_atendimento FROM atendimento")
    atendimentos = [row[0] for row in cursor.fetchall()]

    if not atendimentos:
        print("Você precisa cadastrar atendimentos antes de inserir exames.")
        return

    tipos_exame = ["Sangue", "Urina", "Raio-X", "Tomografia", "Ultrassom"]
    status_exame = ["pendente", "concluído"]
    resultados = ["Normal", "Alterado", "Necessário repetir", "Inconclusivo", "Compatível com diagnóstico"]

    
    total_registros = 0
    for i in range(0, TOTAL_EXAMES, BATCH_SIZE):
        exames_batch = []
        for _ in range(BATCH_SIZE):
            exame = Exame.gerar_exame(atendimentos, tipos_exame, status_exame, resultados)
            exames_batch.append(exame.to_tuple())

        try:
            cursor.execute("START TRANSACTION;")
            sql = """
                INSERT INTO exame (tipo_exame, data_realizacao, exame_status, resultado, codigo_atendimento)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.executemany(sql, exames_batch)
            connection.commit()
            total_registros += cursor.rowcount
            print(f"Batch {i // BATCH_SIZE + 1} inserido com sucesso, total de {total_registros} registros.")
        except Exception as e:
            connection.rollback()
            print("Erro ao inserir exames:", e)
            break

    cursor.close()
    connection.close()

    print(f"Total de {total_registros} exames inseridos com sucesso.")
