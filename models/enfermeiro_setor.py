from datetime import datetime
import random

class EnfermeiroSetor:
    def __init__(self, codigo_enfermeiro, codigo_setor, turno, data_alocacao):
        self.codigo_enfermeiro = codigo_enfermeiro
        self.codigo_setor = codigo_setor
        self.turno = turno
        self.data_alocacao = data_alocacao

    @staticmethod
    def gerar_enfermeiro_setor(codigo_enfermeiro, codigo_setor, turnos, datas_base):
        turno = random.choice(turnos)
        data_alocacao = random.choice(datas_base)
        return EnfermeiroSetor(codigo_enfermeiro, codigo_setor, turno, data_alocacao)

    def to_tuple(self):
        return (self.codigo_enfermeiro, self.codigo_setor, self.turno, self.data_alocacao)
