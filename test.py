from langchain.document_loaders import JSONLoader

loader = JSONLoader(
    file_path='./data/guidelines.json',
    jq_schema='.guidelines[].content',
    text_content=False)

data = loader.load()

