# Projeto de Anonimização de Dados

Este projeto tem como objetivo fornecer uma solução para anonimização de dados sensíveis, garantindo a privacidade e segurança das informações processadas. Desenvolvido especificamente para textos em português brasileiro, utiliza o Microsoft Presidio com recognizers customizados para o contexto brasileiro.

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Inova-MPRJ/Anonymizer
cd Anonymizer
```

2. Crie um ambiente virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Como usar

### Interface Web (Streamlit)

Para usar a interface web interativa:

```bash
cd interface
streamlit run app.py
```

A interface será aberta no seu navegador padrão (geralmente em `http://localhost:8501`) e oferece:
- ✨ Interface intuitiva e amigável
- 📝 Área de entrada para texto original
- ✅ Área de saída para texto anonimizado  
- 🔄 Processamento em tempo real com indicador de loading
- 📊 Estatísticas de anonimização (contagem de caracteres, redução)
- 📥 Download do texto anonimizado
- 🎯 Detecção automática de múltiplos tipos de PII

### API REST

Para usar a API REST:

1. Certifique-se de que o ambiente virtual está ativado
2. Execute o servidor da API:
```bash
python app.py
```

3. Faça requisições POST para `http://localhost:5000/` com o seguinte formato:
```json
{
    "text": "Seu texto para anonimizar aqui"
}
```

## Estrutura do Projeto

```
anonimization/
├── README.md
├── requirements.txt
├── app.py                           # API REST Flask
├── config.py                        # Configurações do projeto
├── teste.py                         # Scripts de teste
├── interface/
│   └── app.py                      # Interface Streamlit
├── tools/
│   ├── anonimization.py            # Motor de anonimização principal
│   ├── agent.py                    # Agente identificador
│   └── recognizers/                # Recognizers customizados
│       ├── cpf.py                  # Reconhecedor de CPF
│       ├── escola.py               # Reconhecedor de escolas
│       └── endereços.py            # Reconhecedor de endereços
└── docs/
    └── analyzer/
        └── languages-config.yml    # Configuração de idiomas
```

## Recognizers Disponíveis

### 🆔 **CPF (Cadastro de Pessoa Física)**
- **Formatos detectados**: 123.456.789-00, 12345678900
- **Score de confiança**: 0.85
- **Contexto**: Detecta CPFs com ou sem formatação

### 👤 **PERSON (Nomes de Pessoas)**
- **Tecnologia**: spaCy NLP (modelo `pt_core_news_lg`)
- **Contexto**: nome, pessoa, chamado
- **Score de confiança**: Variável (baseado no modelo spaCy)

### 📧 **EMAIL (Endereços de Email)**
- **Formatos detectados**: usuario@dominio.com.br
- **Contexto**: email, correio eletrônico, endereço de email
- **Score de confiança**: Alto (recognizer nativo do Presidio)

### 📱 **PHONE_NUMBER (Números de Telefone)**
- **Formatos detectados**: (11) 99999-9999, 11999999999
- **Contexto**: telefone, celular, número de telefone
- **Score de confiança**: Alto (recognizer nativo do Presidio)

### 🏫 **ESCOLA (Instituições de Ensino)**
- **Tipos detectados**:
  - Escola Municipal/Estadual/Federal + Nome
  - Colégio + Nome
  - Universidade + Nome
  - Faculdade + Nome
  - Instituto + Nome
  - Centro Educacional + Nome
  - EMEF/EMEI/CEI (específicos de SP)
  - Abreviações (E.M., E.E., E.F.)
  - Campus + Nome

- **Exemplos**:
  - `Escola Municipal Professor João Silva`
  - `Colégio Santo Antônio`
  - `Universidade de São Paulo`
  - `EMEF Monteiro Lobato`

- **Score de confiança**: 0.85 - 0.95

### 📍 **ENDEREÇO (Endereços e Localização)**
- **Tipos detectados**:
  - Logradouros completos: `Rua das Flores, 123`
  - CEP brasileiro: `01310-100`
  - Endereços com bairro e cidade: `rua pompílio de albuquerque, 62, encantado, rio de janeiro`
  - Complementos: `apartamento 45`, `sala 1503`
  - Endereços rurais: `Fazenda Santa Maria`
  - Condomínios: `Condomínio Villa Real`
  - Rodovias: `BR-116, Km 235`

- **Características especiais**:
  - ✅ **Case insensitive** (detecta minúsculas e maiúsculas)
  - ✅ **Suporte a acentos** (pompílio, josé, joão)
  - ✅ **Múltiplos formatos** de endereço brasileiro
  - ✅ **Contexto inteligente** (situada na, localizada em, etc.)

- **Score de confiança**: 0.80 - 0.99

## Funcionalidades Avançadas

- 🔍 **Detecção Contextual**: Usa palavras de contexto para melhorar a precisão
- 🧠 **NLP Avançado**: Modelos spaCy especializados em português brasileiro
- 🎯 **Alta Precisão**: Recognizers customizados para o contexto brasileiro
- 🔄 **Processamento em Tempo Real**: Interface responsiva com feedback visual
- 📊 **Métricas Detalhadas**: Estatísticas sobre o processo de anonimização
- 🌐 **Suporte Completo ao Português**: Configuração específica para PT-BR
- 🛡️ **Tratamento de Erros**: Sistema robusto com mensagens informativas

## Casos de Uso

### 📋 **Documentos Legais**
- Relatórios policiais
- Processos judiciais
- Documentos administrativos

### 🏥 **Área da Saúde**
- Prontuários médicos
- Relatórios de pacientes
- Documentação hospitalar

### 🎓 **Educação**
- Registros escolares
- Relatórios pedagógicos
- Documentação acadêmica

### 🏢 **Corporativo**
- Relatórios internos
- Documentação de RH
- Correspondências empresariais

## Exemplos de Uso

### Texto Original:
```
João Silva, CPF 123.456.789-00, mora na Rua das Flores, 123, 
e estuda na Escola Municipal Professor Carlos Drummond. 
Seu email é joao.silva@email.com e telefone (11) 99999-9999.
```

### Texto Anonimizado:
```
<PERSON>, CPF <CPF>, mora na <ENDEREÇO>, 
e estuda na <ESCOLA>. 
Seu email é <EMAIL_ADDRESS> e telefone <PHONE_NUMBER>.
```

## Desenvolvimento

### Criando Novos Recognizers

1. Crie um arquivo em `tools/recognizers/`
2. Implemente a classe herdando de `PatternRecognizer`
3. Registre o recognizer em `tools/anonimization.py`
4. Adicione testes apropriados

### Exemplo de Recognizer:
```python
from presidio_analyzer import PatternRecognizer, Pattern

class NovoRecognizer(PatternRecognizer):
    def __init__(self):
        patterns = [
            Pattern(name="Padrão", regex=r"regex_pattern", score=0.9)
        ]
        super().__init__(
            supported_entity="NOVA_ENTIDADE",
            patterns=patterns,
            supported_language="pt",
            context=["palavra1", "palavra2"]
        )
```

## Contribuindo

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

### Diretrizes para Contribuição:
- ✅ Mantenha compatibilidade com Python 3.8+
- ✅ Adicione testes para novos recognizers
- ✅ Documente novas funcionalidades
- ✅ Siga os padrões de código existentes

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes. 