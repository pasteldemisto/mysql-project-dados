from database.connection import connect
import models.suprimento
from faker import Faker
import mysql.connector
from mysql.connector import Error
from datetime import datetime, timedelta
import random

# Conectando ao mysql
#connection = connect()



fake = Faker("pt_BR")

def connect_to_db():
    try:
        connection = connect()
        return connection
    except Error as e:
        print(f"Erro de conexão: {e}")
        return None




############################# Médico #################################

# Especialidades obrigatórias + outras
especialidades_fixas = ["Cardiologia", "Ortopedia", "Pediatria"]
especialidades_extra = [
    "Neurologia", "Dermatologia", "Ginecologia",
    "Oncologia", "Psiquiatria", "Oftalmologia", "Urologia"
]

# Quantidade total de médicos
TOTAL_MEDICOS = 1000

# Garante que as especialidades fixas estejam presentes (com alguns repetidos)
medicos = []
connection2 = connect_to_db()
cursor2 = connection2.cursor()
for especialidade in especialidades_fixas:
    for _ in range(50):  # 50 médicos por especialidade específica
        cpf = fake.unique.random_number(digits=11, fix_len=True)
        crm = f"{random.randint(10000, 99999)}/BR"
        nome = fake.name()
        telefone = fake.phone_number()
        medicos.append((cpf, crm, nome, especialidade, telefone))

# Preenche o restante dos médicos com especialidades variadas
for _ in range(TOTAL_MEDICOS - len(medicos)):
    cpf = fake.unique.random_number(digits=11, fix_len=True)
    crm = f"{random.randint(10000, 99999)}/BR"
    nome = fake.name()
    especialidade = random.choice(especialidades_fixas + especialidades_extra)
    telefone = fake.phone_number()
    medicos.append((cpf, crm, nome, especialidade, telefone))

