from faker import Faker
import random

fake = Faker('pt_BR')

class Medico:
    def __init__(self, cpf, crm, nome, especialidade, telefone):
        self.cpf = cpf
        self.crm = crm
        self.nome = nome
        self.especialidade = especialidade
        self.telefone = telefone

    @staticmethod
    def gerar_medico(especialidade=None):
        return Medico(
            cpf=fake.unique.random_number(digits=11, fix_len=True),
            crm=f"{random.randint(10000, 99999)}/BR",
            nome=fake.name(),
            especialidade=especialidade or random.choice(Medico.get_especialidades()),
            telefone=fake.phone_number()
        )

    @staticmethod
    def get_especialidades():
        return [
            "Cardiologia", "Ortopedia", "Pediatria",
            "Neurologia", "Dermatologia", "Ginecologia",
            "Oncologia", "Psiquiatria", "Oftalmologia", "Urologia"
        ]

    def to_tuple(self):
        return (self.cpf, self.crm, self.nome, self.especialidade, self.telefone)
