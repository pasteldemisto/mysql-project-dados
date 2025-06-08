from models.estoque_medicamento import EstoqueMedicamento
from database.connection import connect
import random

def seed_estoque_medicamentos():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT codigo_medicamento, lote FROM medicamento")
    medicamentos = cursor.fetchall()

    if not medicamentos:
        print("É necessário ter medicamentos cadastrados antes de popular o estoque.")
        return

    # Gerando dados para o estoque
    dados_estoque = []
    for codigo_medicamento, lote in medicamentos:
        quantidade = random.randint(5, 100)  # Quantidade entre 5 e 100
        dados_estoque.append((codigo_medicamento, quantidade, lote))

    
    try:
        cursor.execute("START TRANSACTION;")
        sql = """
            INSERT INTO estoque_medicamento (codigo_medicamento, quantidade, lote)
            VALUES (%s, %s, %s)
        """
        cursor.executemany(sql, dados_estoque)
        connection.commit()
        print(f"{len(dados_estoque)} registros de estoque de medicamentos inseridos com sucesso!")
    except Exception as e:
        connection.rollback()
        print("Erro ao popular estoque de medicamentos:", e)
    finally:
        cursor.close()
        connection.close()