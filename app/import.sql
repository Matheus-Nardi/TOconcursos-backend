-- OPCIONAL: limpar dados anteriores de testes
-- (use só se tiver certeza que pode apagar!)
-- TRUNCATE TABLE alternativas, questoes, disciplinas, orgaos, instituicoes, bancas
-- RESTART IDENTITY CASCADE;

-- 1) Tabelas de apoio (disciplinas, orgaos, instituicoes, bancas)

INSERT INTO disciplinas (id, label) VALUES
  (1, 'Língua Portuguesa'),
  (2, 'Historia e Geografia do Tocantins');

INSERT INTO orgaos (id, label) VALUES
  (1, 'Prefeitura Municipal de Palmas');

INSERT INTO instituicoes (id, label) VALUES
  (1, 'UFTCOPESE');

INSERT INTO bancas (id, label) VALUES
  (1, 'UFTCOPESE');

-- 2) Questões (usando os IDs acima)
-- dificuldade: 'medio', 'medio', 'facil'

INSERT INTO questoes (id, enunciado, id_disciplina, dificuldade, id_orgao, id_instituicao, id_banca) VALUES
  (1, 'QUESTÃO 08
Assinale a alternativa CORRETA que indique a sequência de
verbos adequados nas frases.
I. _____no discurso o início de seus estudos.
II. A próxima _______legislativa iniciará em 24 de fevereiro.
III. O projeto apresentado veio ____ objetivos dos
trabalhadores, atendendo às suas reivindicações.', 1, 'medio', 1, 1, 1),

  (2, 'QUESTÃO 10
Em textos oficiais, deve-se evitar a fragmentação de frases,
uma vez que esse recurso estilístico dificulta a compreensão.
Assinale a alternativa que apresenta o uso da fragmentação
frasal de forma INCORRETA.', 1, 'medio', 1, 1, 1),

  (3, 'QUESTÃO 14
O Tocantins tem destaque na produção agrícola, tanto regional
quanto nacional. Nos últimos anos teve aumento considerável
na área plantada e na produção agrícola.
Assinale a alternativa CORRETA que indica os principais grãos
produzido no estado.', 2, 'facil', 1, 1, 1);

-- 3) Alternativas da Q8 (correta = A)

INSERT INTO alternativas (id, descricao, explicacao, is_correta, id_questao) VALUES
  (1, 'Evocou; sessão; ao encontro dos.', NULL, TRUE, 1),
  (2, 'Avocou; sessão; de encontro aos.', NULL, FALSE, 1),
  (3, 'Invocou; seção; ao encontro dos.', NULL, FALSE, 1),
  (4, 'Evocou; cessão; de encontro aos.', NULL, FALSE, 1),
  (5, 'Avocou; seção; ao encontro dos.', NULL, FALSE, 1);

-- 4) Alternativas da Q10 (correta = D)

INSERT INTO alternativas (id, descricao, explicacao, is_correta, id_questao) VALUES
  (6, 'O documento foi aprovado no Comitê, após ampla
discussão.', NULL, FALSE, 2),
  (7, 'Após ampla discussão, o documento foi aprovado no
Comitê.', NULL, FALSE, 2),
  (8, 'O documento, após ampla discussão, foi aprovado no
Comitê.', NULL, FALSE, 2),
  (9, 'O documento foi aprovado no Comitê. Após, ampla
discussão.', NULL, TRUE, 2),
  (10, 'Depois de ampla discussão, o documento foi aprovado no
Comitê.', NULL, FALSE, 2);

-- 5) Alternativas da Q14 (correta = B)

INSERT INTO alternativas (id, descricao, explicacao, is_correta, id_questao) VALUES
  (11, 'Soja, trigo e aveia.', NULL, FALSE, 3),
  (12, 'Soja, milho e arroz.', NULL, TRUE, 3),
  (13, 'Milho, centeio e trigo.', NULL, FALSE, 3),
  (14, 'Soja, cevada e centeio.', NULL, FALSE, 3),
  (15, 'Arroz, trigo e cevada.', NULL, FALSE, 3);