from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name="test"),
    path("/candidate",views.candidate, name="candidate"),
    path("/recruteur",views.recruteur, name="recruteur"),
    path("delete_recruteur/<recruteur_id>",views.delete_recruteur,name = "delete_recruteur")

]
