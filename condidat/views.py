from django.shortcuts import render
from django.http import HttpResponse
import sqlite3 as sql
from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile, Skill
from .forms import ProfileUpdateForm, NewSkillForm
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator


"""
    This Data will come from a db or ...
    Testing purposes only HERE.
"""
fake_data_for_testing = [
    {
        "title": "Web Developer",
        "description": "We are looking for a skilled web developer to join our team. The ideal candidate should have experience in building responsive web applications using modern web technologies.",
        "skills": ["HTML", "CSS", "JavaScript", "React", "Node.js"],
    },
    {
        "title": "Frontend Engineer",
        "description": "Join our innovative frontend team to work on cutting-edge web applications. We need someone proficient in JavaScript frameworks like Angular or Vue.js, with a strong eye for design and user experience.",
        "skills": ["JavaScript", "HTML", "CSS", "Angular", "Vue.js"],
    },
    {
        "title": "Backend Developer",
        "description": "We're seeking a backend developer to help build and maintain robust server-side applications. Experience with databases, server frameworks like Express.js, and proficiency in languages like Python or Java are required.",
        "skills": ["Node.js", "Express.js", "Python", "Java", "SQL"],
    },
    {
        "title": "Electronics Engineer",
        "description": "Exciting opportunity for an electronics engineer to work on cutting-edge projects. The ideal candidate will have experience with circuit design, PCB layout, and proficiency in simulation software like SPICE.",
        "skills": [
            "Circuit Design",
            "PCB Layout",
            "SPICE",
            "Analog Electronics",
            "Digital Electronics",
        ],
    },
    {
        "title": "Embedded Systems Developer",
        "description": "Join our team of embedded systems developers to work on IoT and embedded projects. Experience with microcontrollers, firmware development, and communication protocols like MQTT or BLE is required.",
        "skills": [
            "Embedded Systems",
            "Microcontrollers",
            "Firmware Development",
            "MQTT",
            "BLE",
        ],
    },
]


def home(request):
    context = {
        "home_page": "active",
        "data": fake_data_for_testing,
    }
    return render(request, "condidat.html", context)


def search_job_offers(request):
    query = request.GET.get("search")
    filtered_offers = []

    if query:
        query = query.lower()
        """
            This logic will change when using real data from database
            to use the built in functions of sqlite
        """
        filtered_offers = [
            job_offer
            for job_offer in fake_data_for_testing
            if (
                query in job_offer["title"].lower()
                or query in job_offer["description"].lower()
                or any(query in skill.lower() for skill in job_offer["skills"])
            )
        ]
    else:
        filtered_offers = fake_data_for_testing

    context = {"data": filtered_offers, "query": query}
    return render(request, "condidat.html", context)


def job_search_list(request):
    query = request.GET.get("p")
    loc = request.GET.get("q")
    object_list = []
    if query == None:
        object_list = Job.objects.all()
    else:
        title_list = Job.objects.filter(title__icontains=query).order_by("-date_posted")
        skill_list = Job.objects.filter(skills_req__icontains=query).order_by(
            "-date_posted"
        )
        company_list = Job.objects.filter(company__icontains=query).order_by(
            "-date_posted"
        )
        job_type_list = Job.objects.filter(job_type__icontains=query).order_by(
            "-date_posted"
        )
        for i in title_list:
            object_list.append(i)
        for i in skill_list:
            if i not in object_list:
                object_list.append(i)
        for i in company_list:
            if i not in object_list:
                object_list.append(i)
        for i in job_type_list:
            if i not in object_list:
                object_list.append(i)
    if loc == None:
        locat = Job.objects.all()
    else:
        locat = Job.objects.filter(location__icontains=loc).order_by("-date_posted")
    final_list = []
    for i in object_list:
        if i in locat:
            final_list.append(i)
    paginator = Paginator(final_list, 20)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "jobs": page_obj,
        "query": query,
    }
    return render(request, 'condidat.html', context)

    return render(request, "condidat.html", context)



