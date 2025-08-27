import enum

class DificuldadeEnum(str, enum.Enum):
    """
    Enum para os níveis de dificuldade das questões.
    """
    FACIL = "facil"
    MEDIO = "medio"
    DIFICIL = "dificil"