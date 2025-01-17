class AppointmentModel:
    def __init__(self, db):
        self.db = db

    def check_appointment_exists(self, patient_id, doctor_id, date,time):
        query = """
        MATCH (r:RendezVous {date: $date,time:$time})<-[:PLANIFIE]-(d:Medecin {id: $doctor_id})
        RETURN r
        """
        result = self.db.query(query, {"patient_id": patient_id, "doctor_id": doctor_id, "date": date,"time":time})
        return len(result) > 0

    def create_appointment(self, patient_id, doctor_id, date,time):
        query = """
        MATCH (p:Patient {id: $patient_id}), (d:Medecin {id: $doctor_id})
        CREATE (p)-[:A_PRIS]->(r:RendezVous {date: $date,time:$time})<-[:PLANIFIE]-(d)
        RETURN r
        """
        self.db.query(query, {"patient_id": patient_id, "doctor_id": doctor_id, "date": date , "time":time})

    def diagnose_patient_with_pathology(self, patient_id, pathology_id):
        query = """
        MATCH (p:Patient {id: $patient_id}), (pa:Pathologie {id: $pathology_id})
        CREATE (p)-[:DIAGNOSTIQUE_AVEC]->(pa)
        RETURN p, pa
        """
        self.db.query(query, {"patient_id": patient_id, "pathology_id": pathology_id})

    def treat_pathology_with_treatment(self, pathology_id, treatment_id):
        query = """
        MATCH (pa:Pathologie {id: $pathology_id}), (t:Traitement {id: $treatment_id})
        CREATE (pa)-[:TRAITE_AVEC]->(t)
        RETURN pa, t
        """
        self.db.query(query, {"pathology_id": pathology_id, "treatment_id": treatment_id})

    def check_treatment_for_pathology(self, pathology_id, treatment_id):
        query = """
        MATCH (pa:Pathologie {id: $pathology_id})-[:TRAITE_AVEC]->(t:Traitement {id: $treatment_id})
        RETURN t
        """
        result = self.db.query(query, {"pathology_id": pathology_id, "treatment_id": treatment_id})
        return len(result) > 0

    def check_diagnosis_for_patient(self, patient_id, pathology_id):
        query = """
        MATCH (p:Patient {id: $patient_id})-[:DIAGNOSTIQUE_AVEC]->(pa:Pathologie {id: $pathology_id})
        RETURN pa
        """
        result = self.db.query(query, {"patient_id": patient_id, "pathology_id": pathology_id})
        return len(result) > 0

    def get_pathologies_for_patient(self, patient_id):
        query = """
        MATCH (p:Patient {id: $patient_id})-[:DIAGNOSTIQUE_AVEC]->(pa:Pathologie)
        RETURN pa.id AS id, pa.name AS name, pa.propriete AS propriete
        """
        return self.db.query(query, {"patient_id": patient_id})

    def get_treatments_for_pathology(self, pathology_id):
        query = """
        MATCH (pa:Pathologie {id: $pathology_id})-[:TRAITE_AVEC]->(t:Traitement)
        RETURN t.id AS id, t.name AS name, t.propriete AS propriete
        """
        return self.db.query(query, {"pathology_id": pathology_id})
