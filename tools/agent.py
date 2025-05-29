from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.llms import Ollama
import os
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from config import MODEL, LLM

load_dotenv()

if MODEL == "Ollama":
    model = Ollama(model=LLM)
elif MODEL == "Groq":
    os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
    model = ChatGroq(model="llama-3.3-70b-versatile")
else:
    raise ValueError(f"Modelo {MODEL} não suportado")


def identificador_agent(texto, texto_anonimizado, tabela_anonimizacao):
    system_prompt="""
        Você é um especialista em identificar entidades anonimizadas em textos.
        Você receberá o texto original e o texto anonimizado, além da
        tabela de anonimização, e deverá correlacionar as entidades anonimizadas.
        As entidades anonimizadas são:
        - <PERSON>
        - <CPF>
        - <EMAIL_ADDRESS>
        Depois do tratamento, o texto anonimizado deve passar a ter:
        - <PERSON1>
        - <CPF1>
        - <EMAIL_ADDRESS1>
        - <PERSON2>
        - <CPF2>
        - <EMAIL_ADDRESS2>
        De acordo com a tabela de anonimização, você deve identificar as entidades anonimizadas e substituir
        pelo seu respectivo valor.
        O texto anonimizado deve ser retornado com as entidades anonimizadas substituídas pelo seu respectivo valor.
        Apenas retorne o texto anonimizado, sem nenhum outro texto adicional.
    """
    user_prompt = f"""
        Texto: {texto}
        Texto anonimizado: {texto_anonimizado}
        Tabela de anonimização: {tabela_anonimizacao}
        """
    menssages = [SystemMessage(system_prompt), HumanMessage(user_prompt)]

    answer = model.invoke(menssages)
    if MODEL == "Ollama":
        print(answer)
        return answer
    else:
        return answer.content
