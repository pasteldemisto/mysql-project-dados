import random
from datetime import datetime, timedelta

class RecepcionistaSetor:
    def __init__(self, codigo_recepcionista, codigo_setor, turno, data_alocacao):
        self.codigo_recepcionista = codigo_recepcionista
        self.codigo_setor = codigo_setor
        self.turno = turno
        self.data_alocacao = data_alocacao

    @staticmethod
    def gerar_recepcionista_setor(codigos_recepcionistas, codigos_setores, turnos):
        codigo_recepcionista = random.choice(codigos_recepcionistas)
        codigo_setor = random.choice(codigos_setores)
        turno = random.choice(turnos)
        data_alocacao = (datetime.now() - timedelta(days=random.randint(0, 1000))).strftime('%Y-%m-%d %H:%M:%S')
        
        return RecepcionistaSetor(codigo_recepcionista, codigo_setor, turno, data_alocacao)

    def to_tuple(self):
        return (self.codigo_recepcionista, self.codigo_setor, self.turno, self.data_alocacao)
