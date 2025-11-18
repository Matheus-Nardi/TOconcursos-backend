-- Script para inserir dados de teste no banco TOconcursos
-- Execute este script no pgAdmin para criar questões de teste

-- Limpar dados existentes (opcional - remova se não quiser apagar dados)
-- DELETE FROM alternativas;
-- DELETE FROM questoes;
-- DELETE FROM bancas;
-- DELETE FROM disciplinas;
-- DELETE FROM instituicoes;
-- DELETE FROM orgaos;

-- 1. Inserir Bancas
INSERT INTO bancas (id, label) VALUES 
(1, 'Cespe'),
(2, 'Fgv'),
(3, 'Vunesp'),
(4, 'Fcc'),
(5, 'Cesgranrio')
ON CONFLICT (id) DO NOTHING;

-- 2. Inserir Disciplinas
INSERT INTO disciplinas (id, label) VALUES 
(1, 'Português'),
(2, 'Matemática'),
(3, 'Direito Constitucional'),
(4, 'Direito Administrativo'),
(5, 'Informática')
ON CONFLICT (id) DO NOTHING;

-- 3. Inserir Órgãos
INSERT INTO orgaos (id, label) VALUES 
(1, 'Polícia Federal'),
(2, 'Receita Federal'),
(3, 'Tribunal de Justiça'),
(4, 'Prefeitura Municipal'),
(5, 'Ministério Público')
ON CONFLICT (id) DO NOTHING;

-- 4. Inserir Instituições
INSERT INTO instituicoes (id, label) VALUES 
(1, 'União'),
(2, 'Estado'),
(3, 'Município'),
(4, 'Autarquia Federal'),
(5, 'Empresa Pública')
ON CONFLICT (id) DO NOTHING;

-- 5. Inserir Questões
INSERT INTO questoes (id, enunciado, ja_respondeu, id_disciplina, dificuldade, id_orgao, id_instituicao, id_banca) VALUES 

-- Questão 1 - Português/Cespe
(1, 'Analise as assertivas abaixo sobre concordância verbal:

I - O verbo concorda com o sujeito em número e pessoa.
II - Em casos de sujeito composto, o verbo vai sempre para o plural.
III - Com expressões partitivas, o verbo pode concordar com o núcleo ou com o especificador.

Está(ão) correta(s):', 
false, 1, 'MEDIO', 1, 1, 1),

-- Questão 2 - Matemática/FGV
(2, 'Um investidor aplicou R$ 10.000,00 a juros compostos de 2% ao mês. Após 3 meses, qual será o montante aproximado?', 
false, 2, 'FACIL', 2, 2, 2),

-- Questão 3 - Direito Constitucional/Vunesp
(3, 'Sobre os direitos fundamentais na Constituição Federal de 1988, assinale a alternativa INCORRETA:', 
false, 3, 'DIFICIL', 3, 2, 3),

-- Questão 4 - Direito Administrativo/FCC
(4, 'O princípio da supremacia do interesse público sobre o privado:

A) É absoluto e não admite relativização.
B) Deve ser ponderado com outros princípios constitucionais.
C) Só se aplica em casos de desapropriação.
D) É incompatível com o Estado Democrático de Direito.
E) Não está previsto na Constituição Federal.', 
false, 4, 'MEDIO', 4, 1, 4),

-- Questão 5 - Informática/Cesgranrio
(5, 'No Microsoft Excel, qual função é utilizada para contar células que atendem a um critério específico?', 
false, 5, 'FACIL', 5, 3, 5)

ON CONFLICT (id) DO NOTHING;

-- 6. Inserir Alternativas para cada questão

-- Alternativas para Questão 1 (Português)
INSERT INTO alternativas (id, descricao, explicacao, is_correta, id_questao) VALUES 
(1, 'Apenas I e II estão corretas.', 'A assertiva III também está correta.', false, 1),
(2, 'Apenas I e III estão corretas.', 'Explicação: I está correto - regra básica de concordância. II está incorreto - há exceções como "nem um nem outro". III está correto - com expressões como "a maioria de", "parte de".', true, 1),
(3, 'Apenas II e III estão corretas.', 'A assertiva I é fundamental e está correta.', false, 1),
(4, 'Todas as assertivas estão corretas.', 'A assertiva II possui exceções.', false, 1),
(5, 'Nenhuma assertiva está correta.', 'Pelo menos duas assertivas estão corretas.', false, 1);

