import asyncio

from langchain_community.graphs import Neo4jGraph
from langchain_experimental.graph_transformers.diffbot import DiffbotGraphTransformer
from langchain.chains import GraphCypherQAChain
from langchain_groq import ChatGroq

from src.config import settings
from src.utils.text_extraction_utils import TextExtractor


class GraphDocumentProcessor:
    def __init__(self, diffbot_api_key):
        self.transformer = DiffbotGraphTransformer(diffbot_api_key=diffbot_api_key)

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
        self.chain = GraphCypherQAChain.from_llm(
            cypher_llm=ChatGroq(temperature=0, model_name=model_name, groq_api_key=llm_api_key),
            qa_llm=ChatGroq(temperature=0, model_name=model_name, groq_api_key=llm_api_key),
            graph=graph,
            verbose=True,
        )

    async def run_query(self, query):
        return await self.chain.run(query)


class TextUploader:
    def __init__(self):
        self.text_extractor = TextExtractor()

    async def upload_and_extract_text(self, uploaded_file=None, uploaded_image=None):
        text, language = '', 'und'
        if uploaded_file:
            text, language = await self.text_extractor.extract_text_from_uploaded_file(uploaded_file)
        elif uploaded_image:
            text, language = await self.text_extractor.extract_text_from_uploaded_image(uploaded_image)
        return text, language


async def main():
    # Setup and process
    document_processor = GraphDocumentProcessor(settings.DIFFBOT_API_KEY)
    graph_handler = GraphHandler(settings.NEO4J_URI, settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD,
                                 settings.NEO4J_DATABASE)
    qa_chain_handler = QAChainHandler(graph_handler.graph, settings.LLM_API_KEY)

    raw_documents = "file_path"  # Placeholder, replace with actual document source
    graph_documents = document_processor.convert_documents(raw_documents)
    graph_handler.add_documents(graph_documents)

    # Example query
    result = await qa_chain_handler.run_query("Which university did Al Khwarizmi attend?")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
