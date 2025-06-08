from datetime import datetime, timedelta
import random

class Atendimento:
    def __init__(self, codigo_medico, codigo_paciente, codigo_recepcionista, codigo_setor, diagnostico, dataHora):
        self.codigo_medico = codigo_medico
        self.codigo_paciente = codigo_paciente
        self.codigo_recepcionista = codigo_recepcionista
        self.codigo_setor = codigo_setor
        self.diagnostico = diagnostico
        self.dataHora = dataHora

    @staticmethod
    def gerar_atendimento(codigos_medicos, codigos_pacientes, codigos_recepcionistas, codigos_setores, diagnosticos):
        return Atendimento(
            codigo_medico=random.choice(codigos_medicos),
            codigo_paciente=random.choice(codigos_pacientes),
            codigo_recepcionista=random.choice(codigos_recepcionistas),
            codigo_setor=random.choice(codigos_setores),
            diagnostico=random.choice(diagnosticos),
            dataHora=(datetime.now() - timedelta(days=random.randint(0, 1000))).strftime('%Y-%m-%d %H:%M:%S')
        )

    def to_tuple(self):
        return (self.codigo_medico, self.codigo_paciente, self.codigo_recepcionista, self.codigo_setor, self.diagnostico, self.dataHora)
