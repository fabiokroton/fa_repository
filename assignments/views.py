from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import CreateView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from .models import Assignment, Submission
from .forms import SubmissionForm


# LISTA DEI COMPITI (necessaria per la navbar)
@login_required
def assignment_list(request):
    assignments = Assignment.objects.all().order_by("due_date")
    return render(request, "assignments/assignment_list.html", {
        "assignments": assignments
    })


# DETTAGLIO DEL COMPITO (vista STUDENTE)
@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)

    # Controllo se lo studente ha già consegnato
    submission = Submission.objects.filter(
        assignment=assignment,
        student=request.user
    ).first()

    # Se lo studente ha già consegnato → niente form
    if submission:
        form = None
    else:
        form = SubmissionForm(request.POST or None, request.FILES or None)

        if request.method == "POST" and form.is_valid():
            new_submission = form.save(commit=False)
            new_submission.assignment = assignment
            new_submission.student = request.user
            new_submission.save()
            return redirect("assignments:assignment_detail", pk=pk)

    return render(request, "assignments/assignment_detail.html", {
        "assignment": assignment,
        "submission": submission,
        "form": form,
    })


# CREAZIONE NUOVO COMPITO (solo staff)
class AssignmentCreateView(UserPassesTestMixin, CreateView):
    model = Assignment
    fields = ["title", "description", "due_date"]  # nessun campo file
    template_name = "assignments/assignment_form.html"
    success_url = reverse_lazy("assignments:assignment_list")

    def test_func(self):
        return self.request.user.is_staff


# MODELLO UTENTE
User = get_user_model()


# REGISTRARE CONSEGNA A MANO (solo staff)
@login_required
def mark_delivered_in_person(request, assignment_id, student_id):
    if not request.user.is_staff:
        return redirect("assignments:assignment_list")

    assignment = get_object_or_404(Assignment, id=assignment_id)
    student = get_object_or_404(User, id=student_id)

    # Evita duplicati
    existing = Submission.objects.filter(assignment=assignment, student=student).first()
    if not existing:
        Submission.objects.create(
            assignment=assignment,
            student=student,
            file=None  # consegna a mano → nessun file
        )

    return redirect("assignments:assignment_submissions", pk=assignment_id)


# PAGINA STAFF: elenco consegne per un compito
@user_passes_test(lambda u: u.is_staff)
def assignment_submissions(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)

    # Tutti gli studenti (non staff)
    students = User.objects.filter(is_staff=False).order_by("username")

    # Consegne effettuate
    submissions = Submission.objects.filter(assignment=assignment)

    submitted_students = [s.student for s in submissions]
    not_submitted_students = [s for s in students if s not in submitted_students]

    return render(request, "assignments/assignment_submissions.html", {
        "assignment": assignment,
        "submissions": submissions,
        "not_submitted": not_submitted_students,
    })
