from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv('.env')

# Set environment variables
NEO4J_URI =  os.getenv("NEO4J_URL")
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')


class Neo4jConnector:
    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def query(self, cypher_query):
        with self.driver.session() as session:
            session.run(cypher_query)

    def close(self):
        self.driver.close()

DB_CONNECTOR=Neo4jConnector(url=NEO4J_URI,username=NEO4J_USERNAME, password=NEO4J_PASSWORD)