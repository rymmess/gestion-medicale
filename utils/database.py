from neo4j import GraphDatabase

class Database:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def query(self, cypher_query, parameters=None):
        with self._driver.session() as session:
            return session.run(cypher_query, parameters or {}).data()

    def close(self):
        self._driver.close()
