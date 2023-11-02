import os
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import JSONLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.vectorstores import Chroma

MODEL_NAME = "gpt-3.5-turbo"

class VectorDB:
    def __init__(self):
        """
        Initialize VectorDB object.

        Args:
            source_data_path (str): Path to the source data file. Should be a json file.
        """
        source_data_path = "example/guidelines.json"
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
        
        self.vector_qa = RetrievalQA.from_chain_type(
            llm=ChatOpenAI(temperature=0, model_name=MODEL_NAME),
            chain_type="stuff",
            retriever=self.db.as_retriever()
        )

    def get_vector_chain(self):
        return self.vector_qa


