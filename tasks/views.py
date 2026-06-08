from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        User.objects.create_user(username=username, email=email, password=password)
        return redirect('account_login')
    return render(request, 'signup.html')


@login_required
def dashboard(request):
    tasks = Task.objects.filter(user=request.user)

    # Filtering
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    search_query = request.GET.get('q', '')

    if status_filter == 'completed':
        tasks = tasks.filter(completed=True)
    elif status_filter == 'pending':
        tasks = tasks.filter(completed=False)

    if priority_filter in ('low', 'medium', 'high'):
        tasks = tasks.filter(priority=priority_filter)

    if search_query:
        tasks = tasks.filter(title__icontains=search_query)

    tasks = tasks.order_by('-created_at')

    completed = Task.objects.filter(user=request.user, completed=True).count()
    pending = Task.objects.filter(user=request.user, completed=False).count()

    return render(request, "tasks/dashboard.html", {
        "tasks": tasks,
        "completed": completed,
        "pending": pending,
        "status_filter": status_filter,
        "priority_filter": priority_filter,
        "search_query": search_query,
    })


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    completed = tasks.filter(completed=True).count()
    pending = tasks.filter(completed=False).count()
    return render(request, "tasks/task_list.html", {
        "tasks": tasks,
        "completed": completed,
        "pending": pending
    })


@login_required
def create_task(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST.get("description", "")
        due_date = request.POST.get("due_date") or None
        priority = request.POST.get("priority", "low")
        user = request.user
        Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            user=user
        )
        messages.success(request, f'Task "{title}" created successfully!')
        return redirect("dashboard")
    return render(request, "tasks/create_task.html")


@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    if request.method == "POST":
        task.title = request.POST["title"]
        task.description = request.POST.get("description", "")
        task.due_date = request.POST.get("due_date") or None
        task.priority = request.POST.get("priority", task.priority)
        task.save()
        messages.success(request, f'Task "{task.title}" updated successfully!')
        return redirect("dashboard")
    return render(request, "tasks/update_task.html", {"task": task})


@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    if request.method == "POST":
        title = task.title
        task.delete()
        messages.success(request, f'Task "{title}" deleted successfully!')
        return redirect("dashboard")
    # GET requests redirect to dashboard (safety)
    return redirect("dashboard")


@login_required
def complete_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    status = "completed" if task.completed else "reopened"
    messages.success(request, f'Task "{task.title}" {status}!')
    return redirect("dashboard")


@login_required
def calendar_data(request):
    tasks = Task.objects.filter(user=request.user)
    events = []
    for task in tasks:
        if task.due_date:
            events.append({
                "title": task.title,
                "start": task.due_date.strftime("%Y-%m-%d"),
                "color": "#f43f5e" if task.priority == "high" else "#f59e0b" if task.priority == "medium" else "#10b981",
            })
    return JsonResponse(events, safe=False)


@login_required
def task_stats(request):
    completed = Task.objects.filter(user=request.user, completed=True).count()
    pending = Task.objects.filter(user=request.user, completed=False).count()
    return JsonResponse({
        "completed": completed,
        "pending": pending
    })