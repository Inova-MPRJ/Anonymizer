from presidio_analyzer import PatternRecognizer, Pattern, RecognizerRegistry
import re

# Expressão regular básica para CPF (aceita formatos com ou sem pontuação)
cpf_pattern = Pattern(
    name="CPF Pattern",
    regex=r"\b\d{3}\.?\d{3}\.?\d{3}-?\d{2}\b",
    score=0.85
)

# Criando o reconhecedor personalizado
class CPFRecognizer(PatternRecognizer):
    def __init__(self):
        super().__init__(
            supported_entity="CPF",
            patterns=[cpf_pattern],
            supported_language="pt"
        )

