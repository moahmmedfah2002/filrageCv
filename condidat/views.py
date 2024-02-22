from django.shortcuts import render
from django.http import HttpResponse
import sqlite3 as sql

dummy_data = [
    {
        "title": "Full Stack Web Developer",
        "description": "We are seeking a talented Full Stack Web Developer to join our team. The ideal candidate will have experience with both front-end and back-end development technologies.",
        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Node.js",
            "Express",
            "MongoDB",
        ],
    },
    {
        "title": "Electronics Engineer",
        "description": "We are looking for an Electronics Engineer to design and develop electronic circuits and systems. The candidate should have strong skills in analog and digital circuit design.",
        "skills": [
            "Analog Circuit Design",
            "Digital Circuit Design",
            "PCB Layout",
            "Microcontrollers",
            "Embedded Systems",
        ],
    },
    {
        "title": "Front-End Developer",
        "description": "We have an opening for a Front-End Developer to work on creating beautiful and responsive user interfaces. The ideal candidate should have a strong understanding of front-end technologies and frameworks.",
        "skills": ["HTML", "CSS", "JavaScript", "React", "Vue.js", "Angular"],
    },
    {
        "title": "Embedded Software Engineer",
        "description": "We are seeking an Embedded Software Engineer to develop firmware and software for embedded systems. The candidate should have experience with programming microcontrollers and debugging embedded software.",
        "skills": ["C/C++", "Embedded C", "RTOS", "ARM Cortex-M", "SPI", "I2C"],
    },
    {
        "title": "Back-End Developer",
        "description": "We are looking for a Back-End Developer to work on server-side logic and database management. The ideal candidate should have experience with backend technologies and frameworks.",
        "skills": ["Python", "Django", "Flask", "Node.js", "Express", "SQL"],
    },
    {
        "title": "UI/UX Designer",
        "description": "We have an opening for a UI/UX Designer to create intuitive and visually appealing user interfaces. The candidate should have a strong portfolio showcasing design skills.",
        "skills": ["UI Design", "UX Design", "Adobe XD", "Sketch", "Figma"],
    },
    {
        "title": "Hardware Engineer",
        "description": "We are seeking a Hardware Engineer to design and develop electronic hardware components. The candidate should have experience with schematic capture and PCB design tools.",
        "skills": [
            "Schematic Capture",
            "PCB Design",
            "Altium Designer",
            "KiCad",
            "Signal Integrity",
        ],
    },
    {
        "title": "Firmware Engineer",
        "description": "We are looking for a Firmware Engineer to develop low-level software for embedded systems. The candidate should have experience with firmware development and debugging.",
        "skills": ["C", "Assembly", "Embedded Systems", "RTOS", "Device Drivers"],
    },
]


# from .models import UploadFileForm
def index(request):
    return render(request, "condidat.html", {"data": dummy_data})


def search_job_offers(request):
    search_query = request.GET.get("search")

    filtered_jobs = []
    if search_query:
        search_query = search_query.lower()
        filtered_jobs = [
            offer
            for offer in dummy_data
            if search_query in offer["title"].lower()
            or search_query in offer["description"].lower()
            or any(search_query in skill.lower() for skill in offer["skills"])
        ]
    else:
        filtered_jobs = dummy_data

    return render(request, "condidat.html", {"data": filtered_jobs})


def offer_details(request, slug):
    selected_offer = None
    for offer in dummy_data:
        if offer["title"].lower().replace(" ", "-") == slug:
            selected_offer = offer
            break

    if selected_offer is not None:
        return render(request, "offer-details.html", {"offer": selected_offer})

    return HttpResponse("404\nOffer Not Found")


"""
def handle_uploaded_file(f):
    with open("some/file/name.txt", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)
"""


def upload_file(request):
    if request.method == "POST":
        print("POST method")
        """"
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES["file"])
            return render(request, "condidat.html")
        """
    else:
        # form = UploadFileForm()
        print("Not POST method")

    return render(request, "upload.html")


def upload(request):

    return render(request, "upload.html")
