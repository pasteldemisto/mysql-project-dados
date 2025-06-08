from datetime import datetime, timedelta
import random

class Exame:
    def __init__(self, tipo_exame, data_realizacao, exame_status, resultado, codigo_atendimento):
        self.tipo_exame = tipo_exame
        self.data_realizacao = data_realizacao
        self.exame_status = exame_status
        self.resultado = resultado
        self.codigo_atendimento = codigo_atendimento

    @staticmethod
    def gerar_exame(codigos_atendimentos, tipos_exame, status_exame, resultados):
        tipo_exame = random.choice(tipos_exame)
        exame_status = random.choice(status_exame)
        resultado = random.choice(resultados)
        codigo_atendimento = random.choice(codigos_atendimentos)
        data_realizacao = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d %H:%M:%S')

        return Exame(tipo_exame, data_realizacao, exame_status, resultado, codigo_atendimento)

    def to_tuple(self):
        return (self.tipo_exame, self.data_realizacao, self.exame_status, self.resultado, self.codigo_atendimento)
