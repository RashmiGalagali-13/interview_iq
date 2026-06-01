from django.urls import path
from . import views

urlpatterns = [
    path('', views.question_bank, name='question_bank'),
    path('<int:pk>/practice/', views.practice, name='practice'),
    path('history/', views.my_practice_history, name='practice_history'),
    path('company/<int:company_pk>/', views.company_interview_prep, name='company_interview_prep'),
]
