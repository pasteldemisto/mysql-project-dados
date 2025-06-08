import random

class EstoqueMedicamento:
    def __init__(self, codigo_medicamento, quantidade, lote):
        self.codigo_medicamento = codigo_medicamento
        self.quantidade = quantidade
        self.lote = lote

    @staticmethod
    def gerar_medicamento(codigos_medicamentos, lotes):
        codigo_medicamento = random.choice(codigos_medicamentos)
        quantidade = random.randint(5, 100)  # Quantidade entre 5 e 100
        lote = random.choice(lotes)
        return EstoqueMedicamento(codigo_medicamento, quantidade, lote)

    def to_tuple(self):
        return (self.codigo_medicamento, self.quantidade, self.lote)
