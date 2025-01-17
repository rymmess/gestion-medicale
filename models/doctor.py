class DoctorModel:
    def __init__(self, db):
        self.db = db

    def get_all_doctors(self):
        query = """
        MATCH (d:Medecin)
        RETURN d.id AS id, d.nom AS name, d.specialite AS specialty
        """
        return self.db.query(query)

    def create_doctor(self,id, name, specialty):
        query = """
        CREATE (d:Medecin {id:$id,nom: $name, specialite: $specialty})
        """
        parameters = {
            "id":id,
            "name": name,
            "specialty": specialty
        }
        self.db.query(query, parameters)

    def delete_doctor(self, doctor_id):
        query = """
        MATCH (d:Medecin)
        WHERE d.id = $doctor_id
        DELETE d
        """
        parameters = {
            "doctor_id": doctor_id
        }
        self.db.query(query, parameters)

    def search_doctors(self, specialty=None, name=None):
    # Construction dynamique du WHERE en fonction des paramètres fournis
      conditions = []
      parameters = {}

      if specialty:
        conditions.append("toLower(d.specialite) CONTAINS toLower($specialty)")
        parameters["specialty"] = specialty
    
      if name:
        conditions.append("toLower(d.nom) CONTAINS toLower($name)")
        parameters["name"] = name

    # Ajout de la clause WHERE seulement si des conditions existent
      if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)
      else:
        where_clause = ""

      query = f"""
      MATCH (d:Medecin)
      {where_clause}
      RETURN d.id AS id, d.nom AS name, d.specialite AS specialty
      """

      return self.db.query(query, parameters)
    
    def patients_par_medecins(self, doctor_id):
          query = """
    MATCH (m:Medecin {id: $doctor_id})-[:PLANIFIE]->(r:RendezVous)<-[:A_PRIS]-(p:Patient)
    RETURN count(DISTINCT p) AS total_patients
    """
          result = self.db.query(query, {"doctor_id": doctor_id})
          return result[0]['total_patients'] if result else 0
