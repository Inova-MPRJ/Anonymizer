# Projeto de Anonimização de Dados

Este projeto tem como objetivo fornecer uma solução para anonimização de dados sensíveis, garantindo a privacidade e segurança das informações processadas.

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

1. Certifique-se de que o ambiente virtual está ativado
2. Execute o script principal:
```bash
python app.py
```

## Estrutura do Projeto

```
anonimization/
├── README.md
├── requirements.txt
├── app.py
├── cpf.py
├── anonimization.py
├── .gitignore
└── docs/
    └── analyzer/
        └── languages-config.yml
```

## Contribuindo

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Faça commit das suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Faça push para a branch (`git push origin feature/nova-feature`)
5. Crie um Pull Request

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes. 