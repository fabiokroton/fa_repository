from django.urls import path
from . import views
from .views import AssignmentCreateView

app_name = "assignments"

urlpatterns = [
    # LISTA COMPITI
    path("", views.assignment_list, name="assignment_list"),

    # DETTAGLIO COMPITO (vista studente)
    path("<int:pk>/", views.assignment_detail, name="assignment_detail"),

    # PAGINA STAFF: elenco consegne per un compito
    path("<int:pk>/submissions/", views.assignment_submissions, name="assignment_submissions"),

    # SEGNARE CONSEGNA A MANO (solo staff)
    path(
        "<int:assignment_id>/deliver/<int:student_id>/",
        views.mark_delivered_in_person,
        name="deliver_in_person"
    ),

    # CREAZIONE NUOVO COMPITO (solo staff)
    path("create/", AssignmentCreateView.as_view(), name="create_assignment"),
]

