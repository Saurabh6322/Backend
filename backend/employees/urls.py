from django.urls import path,include
from . import views

urlpatterns = [

    path('', views.employee_home),
    
    path('add/', views.add_employee),

    path('search/<int:emp_id>/', views.search_employee),

    path('delete/<int:emp_id>/', views.delete_employee),

    path('list/', views.get_employees),

    path('countries/', views.get_countries),

    path('states/<str:country>/', views.get_states),

    path('cities/<str:state>/', views.get_cities),

    path('login/', views.login_user),

    path('register/', views.register_user),

    path('update/<int:emp_id>/', views.update_employee),

    path('auth/success/', views.oauth_success_redirect),
    
]
