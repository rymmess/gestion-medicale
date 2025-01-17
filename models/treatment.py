class TreatmentModel:
    def __init__(self, db):
        self.db = db

    # Créer un nouveau traitement avec id
    def create_treatment(self, id, name, propriete):
        query = """
        CREATE (t:Traitement {id: $id, name: $name, propriete: $propriete})
        """
        parameters = {
            "id": id,
            "name": name,
            "propriete": propriete
        }
        self.db.query(query, parameters)

    # Obtenir tous les traitements
    def get_all_treatments(self):
        query = """
        MATCH (t:Traitement)
        RETURN t.id AS id, t.name AS name, t.propriete AS propriete
        """
        return self.db.query(query)

    # Mettre à jour un traitement
    def update_treatment(self, treatment_id, name, propriete):
        query = """
        MATCH (t:Traitement {id: $treatment_id})
        SET t.name = $name, t.propriete = $propriete
        RETURN t
        """
        parameters = {
            "treatment_id": treatment_id,
            "name": name,
            "propriete": propriete
        }
        self.db.query(query, parameters)

    # Supprimer un traitement
    def delete_treatment(self, treatment_id):
        query = """
        MATCH (t:Traitement {id: $treatment_id})
        DELETE t
        """
        parameters = {"treatment_id": treatment_id}
        self.db.query(query, parameters)

    # Liste des pathologies traitées avec le traitement
    def get_pathologies_for_treatment(self, treatment_id):
        query = """
        MATCH (t:Traitement {id: $treatment_id})<-[:TRAITE_AVEC]-(p:Pathologie)
        RETURN p.id AS id, p.name AS name, p.propriete AS propriete
        """
        parameters = {"treatment_id": treatment_id}
        return self.db.query(query, parameters)
