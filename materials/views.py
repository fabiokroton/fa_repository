from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .forms import MaterialForm
from .models import Material


@login_required
def materials_home(request):
    materials = Material.objects.all().order_by("-uploaded_at")
    return render(request, "materials/materials_home.html", {"materials": materials})


@staff_member_required
def upload_material(request):
    if request.method == "POST":
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("materials_home")
    else:
        form = MaterialForm()

    return render(request, "materials/upload_material.html", {"form": form})


@staff_member_required
def delete_material(request, pk):
    material = get_object_or_404(Material, pk=pk)
    material.delete()
    messages.success(request, "Materiale eliminato correttamente.")
    return redirect("materials_home")
