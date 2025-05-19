import chromadb
from chromadb.config import Settings
from chromadb.api.types import QueryResult
from chromadb.utils.embedding_functions import openai_embedding_function

from app.database.config import Config


class VectorDatabase:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.client = chromadb.HttpClient(
            host=config.CHROMA_HOST,
            port=config.CHROMA_PORT,
            settings=Settings(allow_reset=True)
        )
        self.embedding_function = openai_embedding_function.OpenAIEmbeddingFunction(
            api_key=self.config.OPENAI_API_KEY,
            model_name=self.config.EMBEDDING_MODEL
        )
        self.collection = self._initialize_collection()


    def _initialize_collection(self) -> chromadb.Collection:
        return self.client.get_or_create_collection(
            name=self.config.CHROMA_COLLECTION_NAME, 
            embedding_function=self.embedding_function
        )
    

    def reset_vector_db(self) -> None:
        self.client.reset()
        self.collection = self._initialize_collection()
    

    def insert_vector(self, tool_descr: str, tool_id: str) -> None:
        print("INSERTING")
        print(tool_descr)
        self.collection.add(
            documents=[tool_descr],
            ids=[tool_id]
        )


    def update_vector(self, tool_descr: str, tool_id: str) -> None:
        self.collection.update(
            documents=[tool_descr],
            ids=[tool_id]
        )


    def delete_vector(self, tool_id: str) -> None:
        self.collection.delete(ids=[tool_id])


    def query_vector(self, query: str) -> QueryResult:
        return self.collection.query(
            query_texts=[query],
        )
    

vector_db = VectorDatabase(Config())