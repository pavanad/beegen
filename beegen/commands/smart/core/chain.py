from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence


def load_chain(template: str, model) -> RunnableSequence:
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model | StrOutputParser()
    return chain
