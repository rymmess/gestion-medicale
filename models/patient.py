class PatientModel :
   def __init__(self, db):
      self.db = db

   def get_all_patients(self):
      query = """
      MATCH (p:Patient)
      RETURN p.id as id, p.name AS name, p.age AS age , p.sexe as sexe
      """
      return self.db.query(query)

   def get_patient_by_id(self, patient_id):
      query = "MATCH (p:Patient {id: $patient_id}) RETURN p"
      parameters = {'patient_id': patient_id}
      result = self.db.query(query, parameters)
      print(result)  # Debugging
      if result:
         return result[0]  
      return None



   def create_patient(self,name,age,sexe,id):
         query="""
         CREATE (p:Patient {id:$id,nom:$name,age:$age,sexe:$sexe})
         """
         parameters={
            "id":id,
            "name":name,
            "age":age,
            "sexe":sexe
         }
         self.db.query(query,parameters)
         
   def nombre_reservations(self ,id):
         query="""
         MATCH (p:Patient {id: $id})-[:A_PRIS]->(r:RendezVous)
         RETURN count(r) AS total_reservations
         """
         result=self.db.query(query,{"id":id})
         return result[0]['total_reservations'] if result else 0