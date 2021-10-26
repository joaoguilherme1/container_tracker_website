from django.urls import path, register_converter

from . import views, converters

register_converter(converters.ConversorNumeroContainer, "AAAADDDDDDD")

urlpatterns = [
    path("", views.index, name="index"),
    path("<AAAADDDDDDD:container_number>", views.resultados, name="resultados"),
    path("procura", views.procura, name="procura")
]
