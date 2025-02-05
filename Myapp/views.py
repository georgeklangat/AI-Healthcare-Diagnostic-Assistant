import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, request
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from .models import Profile, Patient1, Diagnosis, Notification, Register

import pandas as pd
from django.shortcuts import render
import joblib
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
from django.conf import settings


def home(request):
    return render(request, 'homepage.html')


def about(request):
    return render(request, 'about.html')


def doctorsDashboard(request):
    if request.method == "POST":
        if Register.objects.filter(
                username=request.POST['username'],
                password=request.POST['password']

        ).exists():
            return render(request, 'homepage.html')
        else:
            return render(request, 'log-in.html')
    else:
        return render(request, 'doctors_dashboard.html')


@login_required
def dashboard(request):
    doctor = request.user.profile
    pending_cases = Diagnosis.objects.filter(doctor=doctor, patient__diagnosis_status='Pending')
    recent_cases = Diagnosis.objects.filter(doctor=doctor, patient__diagnosis_status='pending')
    updated_cases = Diagnosis.objects.filter(doctor=doctor, patient__diagnosis_status='Confirmed').order_by('-patient__updated_at')[:5]

    success_message = request.POST.get('success_message', None)

    notifications = Notification.objects.filter(user=request.user)
    return render(request, 'doctors_dashboard.html', {
        'pending_cases': pending_cases,
        'recent_cases': recent_cases,
        'updated_cases': updated_cases,
        'success_message': success_message,
        'notifications': notifications

    })


def fetch_patient_details(request, patient_id):
    try:
        patient = Patient1.objects.get(id=patient_id)

        predicted_disease = request.session.get('predicted_disease', 'Not Available')
        suggested_disease = request.session.get('suggested_disease', 'Not Available')
        next_steps = request.session.get('next_steps', {})

        # Retrieve predictions and next steps from session or databas
        data = {
            'name': patient.name,
            'age': patient.age,
            'gender': patient.gender,
            'symptoms': patient.symptoms,  # Corrected to match your model
            'notes': patient.notes,
            'predicted_disease': predicted_disease,
            'suggested_disease': suggested_disease,
            'next_steps': next_steps,
        }
        return JsonResponse(data)
    except Patient1.DoesNotExist:
        return JsonResponse({'error': 'Patient not found'}, status=404)


# @login_required
# def patient_input(request):
#     return render(request, 'diagnosis_form.html')


def result(request):
    return render(request, 'results.html')

def register(request):
    if request.method == 'POST':
        users = Register(
            firstName = request.POST['firstName'],
            secondName = request.POST['secondName'],
            email = request.POST['email'],
            password = request.POST['password']
        )
        users.save()
        return redirect('/login')
    else:
        return render(request, 'register.html')
def login(request):
    return render(request, 'log-in.html')


@login_required
def patient_input(request):
    if request.method == 'POST':
        patient_name = request.POST.get('patient-name')
        patient_age = request.POST.get('patient-age')
        patient_gender = request.POST.get('patient-gender')
        symptoms = request.POST.get('symptoms')

        Patient1.objects.create(name=patient_name, age=patient_age, gender=patient_gender, symptoms=symptoms)

        # Save the details in the session or pass as query parameters
        request.session['patient_name'] = patient_name
        request.session['patient_age'] = patient_age
        request.session['patient_gender'] = patient_gender
        request.session['symptoms'] = symptoms

        # Redirect to the prediction view
        return redirect('predict_view')
    else:
        return render(request, 'patient_dashboard.html',{'user': request.user})

# Load the trained model, vectorizer, and label encoder from local directory
rf_model = joblib.load(settings.MODEL_FILE_PATH)
vectorizer = joblib.load(settings.VECTORIZER_FILE_PATH)
label_encoder = joblib.load(settings.LABEL_ENCODER_FILE_PATH)

# Example: Load your dataset (this could be from a CSV or a database)
try:
    data = pd.read_csv('data/disease_symptoms.csv')
except FileNotFoundError:
    data = None


def predict_view(request):
    # Retrieve patient details from the session
    patient_name = request.session.get('patient_name')
    patient_age = request.session.get('patient_age')
    patient_gender = request.session.get('patient_gender')
    symptoms = request.session.get('symptoms')

    predicted_disease = None
    suggested_disease = None
    symptoms_list = symptoms.split(',') if symptoms else []

    if symptoms:
        # Format symptoms and predict
        symptoms_formatted = ' '.join(symptoms_list)
        symptoms_vectorized = vectorizer.transform([symptoms_formatted])
        predicted_disease_idx = rf_model.predict(symptoms_vectorized)
        predicted_disease = label_encoder.inverse_transform(predicted_disease_idx)[0]

        # Find the most similar symptoms in the dataset using cosine similarity
        similarity_scores = cosine_similarity(symptoms_vectorized, vectorizer.transform(data['Symptoms']))
        most_similar_idx = np.argmax(similarity_scores)
        suggested_disease = data['Disease'].iloc[most_similar_idx]

    next_steps = None
    if predicted_disease:
        next_steps = {
            'tests': "Blood Test,X-ray",
            'treatments': "Antibiotics,Rest,Hydration"
        }

    # Pass context to results.html
    context = {
        'patient_name': patient_name,
        'patient_age': patient_age,
        'patient_gender': patient_gender,
        'symptoms': symptoms_list,
        'predicted_disease': predicted_disease,
        'suggested_disease': suggested_disease,
        'next_steps': next_steps
    }
    return render(request, 'results.html', context)


def get_pending_patients(request):
    patients = Patient1.objects.all().values('name', 'age', 'gender')
    return JsonResponse(list(patients), safe=False)


@login_required
@csrf_exempt  # Use cautiously; ideally include CSRF protection in production
def update_diagnosis_status(request, patient_id):
    if request.method == 'POST':
        try:
            # Parse JSON data from the request body
            data = json.loads(request.body)
            new_status = data.get('status', 'Confirmed')  # Default to 'Confirmed'

            # Fetch the Diagnosis object
            diagnosis = get_object_or_404(Diagnosis, patient__id=patient_id)
            diagnosis.status = new_status
            diagnosis.save()

            return JsonResponse({'status': 'success', 'new_status': new_status})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'failure', 'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'failure', 'error': str(e)}, status=500)
    return JsonResponse({'status': 'failure', 'error': 'Invalid request method'}, status=400)


def diagnosis_detail(request, patient_id):
    # Retrieve the patient based on the provided patient_id
    patient = get_object_or_404(Patient1, id=patient_id)

    # Retrieve the diagnosis associated with the patient
    diagnosis = Diagnosis.objects.filter(patient=patient).first()

    # If no diagnosis exists, handle that scenario
    if not diagnosis:
        return render(request, 'no_diagnosis.html', {'patient': patient})

    # Pass the patient and diagnosis data to the template
    return render(request, 'diagnosis_detail.html', {
        'patient': patient,
        'diagnosis': diagnosis
    })


def no_diagnosis(request):
    return render(request, 'no_diagnosis.html', {'patient': Patient1.objects.all()})


def create_notification(request, doctor, patient_name, predicted_disease):
    # Ensure the `doctor` parameter is used instead of overwriting it.
    message = f"New diagnosis prediction for {patient_name}: {predicted_disease}"
    notification = Notification(doctor=doctor, message=message)
    notification.save()


def make_diagnosis(request):
    patient_name = "George"
    predicted_disease = "Flu"
    doctor = request.user

    create_notification(request, doctor, patient_name, predicted_disease)

    return redirect('/dashboard/?success_message=Diagnosis and notification sent succesfully!')
