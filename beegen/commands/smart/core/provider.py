import os

from langchain_community.chat_models import ChatOllama
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.llms import Ollama
from langchain_google_genai import (
    ChatGoogleGenerativeAI,
    GoogleGenerativeAI,
    GoogleGenerativeAIEmbeddings,
)
from langchain_openai import ChatOpenAI, OpenAI, OpenAIEmbeddings


class Provider:
    def __init__(self, config: dict) -> None:
        self.__llm = None
        self.__chat_model = None
        self.__embeddings = None
        self.__embeddings_name = None
        self.__provider_name = None
        self.__temperature = 0
        self.__config = config
        self.__load_provider()

    @property
    def llm(self):
        """Returns the Large Language Model instance."""
        return self.__llm

    @property
    def chat_model(self):
        """Returns the Chat Large Language Model instance."""
        return self.__chat_model

    @property
    def embeddings(self):
        """Returns the Embeddings instance."""
        return self.__embeddings

    @property
    def embeddings_name(self):
        """Returns the embeddings name."""
        return self.__embeddings_name

    @property
    def provider_name(self):
        """Returns the provider name."""
        return self.__provider_name

    def __load_provider(self):
        self.__provider_name = self.__config["provider"]
        provider_method = self.__get_provider_method(self.__provider_name)
        if provider_method is None:
            self.line_prefix(
                f"Provider <error>{self.__provider_name}</> not supported."
            )

        # init provider model
        self.__llm, self.__chat_model, self.__embeddings = provider_method(
            self.__config
        )

    def __get_provider_method(self, provider_name: str):
        """Returns the provider method based on the given provider name."""
        return {
            "Ollama": self.__ollama_provider,
            "OpenAI": self.__openai_provider,
            "Google": self.__google_provider,
        }.get(provider_name, None)

    def __ollama_provider(self, parameters: dict):
        model_name = parameters.get("model_name", "llama3")
        self.__embeddings_name = parameters.get("embeddings_name", model_name)

        llm = Ollama(model=model_name)
        chat_model = ChatOllama(model=model_name)
        embeddings = OllamaEmbeddings(model=self.__embeddings_name)

        return llm, chat_model, embeddings

    def __openai_provider(self, parameters: dict):
        os.environ["OPENAI_API_KEY"] = parameters["api_key"]
        model_name = parameters.get("model_name", "gpt-3.5-turbo")
        self.__embeddings_name = parameters.get(
            "embeddings_name", "text-embedding-3-large"
        )

        llm = OpenAI(model_name=model_name, temperature=self.__temperature)
        chat_model = ChatOpenAI(model_name=model_name, temperature=self.__temperature)
        embeddings = OpenAIEmbeddings(model=self.__embeddings_name)

        return llm, chat_model, embeddings

    def __google_provider(self, parameters: dict):
        os.environ["GOOGLE_API_KEY"] = parameters["api_key"]
        model_name = parameters.get("model_name", "gemini-pro")
        self.__embeddings_name = parameters.get(
            "embeddings_name", "models/embedding-001"
        )

        llm = GoogleGenerativeAI(model=model_name, temperature=self.__temperature)
        chat_model = ChatGoogleGenerativeAI(
            model=model_name, temperature=self.__temperature
        )
        embeddings = GoogleGenerativeAIEmbeddings(model=self.__embeddings_name)

        return llm, chat_model, embeddings
