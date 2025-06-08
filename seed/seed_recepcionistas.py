from models.recepcionista import Recepcionista
from database.connection import connect

TOTAL_RECEPCIONISTAS = 150

def seed_recepcionistas():
    recepcionistas = [Recepcionista.gerar_recepcionista().to_tuple() for _ in range(TOTAL_RECEPCIONISTAS)]

    connection = connect()
    cursor = connection.cursor()

    try:
        cursor.execute("START TRANSACTION;")
        sql = """
            INSERT INTO recepcionista (cpf, telefone, nome)
            VALUES (%s, %s, %s)
        """
        cursor.executemany(sql, recepcionistas)
        connection.commit()
        print(f"{cursor.rowcount} recepcionistas inseridos com sucesso.")
    except Exception as e:
        connection.rollback()
        print("Erro ao inserir recepcionistas:", e)
    finally:
        cursor.close()
        connection.close()
