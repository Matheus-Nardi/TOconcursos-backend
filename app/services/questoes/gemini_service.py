import os
from dotenv import load_dotenv
from google import genai
from core.exceptions.exception import NotFoundException
from repository.questoes.questao_repository import QuestaoRepository
from sqlalchemy.orm import Session

# Tenta carregar o .env (útil para desenvolvimento local)
# No Docker, as variáveis já vêm do docker-compose.yml
load_dotenv()

class GeminiService:
    """Service para integração com a API do Gemini"""
    
    def __init__(self, db: Session):
        self.db = db
        self.questao_repo = QuestaoRepository(db)
        # Busca a variável de ambiente (já carregada pelo Docker Compose ou .env)
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY não encontrada nas variáveis de ambiente. Certifique-se de adicionar GEMINI_API_KEY no arquivo .env na raiz do projeto e reiniciar o container.")
        
        # O Client pode usar a variável de ambiente GEMINI_API_KEY automaticamente
        # ou podemos passar explicitamente via api_key
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.5-flash"
    
    def gerar_resposta_questao(self, questao_id: int) -> str:
        """
        Gera uma resposta curta e objetiva para uma questão usando o Gemini.
        
        Args:
            questao_id: ID da questão
            
        Returns:
            Resposta gerada pelo Gemini
            
        Raises:
            NotFoundException: Se a questão não for encontrada
        """
        # Busca a questão com suas alternativas
        questao = self.questao_repo.get_questao(questao_id)
        
        if not questao:
            raise NotFoundException(f"Questão com id {questao_id} não encontrada")
        
        # Monta o prompt com o enunciado e alternativas
        prompt = self._montar_prompt(questao)
        
        try:
            # Chama a API do Gemini
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            return response.text.strip()
            
        except Exception as e:
            raise Exception(f"Erro ao gerar resposta com Gemini: {str(e)}")
    
    def _montar_prompt(self, questao) -> str:
        """
        Monta o prompt formatado para o Gemini com o enunciado e alternativas.
        
        Args:
            questao: Objeto Questao do banco de dados
            
        Returns:
            Prompt formatado como string
        """
        # Monta a lista de alternativas (ordena por ID para garantir ordem consistente)
        alternativas_ordenadas = sorted(questao.alternativas, key=lambda alt: alt.id)
        alternativas_texto = []
        for i, alt in enumerate(alternativas_ordenadas, start=1):
            letra = chr(64 + i)  # A, B, C, D, E...
            alternativas_texto.append(f"{letra}) {alt.descricao}")
        
        alternativas_str = "\n".join(alternativas_texto)
        
        prompt = f"""Analise a seguinte questão de concurso e forneça uma resposta curta e objetiva explicando a solução.

ENUNCIADO:
{questao.enunciado}

ALTERNATIVAS:
{alternativas_str}

Por favor, forneça uma explicação curta e objetiva (máximo de 150 palavras) sobre como resolver esta questão, indicando qual é a alternativa correta e o motivo."""
        
        return prompt

