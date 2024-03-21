from langchain_community.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
from langchain_openai import ChatOpenAI

from src.config import settings

NEO4J_URI = settings.NEO4J_URI
NEO4J_USERNAME = settings.NEO4J_USERNAME
NEO4J_PASSWORD = settings.NEO4J_PASSWORD
NEO4J_DATABASE = settings.NEO4J_DATABASE

graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)
graph.refresh_schema()

chain = GraphCypherQAChain.from_llm(
    cypher_llm=ChatOpenAI(temperature=0, model_name="gpt-4-0125-preview", openai_api_key=settings.LLM_API_KEY),
    qa_llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-0125", openai_api_key=settings.LLM_API_KEY),
    graph=graph,
    verbose=True,
)

result = chain.invoke("Which location Al-Khwarizmi travel?")

print(result["result"])
