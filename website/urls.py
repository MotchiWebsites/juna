from django.urls import path

from . import views

app_name = "website"

urlpatterns = [
    path("", views.home, name="home"),
    path("contact/submit/", views.submit_contact, name="submit_contact"),
]
