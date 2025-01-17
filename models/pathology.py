class PathologyModel:
    def __init__(self, db):
        self.db = db

    # Créer une nouvelle pathologie avec id
    def create_pathology(self, id, name, propriete):
        query = """
        CREATE (p:Pathologie {id: $id, name: $name, propriete: $propriete})
        """
        parameters = {
            "id": id,
            "name": name,
            "propriete": propriete
        }
        self.db.query(query, parameters)

    # Obtenir toutes les pathologies
    def get_all_pathologies(self):
        query = """
        MATCH (p:Pathologie)
        RETURN p.id AS id, p.name AS name, p.propriete AS propriete
        """
        return self.db.query(query)
    
    # Méthode pour récupérer une pathologie par ID
    def get_pathology_by_id(self, pathology_id):
        query = """
        MATCH (p:Pathologie {id: $id})
        RETURN p.id AS id, p.name AS name, p.propriete AS propriete
        """
        parameters = {"id": pathology_id}
        result = self.db.query(query, parameters)
        if result:
            return result[0]  
        return None

    # Mettre à jour une pathologie
    def update_pathology(self, pathology_id, name, propriete):
        query = """
        MATCH (p:Pathologie {id: $pathology_id})
        SET p.name = $name, p.propriete = $propriete
        RETURN p
        """
        parameters = {
            "pathology_id": pathology_id,
            "name": name,
            "propriete": propriete
        }
        self.db.query(query, parameters)

    # Supprimer une pathologie
    def delete_pathology(self, pathology_id):
        query = """
        MATCH (p:Pathologie {id: $id})
        DETACH DELETE p
        """
        parameters = {"id": pathology_id}
        self.db.query(query, parameters)

