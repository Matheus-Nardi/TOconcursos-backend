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
        disciplina_matematica = get_or_create_by_label(db, Disciplina, "Matemática e Raciocínio Lógico")
        disciplina_leg_palmas = get_or_create_by_label(db, Disciplina, "Legislação de Palmas/TO")
        disciplina_administracao = get_or_create_by_label(db, Disciplina, "Administração")

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

        # Questão 16 - Matemática e Raciocínio Lógico
        enunciado_q16 = (
            "QUESTÃO 16\n"
            "A lógica dedutiva formal está interessada nas relações\n"
            "estruturais que articulam antecedentes e consequentes. Nessa\n"
            "lógica, pode-se dizer que a DEDUÇÃO se caracteriza por:\n"
            "I. Ter um consequente que é inferência necessária do\n"
            "antecedente.\n"
            "II. Ser um argumento organizado por enumeração.\n"
            "III. Ter um consequente cujo conteúdo não excede, não é mais\n"
            "informativo, que o do antecedente.\n"
            "IV. Ser um argumento que parte sempre do particular para o\n"
            "geral.\n"
            "V. Ter um consequente que não leva a um conhecimento novo,\n"
            "mas organiza o conhecimento já adquirido.\n"
            "Assinale a alternativa CORRETA."
        )
        q16 = get_or_create_questao(
            db,
            enunciado=enunciado_q16,
            disciplina=disciplina_matematica,
            dificuldade=DificuldadeEnum.MEDIO,
            orgao=orgao,
            instituicao=instituicao,
            banca=banca,
        )
        alternativas_q16 = [
            "Apenas as afirmativas I, II e IV estão corretas.",
            "Apenas as afirmativas III e V estão corretas.",
            "Apenas as afirmativas I e II estão corretas.",
            "Apenas as afirmativas I, III e V estão corretas.",
            "Nenhuma das afirmativas está correta.",
        ]
        ensure_alternativas(db, q16, alternativas_q16, indice_correta=3)  # D

        # Questão 17 - Matemática e Raciocínio Lógico
        enunciado_q17 = (
            "QUESTÃO 17\n"
            "Em um lançamento simultâneo de dois dados, um dado de cor\n"
            "azul e um dado de cor amarela, calcule a probabilidade do\n"
            "resultado de em um único lançamento “sair a soma 10 (dez)”.\n"
            "Assinale a alternativa CORRETA."
        )
        q17 = get_or_create_questao(
            db,
            enunciado=enunciado_q17,
            disciplina=disciplina_matematica,
            dificuldade=DificuldadeEnum.MEDIO,
            orgao=orgao,
            instituicao=instituicao,
            banca=banca,
        )
        alternativas_q17 = [
            "0,08",
            "0,5",
            "0,1",
            "0,04",
            "0,125",
        ]
        ensure_alternativas(db, q17, alternativas_q17, indice_correta=0)  # A

        # Questão 21 - Legislação de Palmas/TO
        enunciado_q21 = (
            "QUESTÃO 21\n"
            "O município de Palmas tem a propriedade de um bem imóvel\n"
            "que se encontra atualmente desafetado, vazio, sem nenhuma\n"
            "utilização pública. A fim de fazer com que este imóvel seja\n"
            "ocupado e dada a ele uma função de interesse público, analise\n"
            "as afirmativas a seguir.\n"
            "I. Em casos de doação de bem público imóvel, pode haver\n"
            "dispensa de licitação, desde que seja destinada a outros\n"
            "entes da federação e conste da lei e da escritura pública\n"
            "os encargos do donatário, o prazo de seu cumprimento e\n"
            "a cláusula de retrocessão sob pena de nulidade do ato.\n"
            "II. O Município deve outorgar concessão de direito real de\n"
            "uso preferentemente à venda ou doação de seus bens\n"
            "imóveis, sendo dispensada a licitação quando o uso se\n"
            "destinar à concessionária de serviço público, a entidades\n"
            "assistenciais, ou quando houver relevante interesse\n"
            "público devidamente justificado.\n"
            "III. O uso de bens municipais por terceiros poderá ser feito\n"
            "mediante concessão, permissão ou autorização, não\n"
            "exigível, para essas situações, prévia autorização\n"
            "legislativa ou licitação, uma vez que o uso se dá a título\n"
            "precário e a propriedade do bem continua do município.\n"
            "IV. A autorização do uso de bem público poderá incidir sobre\n"
            "qualquer bem público, de uso comum, especial ou\n"
            "dominical, para atividades ou usos específicos e\n"
            "transitórios, por prazo máximo legalmente estabelecido.\n"
            "Assinale a alternativa CORRETA."
        )
        q21 = get_or_create_questao(
            db,
            enunciado=enunciado_q21,
            disciplina=disciplina_leg_palmas,
            dificuldade=DificuldadeEnum.MEDIO,
            orgao=orgao,
            instituicao=instituicao,
            banca=banca,
        )
        alternativas_q21 = [
            "Apenas as afirmativas I e III estão corretas.",
            "Apenas as afirmativas II e IV estão corretas.",
            "Apenas as afirmativas I e IV estão corretas.",
            "Apenas as afirmativas II e III estão corretas.",
            "Apenas as afirmativas I e II estão corretas.",
        ]
        ensure_alternativas(db, q21, alternativas_q21, indice_correta=1)  # B

        # Questão 24 - Legislação de Palmas/TO
        enunciado_q24 = (
            "QUESTÃO 24\n"
            "Assinale a alternativa INCORRETA sobre os direitos e\n"
            "vantagens dos servidores públicos municipais de Palmas,\n"
            "previstos no Estatuto dos Servidores Públicos da Administração\n"
            "Direta e Indireta dos Poderes do Município de Palmas."
        )
        q24 = get_or_create_questao(
            db,
            enunciado=enunciado_q24,
            disciplina=disciplina_leg_palmas,
            dificuldade=DificuldadeEnum.MEDIO,
            orgao=orgao,
            instituicao=instituicao,
            banca=banca,
        )
        alternativas_q24 = [
            "Nenhum servidor da administração direta ou indireta, de\n"
            "qualquer dos Poderes do Município, poderá perceber,\n"
            "mensalmente a título de remuneração ou provento,\n"
            "importância inferior ao salário mínimo ou superior ao\n"
            "subsídio mensal, em espécie, do Prefeito Municipal.",
            "Além do vencimento, poderão ser pagas ao servidor\n"
            "municipal as seguintes vantagens: indenizações, auxílios-\n"
            "pecuniários, gratificações e adicionais, sendo que apenas\n"
            "as duas últimas podem ser incorporadas aos vencimentos\n"
            "ou proventos, nos casos e condições previstos em lei.",
            "A ajuda de custo é um tipo de indenização destinada a\n"
            "compensar as despesas de instalação do servidor que, no\n"
            "interesse do serviço, passe a ter exercício em órgão ou\n"
            "repartição fora dos limites urbanos da sede, com mudança\n"
            "de domicílio em caráter permanente.",
            "Os auxílios pecuniários previstos na lei e que devem\n"
            "constar na folha de pagamento da administração pública\n"
            "municipal são: auxílio-funeral, auxílio-reclusão, salário-\n"
            "família e auxílio-transporte.",
            "Ao servidor ocupante de cargo de provimento efetivo ou ao\n"
            "estabilizado, investido em cargo de provimento em\n"
            "comissão ou em função de confiança, será devida\n"
            "gratificação fixada em lei própria.",
        ]
        ensure_alternativas(db, q24, alternativas_q24, indice_correta=3)  # D

        # Questão 27 - Administração
        enunciado_q27 = (
            "QUESTÃO 27\n"
            "Segundo Max Weber, as organizações formais ou burocráticas\n"
            "apresentam três características principais que as distinguem\n"
            "dos grupos informais ou primários.\n"
            "Assinale a alternativa CORRETA."
        )
        q27 = get_or_create_questao(
            db,
            enunciado=enunciado_q27,
            disciplina=disciplina_administracao,
            dificuldade=DificuldadeEnum.MEDIO,
            orgao=orgao,
            instituicao=instituicao,
            banca=banca,
        )
        alternativas_q27 = [
            "Impessoalidade: as burocracias são formadas por\n"
            "funcionários que são remunerados, obtendo os meios para\n"
            "a sua subsistência. As burocracias funcionam como\n"
            "sistemas de subsistência para os funcionários.",
            "Formalidade: as burocracias são essencialmente sistemas\n"
            "de normas. A figura da autoridade é definida pela lei, que\n"
            "tem como objetivo a racionalidade das decisões baseadas\n"
            "em critérios impessoais.",
            "Profissionalismo: as pessoas são ocupantes de cargos ou\n"
            "posições formais. Alguns dos cargos são de figuras de\n"
            "autoridades. A obediência é devida aos cargos, não aos\n"
            "ocupantes. Todas as pessoas seguem a lei.",
            "Economicidade: as burocracias são formadas por\n"
            "funcionários que são remunerados pelos menores salários\n"
            "possíveis. As burocracias funcionam como sistemas de\n"
            "subsistência para os funcionários.",
            "Controle: as pessoas são ocupantes de cargos ou\n"
            "posições formais que são objeto de controle esporádico.\n"
            "Alguns dos cargos são ocupados por figuras de autoridade,\n"
            "a quem se deve obediência pessoal, não baseada em leis.",
        ]
        ensure_alternativas(db, q27, alternativas_q27, indice_correta=1)  # B

        # Questão 30 - Administração
        enunciado_q30 = (
            "QUESTÃO 30\n"
            "A Higiene do Trabalho é reconhecida como uma ciência do\n"
            "reconhecimento, da avaliação e do controle dos riscos à saúde\n"
            "nas organizações, visando à previsão e mitigação das doenças\n"
            "ocupacionais, ou seja, relacionadas ao trabalho.\n"
            "A Higiene do Trabalho possui diversas finalidades, EXCETO:"
        )
        q30 = get_or_create_questao(
            db,
            enunciado=enunciado_q30,
            disciplina=disciplina_administracao,
            dificuldade=DificuldadeEnum.MEDIO,
            orgao=orgao,
            instituicao=instituicao,
            banca=banca,
        )
        alternativas_q30 = [
            "eliminação das causas das doenças profissionais.",
            "redução dos efeitos prejudiciais provocados pelo trabalho\n"
            "em pessoas doentes ou portadores de necessidades\n"
            "especiais.",
            "aumento dos salários dos trabalhadores em função de sua\n"
            "produtividade.",
            "prevenção do agravamento de doenças e de lesões.",
            "manutenção da saúde dos trabalhadores e aumento da\n"
            "produtividade, por meio de controle do ambiente de\n"
            "trabalho.",
        ]
        ensure_alternativas(db, q30, alternativas_q30, indice_correta=2)  # C

        # Questão 31 - Administração
        enunciado_q31 = (
            "QUESTÃO 31\n"
            "O modelo japonês de administração, uma versão aprimorada\n"
            "das técnicas e princípios ocidentais sobre a Administração\n"
            "tornou-se um modelo de abrangência global, sendo\n"
            "considerado um dos pilares que deve sustentar a capacidade\n"
            "de uma organização de competir no atual contexto econômico.\n"
            "Seus princípios vão além da aplicação em empresas privadas,\n"
            "servindo aos propósitos de qualquer tipo de organização que\n"
            "pretenda melhorar a qualidade de suas ações. Uma das\n"
            "empresas que melhor se utilizou destes princípios foi a Toyota\n"
            "e, não por acaso, o Sistema Toyota de Produção é um dos\n"
            "mais conhecidos e influentes do mundo, sobretudo quanto à\n"
            "eliminação de desperdícios.\n"
            "Quando a organização estabelece um fluxo contínuo de\n"
            "materiais, sincronizado com a programação do processo\n"
            "produtivo, objetivando minimizar a necessidade de estoques,\n"
            "está se utilizando da ideia de:"
        )
        q31 = get_or_create_questao(
            db,
            enunciado=enunciado_q31,
            disciplina=disciplina_administracao,
            dificuldade=DificuldadeEnum.MEDIO,
            orgao=orgao,
            instituicao=instituicao,
            banca=banca,
        )
        alternativas_q31 = [
            "Racionalização da força de trabalho.",
            "Just in time.",
            "Produção enxuta.",
            "Produção flexível.",
            "Círculos de Qualidade.",
        ]
        ensure_alternativas(db, q31, alternativas_q31, indice_correta=1)  # B

        print("✅ Seed inicial executado com sucesso.")
    except Exception as e:
        print(f"❌ Erro ao executar seed inicial: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    run()


