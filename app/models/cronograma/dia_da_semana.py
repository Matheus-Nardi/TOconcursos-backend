import enum

class DiaDaSemanaEnum(str, enum.Enum):
    """
    Enum para os dias da semana
    """
    DOMINGO = "domingo"
    SEGUNDA = "segunda"
    TERCA = "terca"
    QUARTA = "quarta"
    QUINTA = "quinta"
    SEXTA = "sexta"
    SABADO = "sabado"
