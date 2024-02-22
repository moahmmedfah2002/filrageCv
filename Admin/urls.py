from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name="test"),
    path("/candidate",views.candidate, name="candidate")
]
