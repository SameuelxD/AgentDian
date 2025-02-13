from langchain_community.document_loaders import PDFPlumberLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from .confg import vector_store
from langchain_core.tools import tool
import os
# scan of the content


file_path = os.path.abspath("D:/PythonProject/deep_transformer/docs/use-conectores.pdf")
loader = PDFPlumberLoader(file_path)
docs = loader.load()
# Load and chunk contents of the pdf
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # chunk size (characters)
    chunk_overlap=200,  # chunk overlap (characters)
    add_start_index=True,  # track index in original document
)
all_splits = text_splitter.split_documents(docs)

# Index chunks
document_ids = vector_store.add_documents(documents=all_splits)



@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to a query."""
    retrieved_docs = vector_store.similarity_search(query, k=2)
    serialized = "\n\n".join(
        f"Source: {doc.metadata}\n" f"Content: {doc.page_content}"
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs



