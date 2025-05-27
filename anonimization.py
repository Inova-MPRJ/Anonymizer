from presidio_analyzer import AnalyzerEngine, RecognizerRegistry, PatternRecognizer
from presidio_anonymizer import AnonymizerEngine
from presidio_analyzer.predefined_recognizers import SpacyRecognizer, EmailRecognizer, PhoneRecognizer
from presidio_analyzer.nlp_engine import NlpEngineProvider
from cpf import CPFRecognizer

LANGUAGES_CONFIG_FILE = "./docs/analyzer/languages-config.yml"

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
    context=['nome', 'pessoa', 'chamado']
)

cpf_recognizer = CPFRecognizer()

# Create registry with both languages supported
registry = RecognizerRegistry()
registry.supported_languages = ["en", "pt"]

# Add recognizers to registry
# registry.add_recognizer(email_recognizer_en)
registry.add_recognizer(email_recognizer_pt)
registry.add_recognizer(phone_recognizer_pt)
registry.add_recognizer(spacy_recognizer_pt)
registry.add_recognizer(cpf_recognizer)

def anonymize_text(text):
    # Set up analyzer with our updated recognizer registry
    analyzer = AnalyzerEngine(
        registry=registry,
        supported_languages=["en","pt"],
        nlp_engine=nlp_engine_with_portuguese)

    results = analyzer.analyze(text=text, language="pt")
    print(results)

    anonymizer = AnonymizerEngine()

    anonymized_text = anonymizer.anonymize(text=text,analyzer_results=results)

    return anonymized_text.text