def job_detail(request, slug):
    job = get_object_or_404(Job, slug=slug)
    apply_button = 0
    save_button = 0
    profile = Profile.objects.filter(user=request.user).first()
    if AppliedJobs.objects.filter(user=request.user).filter(job=job).exists():
        apply_button = 1
    if SavedJobs.objects.filter(user=request.user).filter(job=job).exists():
        save_button = 1
    relevant_jobs = []
    jobs1 = Job.objects.filter(company__icontains=job.company).order_by("-date_posted")
    jobs2 = Job.objects.filter(job_type__icontains=job.job_type).order_by(
        "-date_posted"
    )
    jobs3 = Job.objects.filter(title__icontains=job.title).order_by("-date_posted")
    for i in jobs1:
        if len(relevant_jobs) > 5:
            break
        if i not in relevant_jobs and i != job:
            relevant_jobs.append(i)
    for i in jobs2:
        if len(relevant_jobs) > 5:
            break
        if i not in relevant_jobs and i != job:
            relevant_jobs.append(i)
    for i in jobs3:
        if len(relevant_jobs) > 5:
            break
        if i not in relevant_jobs and i != job:
            relevant_jobs.append(i)

    return render(request, 'offer-details.html', {'job': job, 'profile': profile, 'apply_button': apply_button, 'save_button': save_button, 'relevant_jobs': relevant_jobs, 'candidate_navbar': 1})

    return render(
        request,
        "offer-details.html",
        {
            "job": job,
            "profile": profile,
            "apply_button": apply_button,
            "save_button": save_button,
            "relevant_jobs": relevant_jobs,
            "candidate_navbar": 1,
        },
    )

@login_required
def intelligent_search(request):
    relevant_jobs = []
    common = []
    job_skills = []
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    my_skill_query = Skill.objects.filter(user=user)
    my_skills = []
    for i in my_skill_query:
        my_skills.append(i.skill.lower())
    if profile:
        jobs = Job.objects.filter(job_type=profile.looking_for).order_by("-date_posted")
    else:
        jobs = Job.objects.all()
    for job in jobs:
        skills = []
        sk = str(job.skills_req).split(",")
        for i in sk:
            skills.append(i.strip().lower())
        common_skills = list(set(my_skills) & set(skills))
        if len(common_skills) != 0 and len(common_skills) >= len(skills) // 2:
            relevant_jobs.append(job)
            common.append(len(common_skills))
            job_skills.append(len(skills))
    objects = zip(relevant_jobs, common, job_skills)
    objects = sorted(objects, key=lambda t: t[1] / t[2], reverse=True)
    objects = objects[:100]
    context = {
        "intel_page": "active",
        "jobs": objects,
        "counter": len(relevant_jobs),
    }
    return render(request, "condidat.html", context)


@login_required
def my_profile(request):
    you = request.user
    profile = Profile.objects.filter(user=you).first()
    user_skills = Skill.objects.filter(user=you)
    if request.method == "POST":
        form = NewSkillForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = you
            data.save()
            return redirect("my-profile")
    else:
        form = NewSkillForm()
    context = {
        "u": you,
        "profile": profile,
        "skills": user_skills,
        "form": form,
        "profile_page": "active",
    }
    return render(request, "condidat.html", context)


@login_required
def edit_profile(request):
    you = request.user
    profile = Profile.objects.filter(user=you).first()
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = you
            data.save()
            return redirect("my-profile")
    else:
        form = ProfileUpdateForm(instance=profile)
    context = {
        "form": form,
    }
    return render(request, "condidat.html", context)


@login_required
def profile_view(request, slug):
    p = Profile.objects.filter(slug=slug).first()
    you = p.user
    user_skills = Skill.objects.filter(user=you)
    context = {
        "u": you,
        "profile": p,
        "skills": user_skills,
    }
    return render(request, "condidat.html", context)


def candidate_details(request):
    return render(request, "condidat.html")


@login_required
@csrf_exempt
def delete_skill(request, pk=None):
    if request.method == "POST":
        id_list = request.POST.getlist("choices")
        for skill_id in id_list:
            Skill.objects.get(id=skill_id).delete()
        return redirect("my-profile")
