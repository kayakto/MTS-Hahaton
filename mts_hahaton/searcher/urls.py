from django.urls import path
from . import views

urlpatterns = [
    path('import_excel', views.import_excel),
    path('search/filters/<str:search_text>', views.search_filters),
]
