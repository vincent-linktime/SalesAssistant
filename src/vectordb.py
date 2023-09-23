import os
from langchain.document_loaders import JSONLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores import Chroma


class VectorDB:
    def __init__(self, source_data_path):
        """
        Initialize VectorDB object.

        Args:
            source_data_path (str): Path to the source data file. Should be a json file.
        """
        loader = JSONLoader(
            file_path = source_data_path,
            jq_schema='.guidelines[].content',
            text_content=False)

        db_path = f'vectordb/{os.path.basename(source_data_path)}'
        if os.path.exists(db_path):
            self.db = Chroma(persist_directory=db_path, embedding_function=OpenAIEmbeddings())
            index = VectorStoreIndexWrapper(vectorstore=self.db)
        else:
            index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":db_path}).from_loaders([loader])
            self.db = index.vectorstore

    def query_db(self, query):
        """
        Query the database for passages that are similar to the query.

        Args:
            query (str): Query string.

        Returns:
            content (list): List of passages that are similar to the query.
        """
        results = self.db.similarity_search(query, k=3)
        content = []
        for result in results:
            content.append(result.page_content)
        return content



