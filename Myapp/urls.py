from django.urls import path
from Myapp import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('result/', views.result, name='result'),

    path('patient_dashboard/', views.patient_input, name='patient_dashboard'),
    path('about/', views.about, name='about'),

    path('predict/', views.predict_view, name='predict_view'),
    path('fetch_patient_details/<int:patient_id>/', views.fetch_patient_details, name='fetch_patient_details'),
    path('update_diagnosis_status/<int:patient_id>/', views.update_diagnosis_status, name='update_diagnosis_status'),
    path('diagnosis/<int:patient_id>/', views.diagnosis_detail, name='diagnosis_detail'),
    path('no_diagnosis/', views.no_diagnosis, name='no_diagnosis'),
    path('update_diagnosis_status/<int:patient_id>/', views.update_diagnosis_status, name='update_diagnosis_status'),
]