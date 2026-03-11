from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth.decorators import login_required


def dashboard(request):
    tasks = Task.objects.all()
    return render(request, "tasks/dashboard.html", {"tasks": tasks})


@login_required
def create_task(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]

        Task.objects.create(
            title=title,
            description=description,
            user=request.user
        )

        return redirect("dashboard")

    return render(request, "tasks/create_task.html")


@login_required
def update_task(request, pk):
    task = Task.objects.get(id=pk)

    if request.method == "POST":
        task.title = request.POST["title"]
        task.description = request.POST["description"]
        task.save()

        return redirect("dashboard")

    return render(request, "tasks/update_task.html", {"task": task})


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.delete()

    return redirect("dashboard")


@login_required
def complete_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.completed = not task.completed
    task.save()

    return redirect("dashboard")