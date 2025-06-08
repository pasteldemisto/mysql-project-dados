from faker import Faker
import random
import string

fake = Faker('pt_BR')

class Enfermeiro:
    def __init__(self, cpf, coren, nome, telefone):
        self.cpf = cpf
        self.coren = coren
        self.nome = nome
        self.telefone = telefone

    @staticmethod
    def gerar_enfermeiro():
        coren_num = random.randint(100000, 999999)
        coren_letra = random.choice(string.ascii_uppercase)
        coren = f"{coren_num}-{coren_letra}"

        return Enfermeiro(
            cpf=fake.unique.random_number(digits=11, fix_len=True),
            coren=coren,
            nome=fake.name(),
            telefone=fake.phone_number()
        )

    def to_tuple(self):
        return (self.cpf, self.coren, self.nome, self.telefone)
