from django.urls import path
from . import views

urlpatterns = [
    path('search/filters/<str:search_text>', views.search_filters),
    path('search', views.search_by_filters),
    path('hierarchy', views.get_hierarchy),
    path('employee/<int:employee_id>', views.get_employee),
    path('employee/<int:employee_id>/hierarchy', views.get_employee_branch),
]
