from presidio_analyzer import AnalyzerEngine, RecognizerRegistry, PatternRecognizer
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer.predefined_recognizers import SpacyRecognizer, EmailRecognizer, PhoneRecognizer
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_analyzer.recognizer_result import RecognizerResult

from tools.recognizers.cpf import CPFRecognizer
from tools.recognizers.escola import EscolaRecognizer
from tools.recognizers.endereços import EnderecoRecognizer

from typing import List
from tools.agent import identificador_agent
from config import AGENT, LANGUAGES_CONFIG_FILE



# TODO Mover função para um arquivo separado
def annotate(text: str, analyze_results: List[RecognizerResult]):
    """Highlight the identified PII entities on the original text

    :param text: Full text
    :param analyze_results: list of results from presidio analyzer engine
    """
    tokens = []
    
    if not analyze_results:
        return [text]

    # sort by start index
    results = sorted(analyze_results, key=lambda x: x.start)
    
    last_end = 0
    for res in results:
        # Add text before the entity
        if res.start > last_end:
            tokens.append(text[last_end:res.start])
        
        # Add the entity as a tuple (text, entity_type)
        tokens.append((text[res.start:res.end], res.entity_type))
        
        last_end = res.end
    
    # Add remaining text after the last entity
    if last_end < len(text):
        tokens.append(text[last_end:])
    
    return tokens

# Create NLP engine based on configuration file
provider = NlpEngineProvider(conf_file=LANGUAGES_CONFIG_FILE)
nlp_engine_with_portuguese = provider.create_engine()

# Setting up Portuguese recognizers with more specific contexts
email_recognizer_pt = EmailRecognizer(
    supported_language="pt",
    context=["email", "correio eletrônico", "endereço de email"],
    # patterns=[r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b']
)

phone_recognizer_pt = PhoneRecognizer(
    supported_language="pt",
    context=["telefone", "celular", "número de telefone"]
)

spacy_recognizer_pt = SpacyRecognizer(
    supported_language='pt',
    supported_entities=["PERSON"],
    context=['nome', 'pessoa', 'chamado', 'filho', 'neto']
)

cpf_recognizer = CPFRecognizer()
escola_recognizer = EscolaRecognizer()
endereco_recognizer = EnderecoRecognizer()
# Create registry with both languages supported
registry = RecognizerRegistry()
registry.supported_languages = ["en", "pt"]

# Add recognizers to registry
# registry.add_recognizer(email_recognizer_en)
registry.add_recognizer(email_recognizer_pt)
registry.add_recognizer(phone_recognizer_pt)
registry.add_recognizer(spacy_recognizer_pt)
registry.add_recognizer(cpf_recognizer)
registry.add_recognizer(escola_recognizer)
registry.add_recognizer(endereco_recognizer)
def anonymize_text(text):
    # Set up analyzer with our updated recognizer registry
    analyzer = AnalyzerEngine(
        registry=registry,
        supported_languages=["en","pt"],
        nlp_engine=nlp_engine_with_portuguese
    )

    results = analyzer.analyze(text=text, language="pt", return_decision_process=True)

    anonymizer = AnonymizerEngine()

    anonymized_text = anonymizer.anonymize(text=text,analyzer_results=results)
    annotated_tokens = annotate(text=text, analyze_results=results)
    print(annotated_tokens)

    if AGENT:
        answer = identificador_agent(text, anonymized_text.text, annotated_tokens)
    else:
        answer = None


    if answer != None:
        return answer
    else:
        return anonymized_text.text