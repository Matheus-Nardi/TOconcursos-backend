from database import SessionLocal
from models.questoes import Disciplina, Orgao, Instituicao, Banca, DificuldadeEnum
from models.questoes.questao import Questao
from models.questoes.alternativa import Alternativa


def get_or_create_by_label(db, model, label: str):
    obj = db.query(model).filter(model.label == label).first()
    if obj is None:
        obj = model(label=label)
        db.add(obj)
        db.commit()
        db.refresh(obj)
    return obj


def get_or_create_questao(
    db,
    enunciado: str,
    disciplina: Disciplina,
    dificuldade: DificuldadeEnum,
    orgao: Orgao,
    instituicao: Instituicao,
    banca: Banca,
):
    questao = db.query(Questao).filter(Questao.enunciado == enunciado).first()
    if questao is None:
        questao = Questao(
            enunciado=enunciado,
            disciplina=disciplina,
            dificuldade=dificuldade,
            orgao=orgao,
            instituicao=instituicao,
            banca=banca,
        )
        db.add(questao)
        db.commit()
        db.refresh(questao)
    return questao


def ensure_alternativas(
    db,
    questao: Questao,
    descricoes,
    indice_correta: int,
):
    """
    Cria alternativas se a questão ainda não tiver nenhuma.
    descricoes: lista de textos das alternativas em ordem [A, B, C, D, E]
    indice_correta: índice da correta (0 = A, 1 = B, ...)
    """
    existentes = db.query(Alternativa).filter(Alternativa.id_questao == questao.id).count()
    if existentes > 0:
        return

    for idx, desc in enumerate(descricoes):
        alt = Alternativa(
            descricao=desc,
            explicacao=None,
            is_correta=(idx == indice_correta),
            questao=questao,
        )
        db.add(alt)
    db.commit()


def run():
    db = SessionLocal()
    try:
        # Tabelas de apoio
        disciplina_portugues = get_or_create_by_label(db, Disciplina, "Língua Portuguesa")
        disciplina_hist_geo = get_or_create_by_label(db, Disciplina, "Historia e Geografia do Tocantins")

        orgao = get_or_create_by_label(db, Orgao, "Prefeitura Municipal de Palmas")
        instituicao = get_or_create_by_label(db, Instituicao, "UFTCOPESE")
        banca = get_or_create_by_label(db, Banca, "UFTCOPESE")

        # Questão 08
        enunciado_q8 = (
            "QUESTÃO 08\n"
            "Assinale a alternativa CORRETA que indique a sequência de\n"
            "verbos adequados nas frases.\n"
            "I. _____no discurso o início de seus estudos.\n"
            "II. A próxima _______legislativa iniciará em 24 de fevereiro.\n"
            "III. O projeto apresentado veio ____ objetivos dos\n"
            "trabalhadores, atendendo às suas reivindicações."
        )
        q8 = get_or_create_questao(
            db,
            enunciado=enunciado_q8,
            disciplina=disciplina_portugues,
            dificuldade=DificuldadeEnum.MEDIO,
            orgao=orgao,
            instituicao=instituicao,
            banca=banca,
        )
        alternativas_q8 = [
            "Evocou; sessão; ao encontro dos.",
            "Avocou; sessão; de encontro aos.",
            "Invocou; seção; ao encontro dos.",
            "Evocou; cessão; de encontro aos.",
            "Avocou; seção; ao encontro dos.",
        ]
        ensure_alternativas(db, q8, alternativas_q8, indice_correta=0)  # A

        # Questão 10
        enunciado_q10 = (
            "QUESTÃO 10\n"
            "Em textos oficiais, deve-se evitar a fragmentação de frases,\n"
            "uma vez que esse recurso estilístico dificulta a compreensão.\n"
            "Assinale a alternativa que apresenta o uso da fragmentação\n"
            "frasal de forma INCORRETA."
        )
        q10 = get_or_create_questao(
            db,
            enunciado=enunciado_q10,
            disciplina=disciplina_portugues,
            dificuldade=DificuldadeEnum.MEDIO,
            orgao=orgao,
            instituicao=instituicao,
            banca=banca,
        )
        alternativas_q10 = [
            "O documento foi aprovado no Comitê, após ampla\ndiscussão.",
            "Após ampla discussão, o documento foi aprovado no\nComitê.",
            "O documento, após ampla discussão, foi aprovado no\nComitê.",
            "O documento foi aprovado no Comitê. Após, ampla\ndiscussão.",
            "Depois de ampla discussão, o documento foi aprovado no\nComitê.",
        ]
        ensure_alternativas(db, q10, alternativas_q10, indice_correta=3)  # D

        # Questão 14
        enunciado_q14 = (
            "QUESTÃO 14\n"
            "O Tocantins tem destaque na produção agrícola, tanto regional\n"
            "quanto nacional. Nos últimos anos teve aumento considerável\n"
            "na área plantada e na produção agrícola.\n"
            "Assinale a alternativa CORRETA que indica os principais grãos\n"
            "produzido no estado."
        )
        q14 = get_or_create_questao(
            db,
            enunciado=enunciado_q14,
            disciplina=disciplina_hist_geo,
            dificuldade=DificuldadeEnum.FACIL,
            orgao=orgao,
            instituicao=instituicao,
            banca=banca,
        )
        alternativas_q14 = [
            "Soja, trigo e aveia.",
            "Soja, milho e arroz.",
            "Milho, centeio e trigo.",
            "Soja, cevada e centeio.",
            "Arroz, trigo e cevada.",
        ]
        ensure_alternativas(db, q14, alternativas_q14, indice_correta=1)  # B

        print("✅ Seed inicial executado com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao executar seed inicial: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    run()


