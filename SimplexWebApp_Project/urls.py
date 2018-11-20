from django.contrib import admin
from django.urls import path
from simplex.views import homeView,simplex_input,simplex_calculate


urlpatterns = [
    path('', homeView),
    path('simplex_input/', simplex_input),
    path('simplexCalculate/',simplex_calculate),
  

]
