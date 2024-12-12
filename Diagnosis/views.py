from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import PatientCase
from .ai_model import predict_disease
from django.contrib.auth.decorators import login_required


# View for the diagnosis form and symptom input page

def diagnosis_form(request):
    if request.method == 'POST':
        # Extract form data
        patient_name = request.POST.get('patientName')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        symptoms = request.POST.getlist('symptoms')

        # Save patient case to database
        case = PatientCase.objects.create(
            patient_name=patient_name,
            age=age,
            gender=gender,
            symptoms=symptoms
        )

        # Redirect to results page with case_id
        return redirect('get_prediction', case_id=case.id)

    return render(request, 'diagnosis_form.html')


# View for displaying the diagnosis results
def get_prediction(request, case_id):
    case = get_object_or_404(PatientCase, id=case_id)
    if request.method == 'GET':
        # Predict the disease using AI
        prediction = predict_disease(case.symptoms)

        # Save the prediction result
        case.diagnosis_results = prediction
        case.save()

        # Render results template with prediction
        return render(request, 'results.html', {'case': case, 'prediction': prediction})


# View for rendering the results template directly

def result(request):
    return render(request, 'results.html')
