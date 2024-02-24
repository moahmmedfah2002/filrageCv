from django.urls import path
from . import views

from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("job/", views.job_search_list, name="job-search-list"),
    path("job/<slug>", views.job_detail, name="job-detail"),
    path("relevant_jobs/", views.intelligent_search, name="intelligent-search"),
    path("profile/", views.my_profile, name="my-profile"),
    path("profile/edit/", views.edit_profile, name="edit-profile"),
    path("profile/<slug>", views.profile_view, name="profile-view"),
    path("introduction/", views.candidate_details, name="detail-candidates"),
    path("delete_skills/", views.delete_skill, name="skill-delete"),
    path("search-job-offers/", views.search_job_offers, name="search-job-offers"),
]
