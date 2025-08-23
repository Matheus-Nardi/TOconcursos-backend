-- SQL Import Script - Concurso Tocantins

-- Inserindo dados na tabela 'bancas'
INSERT INTO bancas (id, nome) VALUES
(1, 'COPESE/UFT'),
(2, 'Cebraspe'),
(3, 'FGV'),
(4, 'AOCP');

-- Inserindo dados na tabela 'dificuldades'
INSERT INTO dificuldades (id, nome) VALUES
(1, 'Fácil'),
(2, 'Média'),
(3, 'Difícil');

-- Inserindo dados na tabela 'instituicoes'
INSERT INTO instituicoes (id, nome) VALUES
(1, 'Prefeitura de Palmas'),
(2, 'Governo do Estado do Tocantins'),
(3, 'Assembleia Legislativa do Tocantins'),
(4, 'Universidade Federal do Tocantins (UFT)');

-- Inserindo dados na tabela 'questoes'
INSERT INTO questoes (id, enunciado, instituicao_id, dificuldade_id, banca_id) VALUES
-- Bloco 1: História e Geografia do Tocantins
(1, 'O Estado do Tocantins foi oficialmente criado pela Constituição Federal de 1988, sendo desmembrado de qual outro estado brasileiro?', 2, 1, 1),
(2, 'Qual é o nome da maior ilha fluvial do mundo, localizada no estado do Tocantins?', 2, 1, 2),
(3, 'A capital do Tocantins, Palmas, foi projetada e construída especificamente para ser a sede do governo do novo estado. Em que ano ela foi fundada?', 1, 2, 3),
(4, 'O Parque Estadual do Jalapão, um dos principais destinos turísticos do Tocantins, é famoso por suas paisagens únicas. Qual das seguintes características NÃO corresponde ao Jalapão?', 2, 2, 1),
(5, 'O "Bico do Papagaio" é uma importante região geográfica, social e econômica do Tocantins. Ela está localizada no:', 3, 2, 4),

-- Bloco 2: Legislação e Administração Pública (Estadual)
(6, 'De acordo com a Constituição do Estado do Tocantins, o Poder Executivo é exercido pelo Governador do Estado, auxiliado pelos:', 3, 2, 2),
(7, 'Qual o nome do primeiro governador do estado do Tocantins, figura central no movimento autonomista que levou à criação do estado?', 3, 2, 3),
(8, 'A Usina Hidrelétrica de Lajeado, uma importante fonte de energia para o estado e para o país, está localizada em qual rio?', 2, 1, 1),
(9, 'O Palácio Araguaia, sede do Poder Executivo do Governo do Tocantins, está localizado em qual cidade?', 1, 1, 4),

-- Bloco 3: Conhecimentos Gerais e Atualidades do Tocantins
(10, 'A economia do Tocantins tem como um de seus pilares principais a:', 2, 2, 3),
(11, 'Qual município do Tocantins é conhecido nacionalmente por suas praias de rio e por ser um polo turístico durante a temporada de veraneio?', 1, 1, 2),
(12, 'A Universidade Federal do Tocantins (UFT) é a principal instituição de ensino superior do estado. Seu campus principal está localizado em:', 4, 1, 1),
(13, 'A culinária tocantinense é rica e diversificada. Um prato típico da região, feito à base de carne de sol desfiada, farinha e temperos, é o(a):', 2, 2, 4),
(14, 'O Monumento aos Dezoito do Forte de Copacabana, localizado na Praça dos Girassóis em Palmas, homenageia um importante evento da história do Brasil. Qual evento é esse?', 1, 3, 2),

-- Bloco 4: Português e Raciocínio Lógico (Contextualizado)
(15, 'Na frase "O Tocantins, que é o mais novo estado da federação, possui belezas naturais exuberantes.", o trecho "que é o mais novo estado da federação" exerce a função sintática de:', 4, 2, 3),
(16, 'Considerando a palavra "TOCANTINS", quantos anagramas (permutações das letras) podem ser formados?', 4, 3, 1),
(17, 'Um servidor público de Palmas trabalha 6 horas por dia e analisa 20 processos. Se ele passar a trabalhar 8 horas por dia, mantendo a mesma produtividade, quantos processos analisará?', 1, 1, 4),
(18, 'Assinale a alternativa em que a concordância verbal está INCORRETA, considerando o contexto tocantinense.', 3, 2, 2),
(19, 'Se a população de Palmas era de aproximadamente 300.000 habitantes e cresceu 10% em dois anos, qual a população aproximada após esse período?', 1, 1, 3),
(20, 'Identifique a figura de linguagem presente na frase: "O Rio Tocantins abraça a cidade de Miracema com suas águas."', 4, 2, 1);

