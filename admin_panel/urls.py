from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.admin_users, name='admin_users'),
    path('users/<int:pk>/toggle/', views.admin_toggle_user, name='admin_toggle_user'),
    path('users/<int:pk>/delete/', views.admin_delete_user, name='admin_delete_user'),
    path('jobs/', views.admin_jobs, name='admin_jobs'),
    path('jobs/post/', views.admin_post_job, name='admin_post_job'),
    path('jobs/<int:pk>/edit/', views.admin_edit_job, name='admin_edit_job'),
    path('jobs/<int:pk>/toggle/', views.admin_toggle_job, name='admin_toggle_job'),
    path('jobs/<int:pk>/delete/', views.admin_delete_job, name='admin_delete_job'),
    path('applications/', views.admin_applications, name='admin_applications'),
    path('applications/<int:pk>/update/', views.admin_update_application, name='admin_update_application'),
    path('questions/', views.admin_questions, name='admin_questions'),
    path('questions/add/', views.admin_add_question, name='admin_add_question'),
path('questions/<int:pk>/edit/', views.admin_edit_question, name='admin_edit_question'),
    path('questions/<int:pk>/delete/', views.admin_delete_question, name='admin_delete_question'),
    path('messages/', views.admin_messages, name='admin_messages'),
    path('messages/<int:pk>/toggle/', views.admin_toggle_message, name='admin_toggle_message'),
    path('messages/<int:pk>/delete/', views.admin_delete_message, name='admin_delete_message'),
]
