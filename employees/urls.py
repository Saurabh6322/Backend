from django.urls import path
from . import views

urlpatterns = [

    path('', views.employee_home),
    
    path('add/', views.add_employee),

    path('search/<int:emp_id>/', views.search_employee),

    path('delete/<int:emp_id>/', views.delete_employee),

    path('list/', views.get_employees),
]