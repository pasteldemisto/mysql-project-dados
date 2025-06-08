from models.recepcionista_setor import RecepcionistaSetor
from database.connection import connect
import random

def seed_recepcionista_setor():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT codigo_recepcionista FROM recepcionista")
    recepcionistas = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT codigo_setor FROM setor")
    setores = [row[0] for row in cursor.fetchall()]

    if not recepcionistas or not setores:
        print("É necessário ter recepcionistas e setores cadastrados antes de popular recepcionista_setor.")
        return

    
    turnos = ['matutino', 'vespertino', 'noturno']

    associacoes = []
    
    # Recupera as associações existentes no banco de dados
    cursor.execute("SELECT codigo_recepcionista, codigo_setor FROM recepcionista_setor")
    existentes = {(row[0], row[1]) for row in cursor.fetchall()}

    # Gerar a associação entre recepcionistas e setores
    for _ in range(len(recepcionistas)):
        associacao = RecepcionistaSetor.gerar_recepcionista_setor(recepcionistas, setores, turnos)
        
        # Verifica se a combinação de codigo_recepcionista e codigo_setor já existe
        if (associacao.codigo_recepcionista, associacao.codigo_setor) not in existentes:
            associacoes.append(associacao.to_tuple())
            existentes.add((associacao.codigo_recepcionista, associacao.codigo_setor))

    if associacoes:
        try:
            cursor.execute("START TRANSACTION;")
            sql = """
                INSERT INTO recepcionista_setor (codigo_recepcionista, codigo_setor, turno, data_alocacao)
                VALUES (%s, %s, %s, %s)
            """
            cursor.executemany(sql, associacoes)
            connection.commit()
            print(f"{len(associacoes)} registros inseridos em recepcionista_setor com sucesso!")
        except Exception as e:
            connection.rollback()
            print("Erro ao popular recepcionista_setor:", e)
        finally:
            cursor.close()
            connection.close()
    else:
        print("Nenhuma nova associação foi inserida. Verifique se todas as combinações já estão presentes.")
