from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect

from .models import SiteSettings

def home(request):
    settings_obj = SiteSettings.load()
    return render(request, 'core/home.html', {
        "site_settings": settings_obj
    })



@login_required
def private_area(request):
    from assignments.models import Assignment, Submission

    assignments = Assignment.objects.all().order_by("due_date")

    # Mappa: assignment.id → submission dello studente (o None)
    submissions = {
        a.id: Submission.objects.filter(assignment=a, student=request.user).first()
        for a in assignments
    }

    return render(request, "core/private_area.html", {
        "assignments": assignments,
        "submissions": submissions,
    })



@staff_member_required
def staff_dashboard(request):
    from assignments.models import Assignment, Submission
    from materials.models import Material
    from accounts.models import User

    settings_obj = SiteSettings.load()

    # Statistiche
    total_students = User.objects.filter(is_staff=False).count()
    total_assignments = Assignment.objects.count()
    total_submissions = Submission.objects.count()

    # Ultimi 5 materiali
    latest_materials = Material.objects.order_by("-id")[:5]

    # Ultimi 5 compiti
    latest_assignments = Assignment.objects.order_by("-id")[:5]

    # Per ogni compito: chi ha consegnato e chi no
    assignment_status = []
    for assignment in latest_assignments:
        submitted = Submission.objects.filter(assignment=assignment)
        submitted_students = [s.student for s in submitted]
        not_submitted_students = User.objects.filter(is_staff=False).exclude(id__in=[s.id for s in submitted_students])

        assignment_status.append({
            "assignment": assignment,
            "submitted": submitted_students,
            "not_submitted": not_submitted_students,
        })

    return render(request, "core/staff_dashboard.html", {
        "site_settings": settings_obj,
        "total_students": total_students,
        "total_assignments": total_assignments,
        "total_submissions": total_submissions,
        "latest_materials": latest_materials,
        "latest_assignments": latest_assignments,
        "assignment_status": assignment_status,
    })

@staff_member_required
def toggle_registration(request):
    settings_obj = SiteSettings.load()
    settings_obj.registration_open = not settings_obj.registration_open
    settings_obj.save()
    return redirect("home")


@login_required
def student_dashboard(request):
    from assignments.models import Assignment, Submission

    assignments = Assignment.objects.all().order_by("due_date")

    submissions = {
        a.id: Submission.objects.filter(assignment=a, student=request.user).first()
        for a in assignments
    }

    return render(request, "core/student_dashboard.html", {
        "assignments": assignments,
        "submissions": submissions,
    })
