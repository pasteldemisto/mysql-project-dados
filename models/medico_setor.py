from datetime import datetime
import random

class MedicoSetor:
    def __init__(self, codigo_medico, codigo_setor, turno, data_alocacao):
        self.codigo_medico = codigo_medico
        self.codigo_setor = codigo_setor
        self.turno = turno
        self.data_alocacao = data_alocacao

    @staticmethod
    def gerar_medico_setor(codigo_medico, codigo_setor, turnos, datas_base):
        turno = random.choice(turnos)
        data_alocacao = random.choice(datas_base)
        return MedicoSetor(codigo_medico, codigo_setor, turno, data_alocacao)

    def to_tuple(self):
        return (self.codigo_medico, self.codigo_setor, self.turno, self.data_alocacao)