-- Inserindo dados na tabela 'alternativas'
-- Respostas para a Questão 1
INSERT INTO alternativas (id, descricao, is_correta, questao_id) VALUES
(1, 'Goiás', TRUE, 1),
(2, 'Mato Grosso', FALSE, 1),
(3, 'Pará', FALSE, 1),
(4, 'Maranhão', FALSE, 1),
(5, 'Bahia', FALSE, 1);

-- Respostas para a Questão 2
INSERT INTO alternativas (id, descricao, is_correta, questao_id) VALUES
(6, 'Ilha do Bananal', TRUE, 2),
(7, 'Ilha de Marajó', FALSE, 2),
(8, 'Ilha do Mel', FALSE, 2),
(9, 'Ilha Grande', FALSE, 2),
(10, 'Arquipélago de Anavilhanas', FALSE, 2);

-- Respostas para a Questão 3
INSERT INTO alternativas (id, descricao, is_correta, questao_id) VALUES
(11, '1988', FALSE, 3),
(12, '1989', TRUE, 3),
(13, '1990', FALSE, 3),
(14, '1991', FALSE, 3),
(15, '1987', FALSE, 3);

-- Respostas para a Questão 4
INSERT INTO alternativas (id, descricao, is_correta, questao_id) VALUES
(16, 'Dunas de areia dourada', FALSE, 4),
(17, 'Fervedouros de água cristalina', FALSE, 4),
(18, 'Cachoeiras e rios', FALSE, 4),
(19, 'Plantações de soja em larga escala', TRUE, 4),
(20, 'Formações rochosas, como a Pedra Furada', FALSE, 4);

-- Respostas para a Questão 5
INSERT INTO alternativas (id, descricao, is_correta, questao_id) VALUES
(21, 'Extremo Norte do estado, na confluência dos rios Araguaia e Tocantins.', TRUE, 5),
(22, 'Região Sul do estado, na divisa com Goiás.', FALSE, 5),
(23, 'Região Central, nos arredores de Palmas.', FALSE, 5),
(24, 'A Leste, na divisa com a Bahia e o Piauí.', FALSE, 5),
(25, 'A Oeste, na Ilha do Bananal.', FALSE, 5);

-- Respostas para a Questão 6
INSERT INTO alternativas (id, descricao, is_correta, questao_id) VALUES
(26, 'Deputados Estaduais', FALSE, 6),
(27, 'Secretários de Estado', TRUE, 6),
(28, 'Desembargadores do Tribunal de Justiça', FALSE, 6),
(29, 'Prefeitos das cidades', FALSE, 6),
(30, 'Membros do Ministério Público', FALSE, 6);

-- Respostas para a Questão 7
INSERT INTO alternativas (id, descricao, is_correta, questao_id) VALUES
(31, 'Mauro Carlesse', FALSE, 7),
(32, 'Marcelo Miranda', FALSE, 7),
(33, 'José Wilson Siqueira Campos', TRUE, 7),
(34, 'Moisés Avelino', FALSE, 7),
(35, 'Carlos Gaguim', FALSE, 7);

-- Respostas para a Questão 8
INSERT INTO alternativas (id, descricao, is_correta, questao_id) VALUES
(36, 'Rio Araguaia', FALSE, 8),
(37, 'Rio Formoso', FALSE, 8),
(38, 'Rio Javaés', FALSE, 8),
(39, 'Rio do Sono', FALSE, 8),
(40, 'Rio Tocantins', TRUE, 8);

-- Respostas para a Questão 9
INSERT INTO alternativas (id, descricao, is_correta, questao_id) VALUES
(41, 'Araguaína', FALSE, 9),
(42, 'Gurupi', FALSE, 9),
(43, 'Palmas', TRUE, 9),
(44, 'Porto Nacional', FALSE, 9),
(45, 'Paraíso do Tocantins', FALSE, 9);

