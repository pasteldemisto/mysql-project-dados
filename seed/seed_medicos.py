from models.medico import Medico
from database.connection import connect

TOTAL_MEDICOS = 1000
especialidades_fixas = ["Cardiologia", "Ortopedia", "Pediatria"]

def seed_medicos():
    medicos = []

    # Garante pelo menos 50 médicos por especialidade fixa
    for especialidade in especialidades_fixas:
        for _ in range(25):
            medico = Medico.gerar_medico(especialidade)
            medicos.append(medico.to_tuple())

    # Completa o total com especialidades variadas
    while len(medicos) < TOTAL_MEDICOS:
        medico = Medico.gerar_medico()
        medicos.append(medico.to_tuple())

    connection = connect()
    cursor = connection.cursor()

    try:
        cursor.execute("START TRANSACTION;")
        sql = """
            INSERT INTO medico (cpf, crm, nome, especialidade, telefone)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.executemany(sql, medicos)
        connection.commit()
        print(f"{cursor.rowcount} médicos inseridos com sucesso.")
    except Exception as e:
        connection.rollback()
        print("Erro ao inserir médicos:", e)
    finally:
        cursor.close()
        connection.close()
