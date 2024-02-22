from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("verif", views.upload_file, name="redirect"),
    path(
        "condidature", views.upload, name="condidation"
    ),  # route vers details off +telechr cv
    path("search-job-offers", views.search_job_offers, name="search-job-offers"),
]
