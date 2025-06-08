from models.enfermeiro_setor import EnfermeiroSetor
from database.connection import connect
import random
from datetime import datetime, timedelta

def seed_enfermeiro_setor():
    # Recupera enfermeiros e setores cadastrados
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT codigo_enfermeiro FROM enfermeiro")
    enfermeiros = [linha[0] for linha in cursor.fetchall()]

    cursor.execute("SELECT codigo_setor FROM setor")
    setores = [linha[0] for linha in cursor.fetchall()]

    if not enfermeiros or not setores:
        print("É necessário ter enfermeiros e setores cadastrados antes de popular enfermeiro_setor.")
        return

    
    turnos = ['matutino', 'vespertino', 'noturno']
    datas_base = [datetime.now() - timedelta(days=random.randint(0, 1000)) for _ in range(len(enfermeiros))]

    # Gerando as associações entre enfermeiros e setores
    associacoes = []
    for codigo_enfermeiro in enfermeiros:
        setor_escolhido = random.choice(setores)
        associacao = EnfermeiroSetor.gerar_enfermeiro_setor(codigo_enfermeiro, setor_escolhido, turnos, datas_base)
        associacoes.append(associacao.to_tuple())

    
    try:
        cursor.execute("START TRANSACTION;")
        sql = """
            INSERT INTO enfermeiro_setor (codigo_enfermeiro, codigo_setor, turno, data_alocacao)
            VALUES (%s, %s, %s, %s)
        """
        cursor.executemany(sql, associacoes)
        connection.commit()
        print(f"{cursor.rowcount} registros inseridos em enfermeiro_setor com sucesso!")
    except Exception as e:
        connection.rollback()
        print("Erro ao popular enfermeiro_setor:", e)
    finally:
        cursor.close()
        connection.close()
