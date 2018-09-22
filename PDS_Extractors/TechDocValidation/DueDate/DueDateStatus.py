from enum import Enum


class DueDateStatus(Enum):
    Valid = "Valido"
    Invalid = "Invalido"
    Modified_Valid = "Modificado Valido"
    Modified_Invalid = "Modificado Invalido"
    New = "Novo"
    Canceled = "Cancelado"
    NoEffect = "Sem Efeito"
    InvertedSequence = "Sequencia Invertida"
    NoConclusion = "Inconclusivo"
