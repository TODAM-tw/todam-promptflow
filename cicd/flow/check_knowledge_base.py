import os
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain_openai.chat_models.azure import AzureChatOpenAI
from langchain_openai.embeddings.azure import AzureOpenAIEmbeddings
from langchain_pinecone.vectorstores import PineconeVectorStore
from promptflow.connections import AzureOpenAIConnection
from promptflow.tools.aoai import tool

ENV_PATH = Path(__file__).parent / "env.local"
print(ENV_PATH)
load_dotenv(dotenv_path=ENV_PATH)
# The inputs section will change based on the arguments of the tool function, after you save the code
# Adding type to arguments and return value will help the system show the types properly
# Please update the function name/signature per need

INDEX_NAME = os.environ.get("PINECONE_INDEX_NAME")
AZURE_DEPLOYMENT_NAME = os.environ.get("AZURE_DEPLOYMENT_NAME")
AZURE_EMBEDDINGS_DEPLOYMENT_NAME = os.environ.get("AZURE_EMBEDDINGS_DEPLOYMENT_NAME")


@tool
def retrieve_qa(
    query: str,
    chat_history: List[Dict[str, Any]],
    conn: AzureOpenAIConnection,
) -> str:

    # Embeddings
    embeddings = AzureOpenAIEmbeddings(
        model="text-embedding-3-small",
        azure_deployment=AZURE_EMBEDDINGS_DEPLOYMENT_NAME,
        azure_endpoint=conn.api_base,
        api_key=conn.api_key,
        api_version=conn.api_version,
    )

    docsearch = PineconeVectorStore.from_existing_index(
        index_name=INDEX_NAME, embedding=embeddings
    )

    # LLM
    llm = AzureChatOpenAI(
        azure_deployment=AZURE_DEPLOYMENT_NAME,
        azure_endpoint=conn.api_base,
        model_version="0613",
        api_key=conn.api_key,
        api_version=conn.api_version,
        verbose=True,
    )
    # Define the retrieval QA model
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
        return_source_documents=True,
    )
    chain = qa
    response = chain.invoke({"query": query, "chat_history": chat_history})
    print(response)
    return response
