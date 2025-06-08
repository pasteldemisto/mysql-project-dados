from faker import Faker

fake = Faker('pt_BR')

class Recepcionista:
    def __init__(self, cpf, telefone, nome):
        self.cpf = cpf
        self.telefone = telefone
        self.nome = nome

    @staticmethod
    def gerar_recepcionista():
        return Recepcionista(
            cpf=fake.unique.random_number(digits=11, fix_len=True),
            telefone=fake.phone_number(),
            nome=fake.name()
        )

    def to_tuple(self):
        return (self.cpf, self.telefone, self.nome)
