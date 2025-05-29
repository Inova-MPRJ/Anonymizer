from presidio_analyzer import PatternRecognizer, Pattern
import re

# Padrões para detectar endereços brasileiros
endereco_patterns = [
    # Logradouros com tipos específicos + nome + número (case insensitive)
    Pattern(
        name="Logradouro Completo",
        regex=r"(?i)\b(?:rua|avenida|av\.|r\.|alameda|travessa|estrada|rodovia|praça|largo|quadra|qd|conjunto|conj\.)\s+[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s]+,?\s*(?:n[ºo°]?\s*)?\d+",
        score=0.95
    ),
    # CEP brasileiro (formato: 12345-678 ou 12345678)
    Pattern(
        name="CEP",
        regex=r"\b\d{5}-?\d{3}\b",
        score=0.99
    ),
    # Endereços com "número" explícito (case insensitive)
    Pattern(
        name="Endereço com Número",
        regex=r"(?i)\b(?:rua|avenida|av\.|r\.|alameda|travessa|estrada|rodovia|praça|largo)\s+[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s]+,?\s*(?:número|nº|n°|n\.)\s*\d+",
        score=0.95
    ),
    # Bairros (precedidos por palavras indicativas) - case insensitive
    Pattern(
        name="Bairro",
        regex=r"(?i)\b(?:bairro|no bairro|do bairro)\s+[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s]+\b",
        score=0.85
    ),
    # Cidade + Estado (formato: Cidade - UF ou Cidade/UF) - case insensitive
    Pattern(
        name="Cidade Estado",
        regex=r"(?i)\b[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s]+\s*[-/]\s*[a-zA-Z]{2}\b",
        score=0.90
    ),
    # Complementos de endereço - case insensitive
    Pattern(
        name="Complemento",
        regex=r"(?i)\b(?:apartamento|apto|apt|casa|bloco|bl|andar|sala|loja|sobreloja)\s+\w+",
        score=0.80
    ),
    # Endereços rurais - case insensitive
    Pattern(
        name="Endereço Rural",
        regex=r"(?i)\b(?:sítio|fazenda|chácara|estância)\s+[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s]+\b",
        score=0.85
    ),
    # Condomínios e residenciais - case insensitive
    Pattern(
        name="Condomínio",
        regex=r"(?i)\b(?:condomínio|residencial|conjunto habitacional|vila)\s+[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s]+\b",
        score=0.85
    ),
    # Endereços com km (rodovias) - case insensitive
    Pattern(
        name="Rodovia KM",
        regex=r"(?i)\b(?:rodovia|rod\.|br|sp|rj|mg)\s*-?\s*\d+,?\s*[km]+\s*\d+",
        score=0.90
    ),
    # Endereço completo com bairro e cidade (mais específico para o caso)
    Pattern(
        name="Endereço Completo com Localização",
        regex=r"(?i)\b(?:rua|avenida|av\.|r\.|alameda|travessa|estrada)\s+[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s]+,\s*\d+,\s*[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s]+,\s*[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s]+",
        score=0.98
    ),
    # Nomes de ruas/avenidas específicos quando precedidos por "na/no/da/do"
    Pattern(
        name="Logradouro com Preposição",
        regex=r"(?i)\b(?:na|no|da|do)\s+(?:rua|avenida|av\.|r\.|alameda|travessa|estrada|rodovia|praça|largo)\s+[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s]+",
        score=0.90
    ),
    # Situado/localizado + endereço
    Pattern(
        name="Endereço com Localização",
        regex=r"(?i)\b(?:situada|situado|localizada|localizado)\s+(?:na|no|em|à)\s+(?:rua|avenida|av\.|r\.|alameda|travessa|estrada)\s+[a-zA-ZÀ-ÿ][a-zA-ZÀ-ÿ\s,\d]+",
        score=0.95
    )
]

class EnderecoRecognizer(PatternRecognizer):
    def __init__(self):
        super().__init__(
            supported_entity="ENDEREÇO",
            patterns=endereco_patterns,
            supported_language="pt",
            context=[
                # Tipos de logradouro
                'endereço', 'rua', 'avenida', 'alameda', 'travessa', 'estrada', 'rodovia',
                'praça', 'largo', 'quadra', 'conjunto', 'condomínio', 'residencial',
                
                # Indicadores de localização
                'bairro', 'cidade', 'estado', 'município', 'CEP', 'cep',
                'localizado', 'situada', 'localizada', 'endereçado', 'situado',
                
                # Verbos relacionados
                'mora', 'reside', 'localiza', 'situa', 'fica', 'encontra',
                
                # Complementos
                'número', 'nº', 'apartamento', 'apto', 'casa', 'bloco', 'andar',
                'sala', 'loja', 'sobreloja', 'complemento', 'km', 'quilômetro',
                
                # Indicadores contextuais
                'no endereço', 'na rua', 'na avenida', 'residente em',
                'domiciliado', 'com endereço', 'endereço residencial',
                'endereço comercial', 'correspondência', 'situada na',
                'situado na', 'localizada na', 'localizado na'
            ]
        )