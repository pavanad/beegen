import os
from typing import Any

from langchain_community.document_loaders import (
    DirectoryLoader,
    PyPDFDirectoryLoader,
    PyPDFLoader,
    TextLoader,
)
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter


class VectorStore:

    def __init__(self, source: str, file_type: str, embeddings):
        self.__source = source
        self.__documents = None
        self.__embeddings = embeddings
        self.__loader = self.__get_loader_method(file_type)

    def __get_loader_method(self, file_type: str):
        if file_type == "pdf":
            return self.__pdf_loader()
        return self.__text_loader(file_type)

    def __pdf_loader(self) -> Any:
        if os.path.isdir(self.__source):
            return PyPDFDirectoryLoader(self.__source)
        return PyPDFLoader(self.__source)

    def __text_loader(self, file_type: str) -> Any:
        if os.path.isdir(self.__source):
            extension = {"markdown": "md", "text": "txt"}.get(file_type, file_type)
            return DirectoryLoader(
                "../", glob=f"**/*.{extension}", loader_cls=TextLoader
            )
        return TextLoader(self.__source, encoding="utf-8")

    def load(self) -> None:
        self.__documents = self.__loader.load()

    def split_text(self) -> None:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        self.__documents = text_splitter.split_documents(self.__documents)

    def size(self) -> int:
        return len(self.__documents)

    def save(self, folder_path: str) -> None:
        db = FAISS.from_documents(self.__documents, self.__embeddings)
        db.save_local(folder_path=folder_path)
