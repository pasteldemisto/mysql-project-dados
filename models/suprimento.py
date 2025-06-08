import random
class Suprimento:
    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao

    @staticmethod
    def gerar(nomes_base):
        nome, descricao = random.choice(nomes_base)
        return Suprimento(nome, descricao)

    def to_tuple(self):
        return (self.nome, self.descricao)