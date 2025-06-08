from models.setor import Setor
from database.connection import connect

def seed_setores():
    setores = [
        ("Setor responsável por atendimentos de emergência médica.", "Térreo", "Emergência"),
        ("Realiza atendimentos a pacientes com problemas cardíacos.", "1º Andar", "Cardiologia"),
        ("Acompanha gestantes e realiza partos.", "2º Andar", "Obstetrícia"),
        ("Setor para cirurgias em geral.", "Subsolo", "Centro Cirúrgico"),
        ("Unidade de terapia intensiva para pacientes graves.", "3º Andar", "UTI"),
        ("Setor de atendimento a pacientes com doenças infecciosas.", "Anexo A", "Doenças Infecciosas"),
        ("Exames laboratoriais e análises clínicas.", "Térreo", "Laboratório"),
        ("Consultas e acompanhamento de pacientes com diabetes e hipertensão.", "1º Andar", "Clínica Geral"),
        ("Administração do hospital.", "Cobertura", "Administração"),
        ("Atendimento psicológico e psiquiátrico.", "2º Andar", "Saúde Mental")
    ]

    connection = connect()
    cursor = connection.cursor()

    try:
        cursor.execute("START TRANSACTION;")
        sql = """
            INSERT INTO setor (descricao, localizacao, nomeSetor)
            VALUES (%s, %s, %s)
        """
        cursor.executemany(sql, setores)
        connection.commit()
        print(f"{cursor.rowcount} setores inseridos com sucesso.")
    except Exception as e:
        connection.rollback()
        print("Erro ao inserir setores:", e)
    finally:
        cursor.close()
        connection.close()
