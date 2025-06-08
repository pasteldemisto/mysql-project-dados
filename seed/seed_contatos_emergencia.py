from models.contato_emergencia import ContatoEmergencia
from database.connection import connect
import random

def seed_contatos_emergencia():
    connection = connect()
    cursor = connection.cursor()

    cursor.execute("SELECT codigo_paciente FROM paciente")
    pacientes = [row[0] for row in cursor.fetchall()]

    if not pacientes:
        print("Você precisa cadastrar pacientes antes.")
        return

    graus_parentesco = ['Pai', 'Mãe', 'Irmão', 'Irmã', 'Esposo(a)', 'Tio(a)', 'Amigo(a)']
    
    contatos = []
    for codigo_paciente in pacientes:
        quantidade_contatos = random.randint(1, 3)  # 1 a 3 contatos por paciente
        for _ in range(quantidade_contatos):
            contato = ContatoEmergencia.gerar_contato_emergencia(codigo_paciente, graus_parentesco)
            contatos.append(contato.to_tuple())

    try:
        cursor.execute("START TRANSACTION;")
        sql = """
            INSERT INTO contato_emergencia (codigo_paciente, nome, parentesco, telefone)
            VALUES (%s, %s, %s, %s)
        """
        cursor.executemany(sql, contatos)
        connection.commit()
        print(f"{cursor.rowcount} contatos de emergência inseridos com sucesso.")
    except Exception as e:
        connection.rollback()
        print("Erro ao inserir contatos de emergência:", e)
    finally:
        cursor.close()
        connection.close()
