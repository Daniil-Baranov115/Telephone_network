from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('make_call/', views.make_call, name='make_call'),
    path('topup/', views.topup_balance, name='topup'),
    path('history/', views.call_history, name='history'),
    path('change_tariff/', views.change_tariff, name='change_tariff'),
    path('admin-panel/', views.admin_dashboard,
         name='admin_dashboard'),  
    path('logout/', views.logout_view, name='logout'),
    path('api/process_call/', views.api_process_call, name='api_process_call'),
]