-- Alternativas para Questão 2 (Matemática)
INSERT INTO alternativas (id, descricao, explicacao, is_correta, id_questao) VALUES 
(6, 'R$ 10.200,00', 'Aplicou apenas juros simples.', false, 2),
(7, 'R$ 10.600,00', 'Não considerou o regime de capitalização composta.', false, 2),
(8, 'R$ 10.612,08', 'Explicação: M = C(1+i)^n = 10000(1,02)^3 = 10000 × 1,061208 = R$ 10.612,08', true, 2),
(9, 'R$ 10.800,00', 'Erro de cálculo.', false, 2),
(10, 'R$ 11.000,00', 'Valor muito alto para o período.', false, 2);

-- Alternativas para Questão 3 (Direito Constitucional)
INSERT INTO alternativas (id, descricao, explicacao, is_correta, id_questao) VALUES 
(11, 'Os direitos fundamentais têm aplicabilidade imediata.', 'Correto, conforme art. 5º, §1º da CF/88.', false, 3),
(12, 'Os direitos sociais são direitos fundamentais de segunda geração.', 'Correto, classificação doutrinária aceita.', false, 3),
(13, 'Os direitos fundamentais são absolutos e não admitem limitações.', 'Explicação: INCORRETA. Os direitos fundamentais podem ser limitados por outros direitos fundamentais e pelo interesse público, através do princípio da proporcionalidade.', true, 3),
(14, 'O direito à vida é um direito fundamental básico.', 'Correto, previsto no art. 5º, caput.', false, 3),
(15, 'Os estrangeiros têm direitos fundamentais no Brasil.', 'Correto, o art. 5º estende proteção aos estrangeiros residentes.', false, 3);

-- Alternativas para Questão 4 (Direito Administrativo)
INSERT INTO alternativas (id, descricao, explicacao, is_correta, id_questao) VALUES 
(16, 'É absoluto e não admite relativização.', 'Incorreto, deve ser ponderado.', false, 4),
(17, 'Deve ser ponderado com outros princípios constitucionais.', 'Explicação: Correto. O princípio da supremacia do interesse público deve ser aplicado com proporcionalidade e ponderado com outros princípios como dignidade da pessoa humana e direitos fundamentais.', true, 4),
(18, 'Só se aplica em casos de desapropriação.', 'Incorreto, aplica-se em várias situações.', false, 4),
(19, 'É incompatível com o Estado Democrático de Direito.', 'Incorreto, é compatível quando aplicado corretamente.', false, 4),
(20, 'Não está previsto na Constituição Federal.', 'Embora implícito, é reconhecido pela doutrina.', false, 4);

-- Alternativas para Questão 5 (Informática)
INSERT INTO alternativas (id, descricao, explicacao, is_correta, id_questao) VALUES 
(21, 'CONT.SE', 'Explicação: A função CONT.SE (COUNTIF em inglês) conta células que atendem a um critério específico. Sintaxe: =CONT.SE(intervalo; critério)', true, 5),
(22, 'SOMA.SE', 'Esta função soma valores, não conta células.', false, 5),
(23, 'CONT.NÚM', 'Esta função conta apenas células numéricas, sem critério específico.', false, 5),
(24, 'CONTAR', 'Esta função conta células não vazias, sem critério específico.', false, 5),
(25, 'MEDIA.SE', 'Esta função calcula média, não conta células.', false, 5);

-- Reset das sequences para próximos inserções (opcional)
SELECT setval('bancas_id_seq', (SELECT MAX(id) FROM bancas));
SELECT setval('disciplinas_id_seq', (SELECT MAX(id) FROM disciplinas));
SELECT setval('orgaos_id_seq', (SELECT MAX(id) FROM orgaos));
SELECT setval('instituicoes_id_seq', (SELECT MAX(id) FROM instituicoes));
SELECT setval('questoes_id_seq', (SELECT MAX(id) FROM questoes));
SELECT setval('alternativas_id_seq', (SELECT MAX(id) FROM alternativas));

-- Consultas para verificar os dados inseridos
SELECT 'BANCAS CRIADAS:' as tipo;
SELECT id, label FROM bancas ORDER BY id;

SELECT 'DISCIPLINAS CRIADAS:' as tipo;
SELECT id, label FROM disciplinas ORDER BY id;

SELECT 'QUESTÕES CRIADAS:' as tipo;
SELECT 
    q.id,
    LEFT(q.enunciado, 50) || '...' as enunciado_resumo,
    d.label as disciplina,
    q.dificuldade,
    b.label as banca
FROM questoes q
JOIN disciplinas d ON q.id_disciplina = d.id  
JOIN bancas b ON q.id_banca = b.id
ORDER BY q.id;

SELECT 'ALTERNATIVAS POR QUESTÃO:' as tipo;
SELECT 
    a.id_questao,
    COUNT(*) as total_alternativas,
    SUM(CASE WHEN a.is_correta THEN 1 ELSE 0 END) as alternativas_corretas
FROM alternativas a 
GROUP BY a.id_questao 
ORDER BY a.id_questao;
