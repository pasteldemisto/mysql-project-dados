from faker import Faker
import random

fake = Faker('pt_BR')
MAX_ADDRESS_LENGTH = 255

class Paciente:
    def __init__(self, cpf, data_nasc, nome, endereco, telefone):
        self.cpf = cpf
        self.data_nasc = data_nasc
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone

    @staticmethod
    def gerar_paciente():
        endereco = fake.address().replace('\n', ', ')

        # Garantir que o tamanho do endereço não ultrapasse o limite de 255 caracteres
        if len(endereco) > MAX_ADDRESS_LENGTH:
            endereco = endereco[:MAX_ADDRESS_LENGTH]

        return Paciente(
            cpf=fake.unique.random_number(digits=11, fix_len=True),
            data_nasc=fake.date_of_birth(minimum_age=18, maximum_age=90),
            nome=fake.name(),
            endereco=endereco,
            telefone=fake.phone_number()
        )

    def to_tuple(self):
        return (self.cpf, self.data_nasc, self.nome, self.endereco, self.telefone)
