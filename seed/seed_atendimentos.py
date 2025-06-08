from models.atendimento import Atendimento
from database.connection import connect
import random
from datetime import datetime, timedelta

TOTAL_ATENDIMENTOS = 1000000
BATCH_SIZE = 10000  # Inserção em lotes de 10.000 registros por vez

def seed_atendimentos():
    # Recuperando os IDs de médicos, pacientes, recepcionistas e setores
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT codigo_medico FROM medico")
    medicos = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT codigo_paciente FROM paciente")
    pacientes = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT codigo_recepcionista FROM recepcionista")
    recepcionistas = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT codigo_setor FROM setor")
    setores = [row[0] for row in cursor.fetchall()]

    if not medicos or not pacientes or not recepcionistas or not setores:
        print("Você precisa cadastrar médicos, pacientes, recepcionistas e setores antes de popular atendimentos.")
        return

    diagnosticos = [
        "Hipertensão arterial", "Diabetes mellitus tipo 2", "Asma brônquica",
        "Infecção urinária", "Gripe comum", "Fratura do punho",
        "Cefaleia tensional", "Gastrite aguda", "Otite média", "Dengue"
    ]

    # Gerando atendimentos em lotes
    total_registros = 0
    for i in range(0, TOTAL_ATENDIMENTOS, BATCH_SIZE):
        atendimentos_batch = []
        for _ in range(BATCH_SIZE):
            atendimento = Atendimento.gerar_atendimento(medicos, pacientes, recepcionistas, setores, diagnosticos)
            atendimentos_batch.append(atendimento.to_tuple())
        
        try:
            cursor.execute("START TRANSACTION;")
            sql = """
                INSERT INTO atendimento (codigo_medico, codigo_paciente, codigo_recepcionista, codigo_setor, diagnostico, dataHora)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.executemany(sql, atendimentos_batch)
            connection.commit()
            total_registros += cursor.rowcount
            print(f"Batch {i//BATCH_SIZE + 1} inserido com sucesso, total de {total_registros} registros.")
        except Exception as e:
            connection.rollback()
            print("Erro ao inserir atendimentos: ", e)
            break

    cursor.close()
    connection.close()

    print(f"Total de {total_registros} atendimentos inseridos com sucesso.")
