from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
import sqlite3 as sql
from .models import Recruteur 

def index(request):
    return render(request,"admin-home.html")
def candidate(request):
    cur = sql.connect("db.sqlite3")
    result=cur.execute("SELECT * FROM condidat")
    result=result.fetchall()
    if request.method=="POST":
        id=request.POST["id"]
        cur.execute("DELETE FROM condidat WHERE id={}".format(id))
        cur.commit()
        return render(request,"candidate.html",context={"condidats":result})
    return render(request,"candidate.html",context={"condidats":result})
def recruteur(request):
    items = Recruteur.objects.all()
    return render(request,"recruteur.html",{"recruteurs":items})
def delete_recruteur(request, recruteur_id):
    recrut = Recruteur.objects.filter(pk = recruteur_id)
    recrut.delete()
    return redirect("recruteur")