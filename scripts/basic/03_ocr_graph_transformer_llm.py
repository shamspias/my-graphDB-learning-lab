import asyncio

from langchain_core.documents.base import Document
from langchain_community.graphs import Neo4jGraph
from langchain_experimental.graph_transformers import LLMGraphTransformer
from langchain.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_groq import ChatGroq

from src.config import settings
from src.utils.text_extraction_utils import TextExtractor


class GraphDocumentProcessor:
    def __init__(self, llm):
        self.transformer = LLMGraphTransformer(llm=llm)

    def convert_documents(self, raw_documents):
        return self.transformer.convert_to_graph_documents(raw_documents)


class GraphHandler:
    def __init__(self, uri, username, password, database=None):
        self.graph = Neo4jGraph(url=uri, username=username, password=password, database=database)

    def add_documents(self, graph_documents):
        self.graph.add_graph_documents(graph_documents)
        self.graph.refresh_schema()


class QAChainHandler:
    def __init__(self, graph, llm_api_key, model_name="mixtral-8x7b-32768"):
        self.base_llm = ChatGroq(temperature=0, model_name=model_name, groq_api_key=llm_api_key)
        self.chain = GraphCypherQAChain.from_llm(
            cypher_llm=self.base_llm,
            qa_llm=ChatGroq(temperature=0, model_name=model_name, groq_api_key=llm_api_key),
            graph=graph,
            verbose=True,
        )

    async def run_query(self, query):
        return self.chain.invoke(query)


class TextUploader:
    def __init__(self):
        self.text_extractor = TextExtractor()

    async def upload_and_extract_text(self, uploaded_file=None, uploaded_image=None):
        text, language = '', 'und'
        if uploaded_file:
            text, language = await self.text_extractor.extract_text_from_file_path(uploaded_file)
        elif uploaded_image:
            text, language = await self.text_extractor.extract_text_from_file_path(uploaded_image)
        return text, language


async def main():
    # Setup and process

    graph_handler = GraphHandler(settings.NEO4J_URI, settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD,
                                 settings.NEO4J_DATABASE)
    qa_chain_handler = QAChainHandler(graph_handler.graph, settings.LLM_API_KEY)
    document_processor = GraphDocumentProcessor(qa_chain_handler.base_llm)

    text_uploader = TextUploader()

    # file_path = "data/examples/pdf/Аменорея и олигоменорея.pdf"  # Placeholder, replace with actual document source
    file_path = "data/examples/pdf/conversation_with_rim.pdf"  # Placeholder, replace with actual document source
    raw_data, language = await text_uploader.upload_and_extract_text(uploaded_file=file_path)
    langchain_document = [Document(page_content=raw_data)]
    print(langchain_document)
    graph_documents = document_processor.convert_documents(langchain_document)
    print(graph_documents)
    graph_handler.add_documents(graph_documents)

    # Example query
    result = await qa_chain_handler.run_query("NEO4J_DATABASE=graph-learn")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
