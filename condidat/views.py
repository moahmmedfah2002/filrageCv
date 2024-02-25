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
        "title": "Backend Developer",
        "description": "We are looking for a Backend Developer to join our team. You will be responsible for building and maintaining the server-side logic of our web applications. If you have a strong understanding of server-side technologies and database management, we want to hear from you.",
        "date": "02/25/2024",
        "location": "Seattle, WA",
        "duration": "Full-time",
        "skills": ["Python", "Django", "RESTful APIs", "SQL", "AWS"],
        "requirements": [
            "Bachelor's degree in Computer Science or related field",
            "Proven experience in backend development",
            "Strong proficiency in Python and Django framework",
            "Experience with RESTful API development",
            "Knowledge of SQL and database management",
            "Familiarity with cloud platforms (e.g., AWS)",
            "Excellent problem-solving and debugging skills",
            "Effective communication and teamwork abilities",
        ],
        "advantages": [
            "Competitive salary and benefits package",
            "Opportunity to work on challenging projects",
            "Collaborative and supportive work environment",
            "Professional development and training opportunities",
            "Flexible work hours",
        ],
    },
    {
        "title": "UI/UX Designer",
        "description": "Join our team as a UI/UX Designer and help create engaging and intuitive user interfaces for our web applications. You will work closely with our development and product teams to design user-friendly experiences that meet our clients' needs.",
        "date": "02/25/2024",
        "location": "Los Angeles, CA",
        "duration": "Contract",
        "skills": ["UI/UX Design", "Wireframing", "Prototyping", "Adobe XD", "Sketch"],
        "requirements": [
            "Bachelor's degree in Design or related field",
            "Proven experience in UI/UX design",
            "Proficiency in wireframing and prototyping tools",
            "Strong visual design skills and attention to detail",
            "Experience with Adobe XD, Sketch, or similar software",
            "Understanding of user-centered design principles",
            "Excellent communication and collaboration skills",
            "Ability to iterate designs based on feedback",
        ],
        "advantages": [
            "Competitive compensation",
            "Opportunity to work with cross-functional teams",
            "Flexible work arrangements",
            "Exciting projects in various industries",
            "Room for creativity and innovation",
        ],
    },
    {
        "title": "Frontend Developer",
        "description": "We are seeking a Frontend Developer to join our team and help build responsive and user-friendly web interfaces. You will work closely with our design and backend teams to implement pixel-perfect designs and optimize performance.",
        "date": "02/25/2024",
        "location": "Chicago, IL",
        "duration": "Full-time",
        "skills": ["HTML", "CSS", "JavaScript", "React", "Responsive Design"],
        "requirements": [
            "Bachelor's degree in Computer Science or related field",
            "Proven experience in frontend development",
            "Strong proficiency in HTML, CSS, and JavaScript",
            "Experience with React or similar frontend frameworks",
            "Familiarity with responsive design principles",
            "Understanding of cross-browser compatibility issues",
            "Excellent problem-solving and debugging skills",
            "Ability to work in a fast-paced environment",
        ],
        "advantages": [
            "Competitive salary and benefits package",
            "Opportunity for career growth",
            "Collaborative and inclusive work culture",
            "Flexible work arrangements",
            "Exciting projects with modern technologies",
        ],
    },
    {
        "title": "Mobile App Developer",
        "description": "Join our team as a Mobile App Developer and help create innovative and user-friendly mobile applications for iOS and Android platforms. You will work closely with our design and backend teams to deliver high-quality mobile experiences.",
        "date": "02/25/2024",
        "location": "Austin, TX",
        "duration": "Full-time",
        "skills": [
            "iOS Development",
            "Android Development",
            "Swift",
            "Kotlin",
            "RESTful APIs",
        ],
        "requirements": [
            "Bachelor's degree in Computer Science or related field",
            "Proven experience in mobile app development",
            "Strong proficiency in iOS and/or Android development",
            "Experience with Swift, Kotlin, or similar languages",
            "Knowledge of RESTful API integration",
            "Understanding of mobile UI/UX design principles",
            "Excellent problem-solving and debugging skills",
            "Ability to work in a collaborative team environment",
        ],
        "advantages": [
            "Competitive salary and benefits package",
            "Opportunity for professional growth and development",
            "Flexible work hours and remote work options",
            "Collaborative and supportive team environment",
            "Exciting projects in the mobile technology space",
        ],
    },
    {
        "title": "Software Engineer",
        "description": "We are looking for a Software Engineer to join our team and help develop scalable and maintainable software solutions. You will work on various projects, from backend services to frontend applications, using cutting-edge technologies.",
        "date": "02/25/2024",
        "location": "San Diego, CA",
        "duration": "Full-time",
        "skills": ["Java", "Spring Boot", "Angular", "Microservices", "SQL"],
        "requirements": [
            "Bachelor's degree in Computer Science or related field",
            "Proven experience in software development",
            "Strong proficiency in Java and Spring Boot framework",
            "Experience with frontend frameworks such as Angular",
            "Knowledge of microservices architecture",
            "Familiarity with SQL and database management",
            "Excellent problem-solving and analytical skills",
            "Ability to work in a collaborative team environment",
        ],
        "advantages": [
            "Competitive compensation and benefits package",
            "Opportunity for career advancement",
            "Flexible work hours and remote work options",
            "Collaborative and supportive work culture",
            "Exciting projects with modern technologies",
        ],
    },
    {
        "title": "Web Designer",
        "description": "Join our team as a Web Designer and help create visually appealing and user-friendly websites. You will work closely with our development and marketing teams to design custom website layouts and graphics.",
        "date": "02/25/2024",
        "location": "Denver, CO",
        "duration": "Contract",
        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "Adobe Creative Suite",
            "Responsive Design",
        ],
        "requirements": [
            "Bachelor's degree in Design or related field",
            "Proven experience in web design",
            "Proficiency in HTML, CSS, and JavaScript",
            "Experience with Adobe Creative Suite (e.g., Photoshop, Illustrator)",
            "Understanding of responsive design principles",
            "Strong visual design skills and attention to detail",
            "Excellent communication and collaboration skills",
            "Ability to work on multiple projects simultaneously",
        ],
        "advantages": [
            "Competitive compensation",
            "Opportunity to work on diverse projects",
            "Flexible work arrangements",
            "Collaborative and supportive team environment",
            "Room for creativity and innovation",
        ],
    },
    {
        "title": "DevOps Engineer",
        "description": "We are seeking a DevOps Engineer to join our team and help streamline our development and deployment processes. You will be responsible for automating build, deployment, and monitoring tasks to ensure efficient and reliable software delivery.",
        "date": "02/25/2024",
        "location": "Portland, OR",
        "duration": "Full-time",
        "skills": ["CI/CD", "Docker", "Kubernetes", "AWS", "Terraform"],
        "requirements": [
            "Bachelor's degree in Computer Science or related field",
            "Proven experience in DevOps or software development",
            "Strong proficiency in CI/CD pipelines",
            "Experience with containerization technologies (e.g., Docker, Kubernetes)",
            "Knowledge of cloud platforms (e.g., AWS)",
            "Familiarity with infrastructure as code tools (e.g., Terraform)",
            "Excellent problem-solving and troubleshooting skills",
            "Ability to work in a collaborative team environment",
        ],
        "advantages": [
            "Competitive salary and benefits package",
            "Opportunity for professional growth and advancement",
            "Flexible work arrangements",
            "Collaborative and inclusive work culture",
            "Exciting projects with modern technologies",
        ],
    },
    {
        "title": "Software Developer",
        "description": "Join our team as a Software Developer and contribute to the design and development of innovative software solutions. You will work on various projects, from backend services to frontend applications, using a mix of programming languages and frameworks.",
        "date": "02/25/2024",
        "location": "Boston, MA",
        "duration": "Full-time",
        "skills": ["Python", "Java", "JavaScript", "React", "Django", "Spring Boot"],
        "requirements": [
            "Bachelor's degree in Computer Science or related field",
            "Proven experience in software development",
            "Strong proficiency in Python, Java, and JavaScript",
            "Experience with frontend frameworks such as React",
            "Knowledge of backend frameworks such as Django and Spring Boot",
            "Understanding of software development best practices",
            "Excellent problem-solving and analytical skills",
            "Ability to work in a collaborative team environment",
        ],
        "advantages": [
            "Competitive compensation and benefits package",
            "Opportunity for career advancement",
            "Flexible work hours and remote work options",
            "Collaborative and supportive work culture",
            "Exciting projects with modern technologies",
        ],
    },
    {
        "title": "Quality Assurance Engineer",
        "description": "We are looking for a Quality Assurance Engineer to join our team and help ensure the quality of our software products. You will be responsible for designing and implementing test plans, conducting automated and manual tests, and identifying and reporting defects.",
        "date": "02/25/2024",
        "location": "Atlanta, GA",
        "duration": "Full-time",
        "skills": [
            "Automated Testing",
            "Manual Testing",
            "Selenium",
            "Jenkins",
            "Agile",
        ],
        "requirements": [
            "Bachelor's degree in Computer Science or related field",
            "Proven experience in software testing",
            "Strong proficiency in automated and manual testing techniques",
            "Experience with testing frameworks such as Selenium",
            "Knowledge of continuous integration tools (e.g., Jenkins)",
            "Familiarity with Agile development methodologies",
            "Excellent problem-solving and analytical skills",
            "Ability to work in a collaborative team environment",
        ],
        "advantages": [
            "Competitive salary and benefits package",
            "Opportunity for professional growth and advancement",
            "Flexible work arrangements",
            "Collaborative and inclusive work culture",
            "Exciting projects with modern technologies",
        ],
    },
    {
        "title": "Frontend UI Developer",
        "description": "We are seeking a Frontend UI Developer to join our team and help create visually stunning and user-friendly web interfaces. You will work closely with our design and engineering teams to translate design concepts into interactive and responsive UI components.",
        "date": "02/25/2024",
        "location": "Seattle, WA",
        "duration": "Full-time",
        "skills": ["HTML", "CSS", "JavaScript", "React", "Sass", "Responsive Design"],
        "requirements": [
            "Bachelor's degree in Computer Science or related field",
            "Proven experience in frontend development",
            "Strong proficiency in HTML, CSS, and JavaScript",
            "Experience with React and frontend build tools",
            "Knowledge of CSS preprocessors such as Sass",
            "Understanding of responsive design principles",
            "Excellent problem-solving and debugging skills",
            "Ability to work in a collaborative team environment",
        ],
        "advantages": [
            "Competitive salary and benefits package",
            "Opportunity for career growth and advancement",
            "Flexible work arrangements",
            "Collaborative and supportive work culture",
            "Exciting projects with modern technologies",
        ],
    },
    {
        "title": "Embedded Software Engineer",
        "description": "Join our team as an Embedded Software Engineer and help develop firmware and software for embedded systems. You will work on a variety of projects, from IoT devices to industrial control systems, using a mix of programming languages and development tools.",
        "date": "02/25/2024",
        "location": "San Francisco, CA",
        "duration": "Full-time",
        "skills": ["C", "C++", "RTOS", "Embedded Linux", "ARM Cortex", "IoT"],
        "requirements": [
            "Bachelor's degree in Computer Engineering or related field",
            "Proven experience in embedded software development",
            "Strong proficiency in C and C++ programming languages",
            "Experience with real-time operating systems (RTOS)",
            "Knowledge of embedded Linux and device drivers",
            "Familiarity with ARM Cortex processors",
            "Understanding of IoT protocols and technologies",
            "Excellent problem-solving and debugging skills",
        ],
        "advantages": [
            "Competitive compensation and benefits package",
            "Opportunity for career advancement",
            "Collaborative and supportive work environment",
            "Exciting projects in emerging technologies",
            "Professional development and training opportunities",
        ],
    },
    {
        "title": "Electrical Engineer",
        "description": "We are seeking an Electrical Engineer to join our hardware development team. You will be responsible for designing and testing electronic circuits and systems for various applications. If you have a passion for electronics and a strong technical background, we want to hear from you.",
        "date": "02/25/2024",
        "location": "Los Angeles, CA",
        "duration": "Permanent",
        "skills": [
            "Analog Circuit Design",
            "Digital Circuit Design",
            "PCB Layout",
            "Signal Processing",
            "FPGA",
        ],
        "requirements": [
            "Bachelor's degree in Electrical Engineering or related field",
            "Proven experience in electrical engineering",
            "Strong proficiency in analog and digital circuit design",
            "Experience with PCB layout and schematic capture tools",
            "Knowledge of signal processing techniques",
            "Familiarity with FPGA programming",
            "Excellent problem-solving and analytical skills",
            "Ability to work in a collaborative team environment",
        ],
        "advantages": [
            "Competitive salary and benefits package",
            "Opportunity for professional growth and advancement",
            "Collaborative and supportive work environment",
            "Exciting projects with cutting-edge technologies",
            "Professional development and training opportunities",
        ],
    },
    {
        "title": "Automation Engineer",
        "description": "We are looking for an Automation Engineer to join our team and help automate manufacturing processes. You will be responsible for designing, implementing, and maintaining automated systems to improve efficiency and productivity.",
        "date": "02/25/2024",
        "location": "Austin, TX",
        "duration": "Full-time",
        "skills": [
            "PLC Programming",
            "SCADA",
            "Robotics",
            "Industrial Automation",
            "Python",
        ],
        "requirements": [
            "Bachelor's degree in Mechanical Engineering, Electrical Engineering, or related field",
            "Proven experience in automation engineering",
            "Strong proficiency in PLC programming and SCADA systems",
            "Experience with robotics and industrial automation",
            "Knowledge of programming languages such as Python",
            "Familiarity with electrical and mechanical systems",
            "Excellent problem-solving and analytical skills",
            "Ability to work in a collaborative team environment",
        ],
        "advantages": [
            "Competitive salary and benefits package",
            "Opportunity for career advancement",
            "Collaborative and supportive work environment",
            "Exciting projects in industrial automation",
            "Professional development and training opportunities",
        ],
    },
    {
        "title": "RF Engineer",
        "description": "We are seeking an RF Engineer to join our team and help design and optimize radio frequency systems. You will be responsible for conducting RF analysis, developing RF circuits, and testing RF components to ensure optimal performance.",
        "date": "02/25/2024",
        "location": "Seattle, WA",
        "duration": "Full-time",
        "skills": [
            "RF Design",
            "Antenna Design",
            "RF Testing",
            "RF Simulation",
            "Wireless Communication",
        ],
        "requirements": [
            "Bachelor's degree in Electrical Engineering or related field",
            "Proven experience in RF engineering",
            "Strong proficiency in RF design and testing",
            "Experience with antenna design and optimization",
            "Knowledge of RF simulation tools",
            "Understanding of wireless communication protocols",
            "Excellent problem-solving and analytical skills",
            "Ability to work in a collaborative team environment",
        ],
        "advantages": [
            "Competitive salary and benefits package",
            "Opportunity for professional growth and advancement",
            "Collaborative and supportive work environment",
            "Exciting projects in wireless technology",
            "Professional development and training opportunities",
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


def view_offer_details(request, slug):
    selected_offer = None
    for offer in fake_data_for_testing:
        title = offer["title"].lower().replace(" ", "-").replace("/", "")

        if title == slug:
            selected_offer = offer
            break

    if selected_offer is None:
        return HttpResponse("404 - Job offer not found")

    context = {"slug": slug, "offer": selected_offer}
    return render(request, "offer-details.html", context)


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
    return render(request, "condidat.html", context)

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
