from models.estoque_suprimento import EstoqueSuprimento
from database.connection import connect
import random

def seed_estoque_suprimentos():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT codigo_suprimento, nome FROM suprimento LIMIT 1000")
    suprimentos = cursor.fetchall()

    if not suprimentos:
        print("É necessário ter suprimentos cadastrados antes de popular o estoque.")
        return


    dados_estoque = []
    lotes = [f"LOTE-{random.randint(1000, 9999)}" for _ in range(len(suprimentos))]

    for codigo_suprimento, nome in suprimentos:
        quantidade = random.randint(10, 200)  # Quantidade entre 10 e 200
        lote = random.choice(lotes)
        dados_estoque.append((codigo_suprimento, quantidade, lote))

    
    try:
        cursor.execute("START TRANSACTION;")
        sql = """
            INSERT INTO estoque_suprimento (codigo_suprimento, quantidade, lote)
            VALUES (%s, %s, %s)
        """
        cursor.executemany(sql, dados_estoque)
        connection.commit()
        print(f"{len(dados_estoque)} registros de estoque de suprimentos inseridos com sucesso!")
    except Exception as e:
        connection.rollback()
        print("Erro ao popular estoque de suprimentos:", e)
    finally:
        cursor.close()
        connection.close()