-- Respostas para a Questão 10
INSERT INTO alternativas (id, descricao, is_correta, questao_id) VALUES
(46, 'Indústria de tecnologia', FALSE, 10),
(47, 'Extrativismo mineral', FALSE, 10),
(48, 'Turismo de luxo', FALSE, 10),
(49, 'Agronegócio, especialmente a produção de grãos e a pecuária.', TRUE, 10),
(50, 'Indústria automobilística', FALSE, 10);

-- Respostas para a Questão 11
INSERT INTO alternativas (id, descricao, is_correta, questao_id) VALUES
(51, 'Dianópolis', FALSE, 11),
(52, 'Araguaína', FALSE, 11),
(53, 'Gurupi', FALSE, 11),
(54, 'Araguatins', FALSE, 11),
(55, 'Araguanã', TRUE, 11);

-- Respostas para a Questão 12
INSERT INTO alternativas (id, descricao, is_correta, questao_id) VALUES
(56, 'Araguaína', FALSE, 12),
(57, 'Gurupi', FALSE, 12),
(58, 'Porto Nacional', FALSE, 12),
(59, 'Palmas', TRUE, 12),
(60, 'Miracema do Tocantins', FALSE, 12);

-- Respostas para a Questão 13
INSERT INTO alternativas (id, descricao, is_correta, questao_id) VALUES
(61, 'Paçoca de carne de sol', TRUE, 13),
(62, 'Feijoada', FALSE, 13),
(63, 'Acarajé', FALSE, 13),
(64, 'Churrasco', FALSE, 13),
(65, 'Moqueca', FALSE, 13);

-- Respostas para a Questão 14
INSERT INTO alternativas (id, descricao, is_correta, questao_id) VALUES
(66, 'Guerra do Paraguai', FALSE, 14),
(67, 'Revolta da Vacina', FALSE, 14),
(68, 'Revolução de 1930', FALSE, 14),
(69, 'Levante dos 18 do Forte de Copacabana', TRUE, 14),
(70, 'Guerra de Canudos', FALSE, 14);

-- Respostas para a Questão 15
INSERT INTO alternativas (id, descricao, is_correta, questao_id) VALUES
(71, 'Aposto explicativo', TRUE, 15),
(72, 'Vocativo', FALSE, 15),
(73, 'Predicativo do sujeito', FALSE, 15),
(74, 'Objeto direto', FALSE, 15),
(75, 'Adjunto adverbial', FALSE, 15);

-- Respostas para a Questão 16
INSERT INTO alternativas (id, descricao, is_correta, questao_id) VALUES
(76, '362.880', FALSE, 16),
(77, '1.814.400', FALSE, 16),
(78, '907.200', TRUE, 16),
(79, '3.628.800', FALSE, 16),
(80, '453.600', FALSE, 16);

-- Respostas para a Questão 17
INSERT INTO alternativas (id, descricao, is_correta, questao_id) VALUES
(81, 'Aproximadamente 23 processos', FALSE, 17),
(82, 'Aproximadamente 25 processos', FALSE, 17),
(83, 'Aproximadamente 27 processos', TRUE, 17),
(84, '30 processos', FALSE, 17),
(85, '20 processos', FALSE, 17);

-- Respostas para a Questão 18
INSERT INTO alternativas (id, descricao, is_correta, questao_id) VALUES
(86, 'Fazem cinco anos que Palmas foi fundada.', TRUE, 18),
(87, 'A maioria dos turistas visitou o Jalapão.', FALSE, 18),
(88, 'Houve muitos eventos na Praia da Graciosa.', FALSE, 18),
(89, 'Existe muitas praias de rio no Tocantins.', FALSE, 18),
(90, 'Mais de um político compareceu à cerimônia.', FALSE, 18);

-- Respostas para a Questão 19
INSERT INTO alternativas (id, descricao, is_correta, questao_id) VALUES
(91, '310.000', FALSE, 19),
(92, '320.000', FALSE, 19),
(93, '330.000', TRUE, 19),
(94, '340.000', FALSE, 19),
(95, '360.000', FALSE, 19);

-- Respostas para a Questão 20
INSERT INTO alternativas (id, descricao, is_correta, questao_id) VALUES
(96, 'Metáfora', FALSE, 20),
(97, 'Hipérbole', FALSE, 20),
(98, 'Eufemismo', FALSE, 20),
(99, 'Ironia', FALSE, 20),
(100, 'Prosopopeia (ou Personificação)', TRUE, 20);