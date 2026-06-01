from django.urls import path
from . import views

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<int:pk>/', views.job_detail, name='job_detail'),
    path('<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('<int:pk>/save/', views.save_job, name='save_job'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('post/', views.post_job, name='post_job'),
    path('<int:pk>/edit/', views.edit_job, name='edit_job'),
    path('<int:pk>/delete/', views.delete_job, name='delete_job'),
    path('recent-applications/', views.recent_applications, name='recent_applications'),
    path('<int:job_pk>/applications/', views.view_applications, name='view_applications'),
    path('application/<int:app_pk>/update/', views.update_application_status, name='update_application_status'),
]

