from django.shortcuts import render,redirect
from django.http import HttpRequest,HttpResponse
import json
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
import sqlite3 as sql



def home(request):
    return render(request,'home.html')


def logup(request):
    cur=sql.connect("db.sqlite3")
    
    if request.method == 'POST':
        if request.POST["type"]=="condidat":
            password=request.POST['password']
            confirmation=request.POST['confirmation']
            if password!=confirmation:
                return render(request,"logup.html",context={"erreur":"entrez le meme mot de pass "})  
            else:
                email=request.POST["email"]
                nom=request.POST["nom"]
                tel=request.POST["tel"]
                prenom=request.POST["prenom"]
                password=request.POST["password"]
                query=cur.execute("insert into Login_condidat(email,nom,prenom,tel,password) values('{}','{}','{}','{}','{}')".format(email,nom,prenom,tel,password))
                cur.commit()
                return redirect('/Login')
        elif request.POST["type"]=="recruteur":
            password=request.POST['password']
            confirmation=request.POST['confirmation']
            if password!=confirmation:
                return render(request,"logup.html",context={"erreur":"entrez le meme mot de pass "})
            else:
                email=request.POST["email"]
                nom=request.POST["nom"]
                tel=request.POST["tel"]
                entreprise=request.POST["entreprise"]
                numero=request.POST["numero_patent"]
                prenom=request.POST["prenom"]
                password=request.POST["password"]
                query=cur.execute("insert into Login_recruteur(email,nom,prenom,telephone,entreprise,numero_patent,password) values('{}','{}','{}','{}','{}','{}','{}')".format(email,nom,prenom,tel,entreprise,numero,password))
                cur.commit()
                return redirect('/Login')

    
    
    return render(request,'logup.html',context={"erreur":"choisire le type d'insciption"})   

   

def login(request):
    cur=sql.connect("db.sqlite3")
    email=""
    password=""
    if request.method=='POST':
            try:
                email=request.POST['email']
                password=request.POST['password']
            except:
                print("Vide")
            
            result=cur.execute("SELECT email,password from Login_condidat WHERE email like'{}' and password like '{}'".format(email,password))
            result=result.fetchall()
           
            if result!=[]:
                return redirect('home')
       
            
    return render(request,"login.html")

    




        
    
    