# Inserção no banco
try:
    cursor2.execute("START TRANSACTION;")
    sql = """
        INSERT INTO medico (cpf, crm, nome, especialidade, telefone)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor2.executemany(sql, medicos)
    connection2.commit()
    print(f"{cursor2.rowcount} médicos inseridos com sucesso.")
except Exception as e:
    connection2.rollback()
    print("Erro ao inserir médicos:", e)
finally:
    cursor2.close()
    connection2.close()

############################# Médico #################################


############################# Paciente #################################

fake2 = Faker('pt_BR')

def popular_pacientes(qtd_pacientes=1000):
    try:
        conexao = connect()
        if conexao.is_connected():
            cursor = conexao.cursor()

            pacientes = []

            for _ in range(qtd_pacientes):
                cpf = fake.unique.random_number(digits=11)
                data_nasc = fake.date_of_birth(minimum_age=18, maximum_age=90)
                nome = fake.name()
                endereco = fake.address().replace('\n', ', ')
                telefone = fake.phone_number()

                pacientes.append((cpf, data_nasc, nome, endereco, telefone))

            cursor.execute("START TRANSACTION;")
            cursor.executemany("""
                INSERT INTO paciente (cpf, dataNascimento, nome, endereco, telefone)
                VALUES (%s, %s, %s, %s, %s)
            """, pacientes)
            conexao.commit()
            print(f"{qtd_pacientes} pacientes inseridos com sucesso!")

    except Error as e:
        print("Erro ao inserir pacientes:", e)
        if conexao:
            conexao.rollback()
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()
popular_pacientes()
############################# Paciente #################################


############################# Enfermeiro #################################
def popular_enfermeiros(qtd=500):
    try:
        conexao = connect()
        if conexao.is_connected():
            cursor = conexao.cursor()
            enfermeiros = []

            for _ in range(qtd):
                cpf = fake.unique.random_number(digits=11)
                coren = f"{fake.random_int(min=100000, max=999999)}-{fake.random_uppercase_letter()}"
                nome = fake.name()
                telefone = fake.phone_number()
                enfermeiros.append((cpf, coren, nome, telefone))

            cursor.execute("START TRANSACTION;")
            cursor.executemany("""
                INSERT INTO enfermeiro (cpf, coren, nome, telefone)
                VALUES (%s, %s, %s, %s)
            """, enfermeiros)
            conexao.commit()
            print(f"{qtd} enfermeiros inseridos com sucesso!")

    except Error as e:
        print("Erro ao inserir enfermeiros:", e)
        if conexao:
            conexao.rollback()
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()
############################# Enfermeiro #################################


############################# Recepcionista #################################
def popular_recepcionistas(qtd=200):
    try:
        conexao = connect()
        if conexao.is_connected():
            cursor = conexao.cursor()
            recepcionistas = []

            for _ in range(qtd):
                cpf = fake.unique.random_number(digits=11)
                telefone = fake.phone_number()
                nome = fake.name()
                recepcionistas.append((cpf, telefone, nome))

            cursor.execute("START TRANSACTION;")
            cursor.executemany("""
                INSERT INTO recepcionista (cpf, telefone, nome)
                VALUES (%s, %s, %s)
            """, recepcionistas)
            conexao.commit()
            print(f"{qtd} recepcionistas inseridos com sucesso!")

    except Error as e:
        print("Erro ao inserir recepcionistas:", e)
        if conexao:
            conexao.rollback()
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()
############################# Recepcionista #################################


############################# Contato_Emergencia #################################
def popular_contatos_emergencia():
    try:
        conexao = connect()
        if conexao.is_connected():
            cursor = conexao.cursor()

            # Buscar todos os pacientes
            cursor.execute("SELECT codigo_paciente FROM paciente")
            pacientes = cursor.fetchall()

            contatos = []
            graus_parentesco = ['Pai', 'Mãe', 'Irmão', 'Irmã', 'Esposo(a)', 'Tio(a)', 'Amigo(a)']

            for paciente in pacientes:
                codigo_paciente = paciente[0]
                quantidade_contatos = random.randint(1, 3)  # de 1 a 3 contatos por paciente
                for _ in range(quantidade_contatos):
                    nome = fake.name()
                    parentesco = random.choice(graus_parentesco)
                    telefone = fake.phone_number()
                    contatos.append((codigo_paciente, nome, parentesco, telefone))

            cursor.execute("START TRANSACTION;")
            cursor.executemany("""
                INSERT INTO contato_emergencia (codigo_paciente, nome, parentesco, telefone)
                VALUES (%s, %s, %s, %s)
            """, contatos)
            conexao.commit()
            print(f"{len(contatos)} contatos de emergência inseridos com sucesso!")

    except Error as e:
        print("Erro ao inserir contatos de emergência:", e)
        if conexao:
            conexao.rollback()
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()
############################# Contato_Emergencia #################################


############################# Setor #################################
def popular_setores():
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

    try:
        conexao = connect()
        if conexao.is_connected():
            cursor = conexao.cursor()
            cursor.execute("START TRANSACTION;")

            cursor.executemany("""
                INSERT INTO setor (descricao, localizacao, nomeSetor)
                VALUES (%s, %s, %s)
            """, setores)

            conexao.commit()
            print(f"{len(setores)} setores inseridos com sucesso!")

    except Error as e:
        print("Erro ao inserir setores:", e)
        if conexao:
            conexao.rollback()
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()
############################# Setor #################################

############################# Medico_Setor #################################
def popular_medico_setor():
    try:
        conexao = connect()
        if conexao.is_connected():
            cursor = conexao.cursor()

            # Recuperando os médicos e setores cadastrados
            cursor.execute("SELECT codigo_medico FROM medico")
            medicos = [linha[0] for linha in cursor.fetchall()]

            cursor.execute("SELECT codigo_setor FROM setor")
            setores = [linha[0] for linha in cursor.fetchall()]

            if not medicos or not setores:
                print("É necessário ter médicos e setores cadastrados antes de popular medico_setor.")
                return

            associacoes = []
            turnos = ['matutino', 'vespertino', 'noturno']
            datas_base = [datetime.now() - timedelta(days=random.randint(0, 1000)) for _ in range(len(medicos))]

            for i, codigo_medico in enumerate(medicos):
                setor_escolhido = random.choice(setores)
                turno = random.choice(turnos)
                data_alocacao = datas_base[i % len(datas_base)]
                associacoes.append((codigo_medico, setor_escolhido, turno, data_alocacao.strftime('%Y-%m-%d %H:%M:%S')))

            cursor.execute("START TRANSACTION;")
            cursor.executemany("""
                INSERT INTO medico_setor (codigo_medico, codigo_setor, turno, data_alocacao)
                VALUES (%s, %s, %s, %s)
            """, associacoes)

            conexao.commit()
            print(f"{len(associacoes)} registros inseridos em medico_setor com sucesso!")

    except Error as e:
        print("Erro ao popular medico_setor:", e)
        if conexao:
            conexao.rollback()
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()
############################# Medico_Setor #################################

############################# Enfermeiro_Setor #################################
def popular_enfermeiro_setor():
    try:
        conexao = connect()
        if conexao.is_connected():
            cursor = conexao.cursor()

            # Recupera enfermeiros e setores cadastrados
            cursor.execute("SELECT codigo_enfermeiro FROM enfermeiro")
            enfermeiros = [row[0] for row in cursor.fetchall()]

            cursor.execute("SELECT codigo_setor FROM setor")
            setores = [row[0] for row in cursor.fetchall()]

            if not enfermeiros or not setores:
                print("É necessário ter enfermeiros e setores cadastrados antes de popular enfermeiro_setor.")
                return

            turnos = ['matutino', 'vespertino', 'noturno']
            associacoes = []

            for enfermeiro in enfermeiros:
                setor = random.choice(setores)
                turno = random.choice(turnos)
                data_alocacao = datetime.now() - timedelta(days=random.randint(0, 1000))
                associacoes.append((enfermeiro, setor, turno, data_alocacao.strftime('%Y-%m-%d %H:%M:%S')))

            cursor.execute("START TRANSACTION;")
            cursor.executemany("""
                INSERT INTO enfermeiro_setor (codigo_enfermeiro, codigo_setor, turno, data_alocacao)
                VALUES (%s, %s, %s, %s)
            """, associacoes)

            conexao.commit()
            print(f"{len(associacoes)} registros inseridos em enfermeiro_setor com sucesso!")

    except Error as e:
        print("Erro ao popular enfermeiro_setor:", e)
        if conexao:
            conexao.rollback()
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()
############################# Enfermeiro_Setor #################################

############################# Recepcionista_Setor #################################
def popular_recepcionista_setor():
    try:
        conexao = connect()
        if conexao.is_connected():
            cursor = conexao.cursor()

            # Recupera recepcionistas e setores cadastrados
            cursor.execute("SELECT codigo_recepcionista FROM recepcionista")
            recepcionistas = [row[0] for row in cursor.fetchall()]

            cursor.execute("SELECT codigo_setor FROM setor")
            setores = [row[0] for row in cursor.fetchall()]

            if not recepcionistas or not setores:
                print("É necessário ter recepcionistas e setores cadastrados antes de popular rececionista_setor.")
                return

            turnos = ['matutino', 'vespertino', 'noturno']
            associacoes = []

            for recepcionista in recepcionistas:
                setor = random.choice(setores)
                turno = random.choice(turnos)
                data_alocacao = datetime.now() - timedelta(days=random.randint(0, 1000))
                associacoes.append((recepcionista, setor, turno, data_alocacao.strftime('%Y-%m-%d %H:%M:%S')))

            cursor.execute("START TRANSACTION;")
            cursor.executemany("""
                INSERT INTO recepcionista_setor (codigo_recepcionista, codigo_setor, turno, data_alocacao)
                VALUES (%s, %s, %s, %s)
            """, associacoes)

            conexao.commit()
            print(f"{len(associacoes)} registros inseridos em recepcionista_setor com sucesso!")

    except Error as e:
        print("Erro ao popular recepcionista_setor:", e)
        if conexao:
            conexao.rollback()
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()
############################# Recepcionista_Setor #################################

############################# Atendimento #################################
def popular_atendimentos(qtd=1000):
    try:
        conexao = connect()
        if conexao.is_connected():
            cursor = conexao.cursor()

            # Recuperando IDs de médicos, pacientes, recepcionistas e setores
            cursor.execute("SELECT codigo_medico FROM medico")
            medicos = [row[0] for row in cursor.fetchall()]

            cursor.execute("SELECT codigo_paciente FROM paciente")
            pacientes = [row[0] for row in cursor.fetchall()]

            cursor.execute("SELECT codigo_recepcionista FROM recepcionista")
            recepcionistas = [row[0] for row in cursor.fetchall()]

            cursor.execute("SELECT codigo_setor FROM setor")
            setores = [row[0] for row in cursor.fetchall()]

            if not medicos or not pacientes or not recepcionistas or not setores:
                print("Você precisa cadastrar médicos, pacientes, recepcionistas e setores antes.")
                return

            diagnosticos = [
                "Hipertensão arterial", "Diabetes mellitus tipo 2", "Asma brônquica",
                "Infecção urinária", "Gripe comum", "Fratura do punho",
                "Cefaleia tensional", "Gastrite aguda", "Otite média", "Dengue"
            ]

            atendimentos = []

            for _ in range(qtd):
                medico = random.choice(medicos)
                paciente = random.choice(pacientes)
                recepcionista = random.choice(recepcionistas)
                setor = random.choice(setores)
                diagnostico = random.choice(diagnosticos)
                dataHora = datetime.now() - timedelta(days=random.randint(0, 1000))
                atendimentos.append((
                    medico, paciente, recepcionista, setor,
                    diagnostico, dataHora.strftime('%Y-%m-%d %H:%M:%S')
                ))

            cursor.execute("START TRANSACTION;")
            cursor.executemany("""
                INSERT INTO atendimento (codigo_medico, codigo_paciente, codigo_recepcionista, codigo_setor, diagnostico, dataHora)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, atendimentos)

            conexao.commit()
            print(f"{qtd} atendimentos inseridos com sucesso!")

    except Error as e:
        print("Erro ao popular atendimentos:", e)
        if conexao:
            conexao.rollback()
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()
############################# Atendimento #################################

