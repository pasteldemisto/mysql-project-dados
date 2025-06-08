import random

class Prescricao:
    def __init__(self, dosagem, duracao, codigo_atendimento):
        self.dosagem = dosagem
        self.duracao = duracao
        self.codigo_atendimento = codigo_atendimento

    @staticmethod
    def gerar_prescricao(codigos_atendimentos, dosagens, duracoes):
        dosagem = random.choice(dosagens)
        duracao = random.choice(duracoes)
        codigo_atendimento = random.choice(codigos_atendimentos)
        return Prescricao(dosagem, duracao, codigo_atendimento)

    def to_tuple(self):
        return (self.dosagem, self.duracao, self.codigo_atendimento)
