from django.shortcuts import render
from .models import Profile


import pdfkit
from django.http import HttpResponse
from django.template import loader
import io

import os, sys, subprocess, platform


# Create your views here.
def index(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        summary = request.POST.get("summary")
        degree = request.POST.get("degree")
        school = request.POST.get("school")
        university = request.POST.get("university")
        previous_work = request.POST.get("previous_work")
        skills= request.POST.get("skills")

        profile = Profile(name=name, email=email, phone=phone, summary=summary, degree=degree, school=school, university=university,  previous_work=previous_work, skills=skills)
        profile.save()
    return render(request, "pdf/index.html")


def list(request):
    user_profiles = Profile.objects.all()
    context = {
        'user_profiles':user_profiles,
    }
    return render(request, "pdf/list.html", context)

def resume(request, id):
    user_profile = Profile.objects.get(pk=id)
    template = loader.get_template("pdf/resume.html")
    html = template.render({'user_profile':user_profile})
    options = {
        'page-size' : 'Letter',
        'encoding' : "UTF-8",
    }



    if platform.system() == "Windows":
        config = pdfkit.configuration(wkhtmltopdf=os.environ.get('WKHTMLTOPDF_BINARY', 'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe'))
    else:
        os.environ['PATH'] += os.pathsep + os.path.dirname(sys.executable) 
        WKHTMLTOPDF_CMD = subprocess.Popen(['which', os.environ.get('WKHTMLTOPDF_BINARY', 'wkhtmltopdf')], 
            stdout=subprocess.PIPE).communicate()[0].strip()
        config = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_CMD)



    pdf = pdfkit.from_string(html, False, configuration=config, options=options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    return response
