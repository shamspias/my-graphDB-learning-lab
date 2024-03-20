from langchain_community.graphs import Neo4jGraph
from langchain_experimental.graph_transformers.diffbot import DiffbotGraphTransformer
from langchain_community.document_loaders import WikipediaLoader
from langchain.chains import GraphCypherQAChain
from langchain_groq import ChatGroq

from src.config import settings

NEO4J_URI = settings.NEO4J_URI
NEO4J_USERNAME = settings.NEO4J_USERNAME
NEO4J_PASSWORD = settings.NEO4J_PASSWORD
NEO4J_DATABASE = settings.NEO4J_DATABASE

diffbot_api_key = settings.DIFFBOT_API_KEY
diffbot_nlp = DiffbotGraphTransformer(diffbot_api_key=diffbot_api_key)

query = "Al-Khwarizmi"
raw_documents = WikipediaLoader(query=query).load()
graph_documents = diffbot_nlp.convert_to_graph_documents(raw_documents)

graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)
graph.add_graph_documents(graph_documents)
graph.refresh_schema()

chain = GraphCypherQAChain.from_llm(
    cypher_llm=ChatGroq(temperature=0, model_name="mixtral-8x7b-32768", groq_api_key=settings.LLM_API_KEY),
    qa_llm=ChatGroq(temperature=0, model_name="mixtral-8x7b-32768", groq_api_key=settings.LLM_API_KEY),
    graph=graph,
    verbose=True,
)

chain.run("Which university did Al Khwarizmi attend?")