############################# Exames #################################
def popular_exames(qtd=1000):
    try:
        conexao = connect()
        if conexao.is_connected():
            cursor = conexao.cursor()

            # Recuperar os atendimentos existentes
            cursor.execute("SELECT codigo_atendimento FROM atendimento")
            atendimentos = [row[0] for row in cursor.fetchall()]

            if not atendimentos:
                print("É necessário ter atendimentos cadastrados antes de inserir exames.")
                return

            tipos_exame = ["Sangue", "Urina", "Raio-X", "Tomografia", "Ultrassom"]
            status_exame = ["pendente", "concluído"]
            resultados = ["Normal", "Alterado", "Necessário repetir", "Inconclusivo", "Compatível com diagnóstico"]

            exames = []

            for _ in range(qtd):
                tipo = random.choice(tipos_exame)
                status = random.choice(status_exame)
                resultado = random.choice(resultados)
                atendimento = random.choice(atendimentos)
                data_realizacao = datetime.now() - timedelta(days=random.randint(0, 365))
                exames.append((
                    tipo,
                    data_realizacao.strftime('%Y-%m-%d %H:%M:%S'),
                    status,
                    resultado,
                    atendimento
                ))

            cursor.execute("START TRANSACTION;")
            cursor.executemany("""
                INSERT INTO exame (tipo_exame, data_realizacao, exame_status, resultado, codigo_atendimento)
                VALUES (%s, %s, %s, %s, %s)
            """, exames)

            conexao.commit()
            print(f"{qtd} exames inseridos com sucesso!")

    except Error as e:
        print("Erro ao popular exames:", e)
        if conexao:
            conexao.rollback()
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()
############################# Exames #################################

