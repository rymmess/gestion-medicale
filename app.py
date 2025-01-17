from flask import Flask, flash, redirect, render_template, request, url_for
from config import Config
from utils.database import Database
from models.doctor import DoctorModel
from models.patient import PatientModel
from models.appointment import AppointmentModel
from models.pathology import PathologyModel
from models.treatment import TreatmentModel

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'une_clé_secrète_unique_aleatoire'

# Initialize database connection
db = Database(Config.NEO4J_URI, Config.NEO4J_USER, Config.NEO4J_PASSWORD)
doctor_model = DoctorModel(db)
patient_model=PatientModel(db)
appointment_model=AppointmentModel(db)
pathology_model = PathologyModel(db)
treatment_model = TreatmentModel(db)

@app.route('/')
def home():
    return render_template("doctors.html")
    #doctors = doctor_model.get_all_doctors()
    #return render_template("doctors.html", doctors=doctors)


@app.route('/get_doctors', endpoint='get_doctors')
def get_doctors():
    doctors = doctor_model.get_all_doctors()
    patients_count = {
        doctor['id']: doctor_model.patients_par_medecins(doctor['id'])
        for doctor in doctors
    }
    
    return render_template('doctor_list.html', doctors=doctors,patients_count=patients_count)


@app.route('/create_doctor', methods=['GET', 'POST'])
def create_doctor():
    if request.method == 'POST':
        id=request.form['id']
        name = request.form['name']
        specialty = request.form['specialty']
        doctor_model.create_doctor(id,name, specialty)
        return redirect(url_for('get_doctors'))
    return render_template('create_doctor.html')


@app.route('/delete_doctor/<doctor_id>', methods=['GET', 'POST'])
def delete_doctor(doctor_id):
    doctor_model.delete_doctor(doctor_id)
    return redirect(url_for('get_doctors'))


@app.route('/search_doctors', methods=['GET', 'POST'])
def search_doctors():
    specialty = request.args.get('specialty')
    name = request.args.get('name')
    doctors = doctor_model.search_doctors(specialty,name)
    return render_template('search_doctors.html', doctors=doctors)


@app.route('/get_patients', endpoint='get_patients')
def get_patients():
    patients = patient_model.get_all_patients()
    reservations_count = {
        patient['id']: patient_model.nombre_reservations(patient['id'])
        for patient in patients
    }
    return render_template('patient_list.html', patients=patients,reservations_count=reservations_count)


@app.route('/create_patients',methods=['GET', 'POST']) 
def create_patients():
    if request.method == 'POST':
        id=request.form['id']
        name = request.form['name']
        age  = request.form['age']
        sexe=request.form['sexe']
        patient_model.create_patient(name, age,sexe,id)
        return redirect(url_for('get_patients'))
    return render_template('create_patient.html')


@app.route('/create_appointment/<patient_id>', methods=['GET', 'POST'])
def create_appointment(patient_id):
    if request.method == 'POST':
        # Récupération des données du formulaire
        doctor_id = request.form['doctor_id']
        date = request.form['date']
        time = request.form['time']
        # Vérifiez si un rendez-vous existe déjà entre ce patient et ce médecin à cette date
        if appointment_model.check_appointment_exists(patient_id, doctor_id, date,time):
            flash("Ce rendez-vous existe déjà.", "error")
            return redirect(url_for('create_appointment', patient_id=patient_id)) 
        else:
            # Créez le rendez-vous si nécessaire
            appointment_model.create_appointment(patient_id, doctor_id, date,time)
            flash("Rendez-vous créé avec succès.", "success")
            return redirect(url_for('appointment_list', doctor_id=doctor_id))  # Redirection pour afficher le message flash
    # Récupération des médecins pour afficher dans le formulaire
    doctors = doctor_model.get_all_doctors()
    patient = patient_model.get_patient_by_id(patient_id)

    return render_template('create_appointment.html', patient=patient, doctors=doctors)


@app.route('/appointments/<doctor_id>')
def appointment_list(doctor_id):
    # Récupérer les rendez-vous du médecin en fonction de son ID
    query = """
        MATCH (d:Medecin {id: $doctor_id})-[:PLANIFIE]->(r:RendezVous)<-[:A_PRIS]-(p:Patient)
        RETURN r.id AS rendezvous_id, r.date AS date, r.time AS time, p.nom AS patient_name
        ORDER BY r.date, r.time
        LIMIT 7
    """
    parameters = {'doctor_id': doctor_id}
    appointments = db.query(query, parameters)
    
    # Passer les résultats à la page HTML
    return render_template('appointment_list.html', appointments=appointments, doctor_id=doctor_id)

# afficher toutes les pathologies

@app.route('/pathologies', methods=['GET'])
def list_pathologies():
    pathologies = pathology_model.get_all_pathologies()
    return render_template('pathology_list.html', pathologies=pathologies)

# creer pathologie 

@app.route('/create_pathology', methods=['GET', 'POST'])
def create_pathology():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        propriete = request.form['propriete']
        pathology_model.create_pathology(id,name, propriete)
        return redirect(url_for('list_pathologies'))
    return render_template('create_pathology.html')


#update pathologie

@app.route('/update_pathology/<pathology_id>', methods=['GET', 'POST'])
def update_pathology(pathology_id):
    pathology = pathology_model.get_pathology_by_id(pathology_id)
    if not pathology:
        flash("Pathologie introuvable.", "error")
        return redirect(url_for('list_pathologies'))

    if request.method == 'POST':
        name = request.form['name']
        propriete = request.form['propriete']
        # Appelle de la méthode pour mettre à jour la pathologie
        pathology_model.update_pathology(pathology_id, name, propriete)
        flash("Pathologie mise à jour avec succès.", "success")
        return redirect(url_for('list_pathologies'))

    return render_template('update_pathology.html', pathology=pathology)


# supprimer pathologie 

@app.route('/delete_pathology/<pathology_id>', methods=['POST'])
def delete_pathology(pathology_id):
    try:
        pathology_model.delete_pathology(pathology_id)
        flash("Pathologie supprimée avec succès.", "success")
    except Exception as e:
        flash(f"Erreur lors de la suppression : {str(e)}", "error")
    return redirect(url_for('list_pathologies'))


@app.route('/patient_pathology', methods=['GET'])
def get_patient_pathology():
    patient_list = patient_model.get_all_patients()
    resultats = []
    for patient in patient_list:
        # Récupère les pathologies pour le patient
        pathologies = appointment_model.get_pathologies_for_patient(patient["id"])
        
        # Vérifie si des pathologies existent pour ce patient
        if pathologies:
            pathology = pathologies[0]  # Utilise le premier élément de la liste de pathologies
            # Récupère les traitements pour la pathologie
            treatments = appointment_model.get_treatments_for_pathology(pathology["id"])
            
            # Vérifie si des traitements existent pour cette pathologie
            if treatments:
                treatment = treatments[0]  # Utilise le premier traitement trouvé
                resultats.append({
                    "patient": patient["name"],
                    "pathologie": pathology["name"],
                    "traitement": treatment["name"]
                })
        
    return render_template('patient_diagnostic.html', resultats=resultats)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
