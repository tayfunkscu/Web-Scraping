from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("frekans", views.frekans, name="frekans"),
    path("frekansResult", views.frekansResult, name="frekansResult"),
]