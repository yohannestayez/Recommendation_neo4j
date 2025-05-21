from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv('.env')

# Set environment variables
NEO4J_URL = os.getenv("NEO4J_URL")
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')

class Neo4jConnector:
    def __init__(self, url, username, password):
        try:
            self.driver = GraphDatabase.driver(url, auth=(username, password))
        except Exception as e:
            raise Exception(f"Failed to connect to Neo4j: {str(e)}")

    def query(self, cypher_query, **kwargs):
        with self.driver.session() as session:
            result = session.run(cypher_query, **kwargs)  # Pass parameters as kwargs
            return [record for record in result]  # Return list of records

    def close(self):
        self.driver.close()

# Initialize the connector
DB_CONNECTOR = Neo4jConnector(url=NEO4J_URL, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)