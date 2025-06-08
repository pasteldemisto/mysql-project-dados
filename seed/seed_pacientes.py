from models.paciente import Paciente
from database.connection import connect

TOTAL_PACIENTES = 8000

def seed_pacientes():
    pacientes = [Paciente.gerar_paciente().to_tuple() for _ in range(TOTAL_PACIENTES)]

    connection = connect()
    cursor = connection.cursor()

    try:
        cursor.execute("START TRANSACTION;")
        sql = """
            INSERT INTO paciente (cpf, dataNascimento, nome, endereco, telefone)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.executemany(sql, pacientes)
        connection.commit()
        print(f"{cursor.rowcount} pacientes inseridos com sucesso.")
    except Exception as e:
        connection.rollback()
        print("Erro ao inserir pacientes: ", e)
    finally:
        cursor.close()
        connection.close()
