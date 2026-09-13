import os
from neo4j import GraphDatabase

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "neo4jpassword")

class Neo4jDriver:
    def __init__(self):
        self.driver = None

    def connect(self):
        if not self.driver:
            self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

    def close(self):
        if self.driver:
            self.driver.close()
            self.driver = None

    def get_session(self):
        if not self.driver:
            self.connect()
        return self.driver.session()

neo4j_driver = Neo4jDriver()

def get_neo4j():
    session = neo4j_driver.get_session()
    try:
        yield session
    finally:
        session.close()
