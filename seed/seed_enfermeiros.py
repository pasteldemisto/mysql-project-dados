from models.enfermeiro import Enfermeiro
from database.connection import connect

TOTAL_ENFERMEIROS = 200

def seed_enfermeiros():
    enfermeiros = [Enfermeiro.gerar_enfermeiro().to_tuple() for _ in range(TOTAL_ENFERMEIROS)]

    connection = connect()
    cursor = connection.cursor()

    try:
        cursor.execute("START TRANSACTION;")
        sql = """
            INSERT INTO enfermeiro (cpf, coren, nome, telefone)
            VALUES (%s, %s, %s, %s)
        """
        cursor.executemany(sql, enfermeiros)
        connection.commit()
        print(f"{cursor.rowcount} enfermeiros inseridos com sucesso.")
    except Exception as e:
        connection.rollback()
        print("Erro ao inserir enfermeiros:", e)
    finally:
        cursor.close()
        connection.close()
