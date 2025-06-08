from models.medicamento import Medicamento
from database.connection import connect
import random

TOTAL_MEDICAMENTOS = 500
BATCH_SIZE = 10000

def seed_medicamentos():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT codigo_prescricao FROM prescricao")
    prescricoes = [row[0] for row in cursor.fetchall()]

    if not prescricoes:
        print("Você precisa cadastrar prescrições antes de inserir medicamentos.")
        return

    fabricantes = ["EMS", "Medley", "Eurofarma", "Aché", "Hypera", "Neo Química", "Bayer"]

    total_registros = 0
    for i in range(0, TOTAL_MEDICAMENTOS, BATCH_SIZE):
        medicamentos_batch = []
        for _ in range(BATCH_SIZE):
            medicamento = Medicamento.gerar_medicamento(prescricoes, fabricantes)
            medicamentos_batch.append(medicamento.to_tuple())

        try:
            cursor.execute("START TRANSACTION;")
            sql = """
                INSERT INTO medicamento (fabricante, data_validade, lote, codigo_prescricao, telefone)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.executemany(sql, medicamentos_batch)
            connection.commit()
            total_registros += cursor.rowcount
            print(f"Batch {i // BATCH_SIZE + 1} inserido com sucesso, total de {total_registros} registros.")
        except Exception as e:
            connection.rollback()
            print("Erro ao inserir medicamentos:", e)
            break

    cursor.close()
    connection.close()

    print(f"Total de {total_registros} medicamentos inseridos com sucesso.")
