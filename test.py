from neo4j import GraphDatabase

try:
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "rym1902200319"))
    with driver.session() as session:
        result = session.run("RETURN 'Connection successful' AS message")
        for record in result:
            print(record["message"])
except Exception as e:
    print(f"Error: {e}")
finally:
    driver.close()