############################# Prescricao #################################
def popular_prescricoes(qtd=1000):
    try:
        conexao = connect()
        if conexao.is_connected():
            cursor = conexao.cursor()

            # Buscar atendimentos disponíveis
            cursor.execute("SELECT codigo_atendimento FROM atendimento")
            atendimentos = [row[0] for row in cursor.fetchall()]

            if not atendimentos:
                print("Cadastre atendimentos antes de inserir prescrições.")
                return

            dosagens = ["1 comprimido", "2 ml", "50 mg", "10 gotas", "1 ampola"]
            duracoes = ["7 dias", "10 dias", "15 dias", "1 mês", "uso contínuo"]

            prescricoes = []
            for _ in range(qtd):
                atendimento = random.choice(atendimentos)
                dosagem = random.choice(dosagens)
                duracao = random.choice(duracoes)
                prescricoes.append((dosagem, duracao, atendimento))

            cursor.execute("START TRANSACTION;")
            cursor.executemany("""
                INSERT INTO prescricao (dosagem, duracao, codigo_atendimento)
                VALUES (%s, %s, %s)
            """, prescricoes)

            conexao.commit()
            print(f"{qtd} prescrições inseridas com sucesso!")

    except Error as e:
        print("Erro ao popular prescrições:", e)
        if conexao:
            conexao.rollback()
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()
############################# Prescricao #################################

