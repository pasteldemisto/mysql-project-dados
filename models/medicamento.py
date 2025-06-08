from faker import Faker
import random

fake = Faker('pt_BR')

class Medicamento:
    def __init__(self, fabricante, data_validade, lote, codigo_prescricao, telefone):
        self.fabricante = fabricante
        self.data_validade = data_validade
        self.lote = lote
        self.codigo_prescricao = codigo_prescricao
        self.telefone = telefone

    @staticmethod
    def gerar_medicamento(codigos_prescricoes, fabricantes):
        fabricante = random.choice(fabricantes)
        validade = fake.date_between(start_date='+30d', end_date='+365d')
        lote = f"L{random.randint(1000, 9999)}-{random.randint(100, 999)}"
        telefone = fake.phone_number()
        codigo_prescricao = random.choice(codigos_prescricoes)

        return Medicamento(fabricante, validade, lote, codigo_prescricao, telefone)

    def to_tuple(self):
        return (self.fabricante, self.data_validade, self.lote, self.codigo_prescricao, self.telefone)
