from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Task




# ========================= Signup =========================
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        User.objects.create_user(username=username, email=email, password=password)
        return redirect('account_login')

    return render(request, 'signup.html')
# ========================= DASHBOARD =========================
def dashboard(request):

    tasks = Task.objects.all()

    completed = Task.objects.filter(completed=True).count()
    pending = Task.objects.filter(completed=False).count()

    context = {
        "tasks": tasks,
        "completed": completed,
        "pending": pending,
    }

    return render(request, "tasks/dashboard.html", context)


# ========================= TASK LIST =========================
def task_list(request):

    tasks = Task.objects.all()

    completed = Task.objects.filter(completed=True).count()
    pending = Task.objects.filter(completed=False).count()

    return render(request, "tasks/task_list.html", {
        "tasks": tasks,
        "completed": completed,
        "pending": pending
    })


# ========================= CREATE TASK =========================
def create_task(request):

    if request.method == "POST":

        title = request.POST["title"]
        description = request.POST["description"]
        due_date = request.POST.get("due_date")
        priority = request.POST.get("priority")

        user = User.objects.first()

        Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            user=user
        )

        return redirect("dashboard")

    return render(request, "tasks/create_task.html")

# ========================= UPDATE TASK =========================
def update_task(request, pk):

    task = get_object_or_404(Task, id=pk)

    if request.method == "POST":

        task.title = request.POST["title"]
        task.description = request.POST["description"]
        task.save()

        return redirect("dashboard")

    return render(request, "tasks/update_task.html", {"task": task})


# ========================= DELETE TASK =========================
def delete_task(request, pk):

    task = get_object_or_404(Task, id=pk)
    task.delete()

    return redirect("dashboard")


# ========================= TOGGLE COMPLETE =========================
def complete_task(request, pk):

    task = get_object_or_404(Task, id=pk)

    task.completed = not task.completed
    task.save()

    return redirect("dashboard")


# ========================= CALENDAR EVENTS =========================
def calendar_data(request):

    tasks = Task.objects.all()

    events = []

    for task in tasks:

        if task.due_date:
            events.append({
                "title": task.title,
                "start": task.due_date.strftime("%Y-%m-%d")
            })

    return JsonResponse(events, safe=False)


# ========================= TASK STATS FOR CHART =========================
def task_stats(request):

    completed = Task.objects.filter(completed=True).count()
    pending = Task.objects.filter(completed=False).count()

    return JsonResponse({
        "completed": completed,
        "pending": pending
    })