############################# Medicamento #################################
def popular_medicamentos(qtd=500):
    try:
        conexao = connect()
        if conexao.is_connected():
            cursor = conexao.cursor()

            # Buscar prescrições disponíveis
            cursor.execute("SELECT codigo_prescricao FROM prescricao")
            prescricoes = [row[0] for row in cursor.fetchall()]

            if not prescricoes:
                print("Cadastre prescrições antes de inserir medicamentos.")
                return

            fabricantes = ["EMS", "Medley", "Eurofarma", "Aché", "Hypera", "Neo Química", "Bayer"]
            medicamentos = []

            prescricoes_escolhidas = random.sample(prescricoes, min(qtd, len(prescricoes)))

            for cod_presc in prescricoes_escolhidas:
                fabricante = random.choice(fabricantes)
                validade = fake.date_between(start_date='+30d', end_date='+365d')
                lote = f"L{random.randint(1000,9999)}-{random.randint(100,999)}"
                telefone = fake.phone_number()
                medicamentos.append((fabricante, validade, lote, cod_presc, telefone))

            cursor.execute("START TRANSACTION;")
            cursor.executemany("""
                INSERT INTO medicamento (fabricante, data_validade, lote, codigo_prescricao, telefone)
                VALUES (%s, %s, %s, %s, %s)
            """, medicamentos)

            conexao.commit()
            print(f"{len(medicamentos)} medicamentos inseridos com sucesso!")

    except Error as e:
        print("Erro ao popular medicamentos:", e)
        if conexao:
            conexao.rollback()
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()
############################# Medicamento #################################

############################# Suprimento #################################
def gerar_dados_suprimento(qtd=1_000_000):
    nomes_base = [
        ("Seringa descartável", "Usada para aplicações intravenosas ou intramusculares"),
        ("Luvas cirúrgicas", "Utilizadas em procedimentos médicos para proteção"),
        ("Máscara N95", "Máscara de alta proteção contra partículas"),
        ("Álcool em gel", "Higienização das mãos"),
        ("Gaze estéril", "Utilizada para curativos e absorção de sangue"),
        ("Esparadrapo", "Fixa curativos na pele"),
        ("Soro fisiológico", "Solução salina para limpeza de feridas ou diluições"),
        ("Termômetro digital", "Mede a temperatura corporal"),
        ("Avental descartável", "Usado por profissionais em ambiente estéril"),
        ("Touca cirúrgica", "Cobertura descartável para os cabelos")
    ]
    for i in range(qtd):
        nome, descricao = random.choice(nomes_base)
        yield (f"{nome}", descricao)

