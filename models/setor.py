class Setor:
    def __init__(self, descricao, localizacao, nomeSetor):
        self.descricao = descricao
        self.localizacao = localizacao
        self.nomeSetor = nomeSetor

    @staticmethod
    def gerar(descricao, localizacao, nomeSetor):
        return Setor(descricao, localizacao, nomeSetor)

    def to_tuple(self):
        return (self.descricao, self.localizacao, self.nomeSetor)