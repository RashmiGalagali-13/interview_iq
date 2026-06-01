from django.urls import path
from . import views

urlpatterns = [
    path('register/seeker/', views.register_seeker, name='register_seeker'),
    path('register/company/', views.register_company, name='register_company'),
    path('register/admin/', views.register_admin, name='register_admin'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/seeker/', views.seeker_dashboard, name='seeker_dashboard'),
    path('dashboard/company/', views.company_dashboard, name='company_dashboard'),
    path('profile/seeker/edit/', views.edit_seeker_profile, name='edit_seeker_profile'),
    path('dashboard/website/', views.company_website, name='company_website'),
    path('profile/company/edit/', views.edit_company_profile, name='edit_company_profile'),
    path('contact/', views.contact_view, name='contact'),
]
