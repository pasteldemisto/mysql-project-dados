from models.medico_setor import MedicoSetor
from database.connection import connect
import random
from datetime import datetime, timedelta

def seed_medico_setor():
    
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT codigo_medico FROM medico")
    medicos = [linha[0] for linha in cursor.fetchall()]

    cursor.execute("SELECT codigo_setor FROM setor")
    setores = [linha[0] for linha in cursor.fetchall()]

    if not medicos or not setores:
        print("É necessário ter médicos e setores cadastrados antes de popular medico_setor.")
        return

    
    turnos = ['matutino', 'vespertino', 'noturno']
    datas_base = [datetime.now() - timedelta(days=random.randint(0, 1000)) for _ in range(len(medicos))]

    # Gerando as associações entre médicos e setores
    associacoes = []
    for codigo_medico in medicos:
        setor_escolhido = random.choice(setores)
        associacao = MedicoSetor.gerar_medico_setor(codigo_medico, setor_escolhido, turnos, datas_base)
        associacoes.append(associacao.to_tuple())

    
    try:
        cursor.execute("START TRANSACTION;")
        sql = """
            INSERT INTO medico_setor (codigo_medico, codigo_setor, turno, data_alocacao)
            VALUES (%s, %s, %s, %s)
        """
        cursor.executemany(sql, associacoes)
        connection.commit()
        print(f"{cursor.rowcount} registros inseridos em medico_setor com sucesso!")
    except Exception as e:
        connection.rollback()
        print("Erro ao popular medico_setor:", e)
    finally:
        cursor.close()
        connection.close()
