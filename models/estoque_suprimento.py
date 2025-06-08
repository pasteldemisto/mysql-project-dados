import random

class EstoqueSuprimento:
    def __init__(self, codigo_suprimento, quantidade, lote):
        self.codigo_suprimento = codigo_suprimento
        self.quantidade = quantidade
        self.lote = lote

    @staticmethod
    def gerar_estoque_suprimento(codigos_suprimentos, lotes):
        codigo_suprimento = random.choice(codigos_suprimentos)
        quantidade = random.randint(10, 200)  # Quantidade entre 10 e 200
        lote = random.choice(lotes)
        return EstoqueSuprimento(codigo_suprimento, quantidade, lote)

    def to_tuple(self):
        return (self.codigo_suprimento, self.quantidade, self.lote)
