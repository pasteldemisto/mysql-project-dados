from faker import Faker
import random

fake = Faker('pt_BR')

class ContatoEmergencia:
    def __init__(self, codigo_paciente, nome, parentesco, telefone):
        self.codigo_paciente = codigo_paciente
        self.nome = nome
        self.parentesco = parentesco
        self.telefone = telefone

    @staticmethod
    def gerar_contato_emergencia(codigo_paciente, graus_parentesco):
        return ContatoEmergencia(
            codigo_paciente=codigo_paciente,
            nome=fake.name(),
            parentesco=random.choice(graus_parentesco),
            telefone=fake.phone_number()
        )

    def to_tuple(self):
        return (self.codigo_paciente, self.nome, self.parentesco, self.telefone)
