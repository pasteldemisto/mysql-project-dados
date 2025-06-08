from seed.seed_medicos import seed_medicos
from seed.seed_pacientes import seed_pacientes
from seed.seed_enfermeiros import seed_enfermeiros
from seed.seed_recepcionistas import seed_recepcionistas
from seed.seed_setores import seed_setores
from seed.seed_contatos_emergencia import seed_contatos_emergencia
from seed.seed_medico_setor import seed_medico_setor
from seed.seed_enfermeiro_setor import seed_enfermeiro_setor
from seed.seed_recepcionistas_setor import seed_recepcionista_setor
from seed.seed_atendimentos import seed_atendimentos
from seed.seed_exames import seed_exames
from seed.seed_prescricoes import seed_prescricoes
from seed.seed_medicamentos import seed_medicamentos
from seed.seed_suprimentos import seed_suprimentos
from seed.seed_estoque_medicamentos import seed_estoque_medicamentos
from seed.seed_estoque_suprimentos import seed_estoque_suprimentos

if __name__ == "__main__":
    seed_medicos()
    seed_pacientes()
    seed_enfermeiros()
    seed_recepcionistas()
    seed_setores()
    seed_contatos_emergencia()
    seed_medico_setor()
    seed_enfermeiro_setor()
    seed_recepcionista_setor()
    seed_atendimentos()
    seed_exames()
    seed_prescricoes()
    seed_medicamentos()
    seed_suprimentos()
    seed_estoque_medicamentos()
    seed_estoque_suprimentos()

    print("Banco de dados populado com sucesso!")