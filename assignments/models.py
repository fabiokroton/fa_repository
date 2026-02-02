import uuid
from django.contrib.auth.decorators import login_required

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

def submission_upload_path(instance, filename):
    # I file andranno in: media/submissions/assignment_<id>/student_<id>/
    return f"submissions/assignment_{instance.assignment.id}/student_{instance.student.id}/{filename}"


class Assignment(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()

    def __str__(self):
        return self.title


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    file = models.FileField(upload_to=submission_upload_path)
    submitted_at = models.DateTimeField(auto_now_add=True)
    protocol_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.student} → {self.assignment}"


User = get_user_model()

@login_required
def mark_delivered_in_person(request, assignment_id, student_id):
    if not request.user.is_staff:
        return redirect("assignments:assignment_list")

    assignment = get_object_or_404(Assignment, id=assignment_id)
    student = get_object_or_404(User, id=student_id)

    # Evita duplicati: se esiste già una submission, non crearne un'altra
    existing = Submission.objects.filter(assignment=assignment, student=student).first()
    if not existing:
        Submission.objects.create(
            assignment=assignment,
            student=student,
            file=None,  # consegna a mano → nessun file
            created_at=timezone.now()
        )

    return redirect("assignments:assignment_detail", pk=assignment_id)
