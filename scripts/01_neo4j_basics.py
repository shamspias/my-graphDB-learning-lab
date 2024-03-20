import os

from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph

from src.config import settings

NEO4J_URI = settings.NEO4J_URI
NEO4J_USERNAME = settings.NEO4J_USERNAME
NEO4J_PASSWORD = settings.NEO4J_PASSWORD
NEO4J_DATABASE = settings.NEO4J_DATABASE

kg = Neo4jGraph(
    url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD, database=NEO4J_DATABASE
)

cypher = """
  MATCH (n) 
  RETURN count(n)
  """

result = kg.query(cypher)
print(result)