#Popular a tabela de suprimentos médicos no banco de dados
def popular_suprimentos():
    connection = connect_to_db()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("START TRANSACTION;")
            insert_sql = "INSERT INTO suprimento (nome, descricao) VALUES (%s, %s)"

            batch_size = 10000
            buffer = []

            for i, dado in enumerate(gerar_dados_suprimento()):
                buffer.append(dado)
                if len(buffer) == batch_size:
                    cursor.executemany(insert_sql, buffer)
                    print(f"{i+1} registros inseridos...")
                    buffer = []

            if buffer:
                cursor.executemany(insert_sql, buffer)

            connection.commit()
            print("Inserção finalizada com sucesso!")
        except Error as e:
            print(f"Erro ao inserir dados: {e}")
            connection.rollback()
        finally:
            cursor.close()
            connection.close()

popular_suprimentos()
############################# Suprimento #################################

############################# Estoque_Medicamento #################################
def popular_estoque_medicamentos():
    try:
        conexao = connect()
        if conexao.is_connected():
            cursor = conexao.cursor()

            # Buscar medicamentos existentes
            cursor.execute("SELECT codigo_medicamento, lote FROM medicamento")
            medicamentos = cursor.fetchall()

            if not medicamentos:
                print("É necessário ter medicamentos cadastrados antes de popular o estoque.")
                return

            dados_estoque = []
            for codigo_medicamento, lote in medicamentos:
                quantidade = random.randint(5, 100)
                dados_estoque.append((codigo_medicamento, quantidade, lote))

            cursor.execute("START TRANSACTION;")
            cursor.executemany("""
                INSERT INTO estoque_medicamento (codigo_medicamento, quantidade, lote)
                VALUES (%s, %s, %s)
            """, dados_estoque)

            conexao.commit()
            print(f"{len(dados_estoque)} registros de estoque de medicamentos inseridos com sucesso!")

    except Error as e:
        print("Erro ao popular estoque de medicamentos:", e)
        if conexao:
            conexao.rollback()
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()
############################# Estoque_Medicamento #################################

############################# Estoque_Suprimento #################################

def popular_estoque_suprimentos():
    try:
        conexao = connect()
        if conexao.is_connected():
            cursor = conexao.cursor()

            # Buscar suprimentos existentes
            cursor.execute("SELECT codigo_suprimento, nome FROM suprimento LIMIT 1000")
            suprimentos = cursor.fetchall()

            if not suprimentos:
                print("É necessário ter suprimentos cadastrados antes de popular o estoque.")
                return

            dados_estoque = []
            for codigo_suprimento, nome in suprimentos:
                quantidade = random.randint(10, 200)
                lote = f"LOTE-{random.randint(1000,9999)}"
                dados_estoque.append((codigo_suprimento, quantidade, lote))

            cursor.execute("START TRANSACTION;")
            cursor.executemany("""
                INSERT INTO estoque_suprimento (codigo_suprimento, quantidade, lote)
                VALUES (%s, %s, %s)
            """, dados_estoque)

            conexao.commit()
            print(f"{len(dados_estoque)} registros de estoque de suprimentos inseridos com sucesso!")

    except Error as e:
        print("Erro ao popular estoque de suprimentos:", e)
        if conexao:
            conexao.rollback()
    finally:
        if conexao and conexao.is_connected():
            cursor.close()
            conexao.close()
############################# Estoque_Suprimento #################################

############################# Chamada Métodos #################################
popular_enfermeiros()
popular_pacientes()
popular_suprimentos()
popular_recepcionistas()
popular_contatos_emergencia()
popular_setores()
popular_medico_setor()
popular_enfermeiro_setor()
popular_recepcionista_setor()
popular_atendimentos()
popular_exames()
popular_prescricoes()
popular_medicamentos()
popular_estoque_medicamentos()
popular_estoque_suprimentos()
############################# Chamada Métodos #################################