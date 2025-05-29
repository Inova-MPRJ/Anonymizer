from presidio_analyzer import PatternRecognizer, Pattern
import re

# Padrões para detectar nomes de escolas
escola_patterns = [
    # Escolas municipais, estaduais, federais
    Pattern(
        name="Escola Municipal/Estadual/Federal",
        regex=r"\b(?:Escola\s+(?:Municipal|Estadual|Federal|Particular)\s+[A-Z][a-z\s]+)\b",
        score=0.9
    ),
    # Colégios
    Pattern(
        name="Colégio",
        regex=r"\bColégio\s+[A-Z][a-z\s]+\b",
        score=0.9
    ),
    # Centros Educacionais
    Pattern(
        name="Centro Educacional",
        regex=r"\bCentro\s+Educacional\s+[A-Z][a-z\s]+\b",
        score=0.9
    ),
    # Institutos
    Pattern(
        name="Instituto",
        regex=r"\bInstituto\s+[A-Z][a-z\s]+\b",
        score=0.85
    ),
    # Universidades
    Pattern(
        name="Universidade",
        regex=r"\bUniversidade\s+[A-Z][a-z\s]+\b",
        score=0.9
    ),
    # Faculdades
    Pattern(
        name="Faculdade",
        regex=r"\bFaculdade\s+[A-Z][a-z\s]+\b",
        score=0.9
    ),
    # Abreviações específicas de São Paulo (EMEF, EMEI, CEI)
    Pattern(
        name="Escolas SP Abrev",
        regex=r"\b(?:EMEF|EMEI|CEI|CIEJA)\s+[A-Z][a-z\s]+\b",
        score=0.95
    ),
    # Abreviações gerais (E.M., E.E.)
    Pattern(
        name="Escolas Abrev Gerais",
        regex=r"\b(?:E\.M\.|E\.E\.|E\.F\.)\s+[A-Z][a-z\s]+\b",
        score=0.9
    ),
    # Campus universitários
    Pattern(
        name="Campus",
        regex=r"\bCampus\s+[A-Z][a-z\s]+\b",
        score=0.85
    )
]

# Criando o reconhecedor personalizado para escolas
class EscolaRecognizer(PatternRecognizer):
    def __init__(self):
        super().__init__(
            supported_entity="ESCOLA",
            patterns=escola_patterns,
            supported_language="pt",
            context=[
                "escola", "colégio", "universidade", "faculdade", "instituto",
                "centro educacional", "campus", "educação", "ensino",
                "estudante", "aluno", "professor", "matrícula",
                "municipal", "estadual", "federal", "particular",
                "educacional", "pedagógico"
            ]
        )

