from django.urls import path
from . import views

urlpatterns = [
    path('', views.diagnosis_form, name='diagnosis_form'),
    path('results/<int:case_id>/', views.get_prediction, name='get_prediction'),
]
