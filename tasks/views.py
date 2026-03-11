from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
from django.contrib.auth.models import User


def dashboard(request):
    tasks = Task.objects.all()
    return render(request, "tasks/dashboard.html", {"tasks": tasks})



def create_task(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]

        user = User.objects.first()

        Task.objects.create(
            title=title,
            description=description,
            user=user
        )

        return redirect("dashboard")

    return render(request, "tasks/create_task.html")


def update_task(request, pk):
    task = Task.objects.get(id=pk)

    if request.method == "POST":
        task.title = request.POST["title"]
        task.description = request.POST["description"]
        task.save()

        return redirect("dashboard")

    return render(request, "tasks/update_task.html", {"task": task})


def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    task.delete()

    return redirect("dashboard")


def complete_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    task.completed = not task.completed
    task.save()

    return redirect("dashboard")