from cleo.helpers import argument, option

from beegen.commands.smart.base import SmartBaseCommand
from beegen.commands.smart.core.vector_store import VectorStore


class SmartCreateVectorStoreCommand(SmartBaseCommand):
    name = "smart create-vectorstore"
    description = (
        "Create a local vector store using FAISS from specified files or directories."
    )

    arguments = [
        argument(
            name="path",
            description=(
                "The path to the file or directory to be included in the vector store."
            ),
        )
    ]

    options = [
        option(
            long_name="file-type",
            short_name="f",
            description="Specifies the type of the files (e.g., markdown, txt, pdf)",
            flag=False,
        )
    ]

    files_supported = ["html", "json", "markdown", "pdf", "text"]

    def handle(self) -> int:
        self.line("")

        file_type = self.option("file-type")
        if file_type is None:
            file_type = self.choice(
                f"{self.PREFIX}Please select the file type supported:",
                self.files_supported,
                0,
            )

        if file_type not in self.files_supported:
            self.line_prefix(f"<error>Unsupported file type: {file_type}</error>")
            self.line_prefix(f"Supported files: {', '.join(self.files_supported)}\n")
            return

        source_path = self.argument("path")
        self.__create_vector_store(source_path, file_type)

        self.line("")

    def __create_vector_store(self, source_path: str, file_type: str) -> None:
        try:
            self.line("")
            self.line_prefix(
                f"Loading document(s) from <comment>{source_path}</comment>"
            )

            with self.console.status("") as _:
                vectorstore = VectorStore(
                    source_path, file_type, self.provider.embeddings
                )
                vectorstore.load()

            self.line_prefix(
                f"Loaded <comment>{vectorstore.size()}</> document(s) from "
                f"<comment>{source_path}</>"
            )

            if self.confirm(
                "\nDo you want to split the documents into small chunks?", False
            ):
                vectorstore.split_text()

            self.line("")
            self.line_prefix(
                "Creating a vector store with the "
                f"<comment>{self.provider.embeddings_name}</> embeddings model "
                f"from provider <comment>{self.provider.provider_name}</>"
            )

            with self.console.status("") as _:
                vectorstore.save("./data")

            self.line_prefix(
                f"Vector store created and saved to <comment>{'./data'}</>"
            )
            self.__client_example(self.provider.embeddings_name)

        except Exception:
            self.line_prefix(
                "<error>An error occurred while creating the vector store.</>"
            )

    def __client_example(self, embedding_model: str):
        model = embedding_model if embedding_model else "mxbai-embed-large"
        example = f"""
        from langchain_community.embeddings import OllamaEmbeddings
        from langchain_community.vectorstores import FAISS

        # load embeddings model
        embeddings = OllamaEmbeddings(model="{model}")

        # load the vector store
        db = FAISS.load_local(
            folder_path="./data",
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        )

        # query the vectorstore
        query = "Make a question"
        docs = db.similarity_search(query)
        print(docs[0].page_content)

        # convert vector store to retrieve
        retriever = db.as_retriever()
        docs = retriever.invoke(query)
        print(docs[0].page_content)
        """
        self.line_prefix("Use the following code as a starting point:\n")
        self.print_code(example)
