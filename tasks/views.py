from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Task, Project, Subtask
import json


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

    projects = Project.objects.filter(user=request.user)

    return render(request, "tasks/dashboard.html", {
        "tasks": tasks,
        "projects": projects,
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
        project_id = request.POST.get("project")
        project = Project.objects.get(id=project_id, user=user) if project_id else None
        
        Task.objects.create(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            user=user,
            project=project
        )
        messages.success(request, f'Task "{title}" created successfully!')
        return redirect("dashboard")
    
    projects = Project.objects.filter(user=request.user)
    return render(request, "tasks/create_task.html", {"projects": projects})


@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    if request.method == "POST":
        task.title = request.POST["title"]
        task.description = request.POST.get("description", "")
        task.due_date = request.POST.get("due_date") or None
        task.priority = request.POST.get("priority", task.priority)
        project_id = request.POST.get("project")
        task.project = Project.objects.get(id=project_id, user=request.user) if project_id else None
        
        task.save()
        messages.success(request, f'Task "{task.title}" updated successfully!')
        return redirect("dashboard")
    
    projects = Project.objects.filter(user=request.user)
    return render(request, "tasks/update_task.html", {"task": task, "projects": projects})


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


# ==========================================
# PROJECTS CRUD
# ==========================================

@login_required
def project_list(request):
    projects = Project.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tasks/project_list.html', {'projects': projects})

@login_required
def create_project(request):
    if request.method == "POST":
        name = request.POST["name"]
        description = request.POST.get("description", "")
        Project.objects.create(name=name, description=description, user=request.user)
        messages.success(request, f'Project "{name}" created successfully!')
        return redirect('project_list')
    return render(request, 'tasks/create_project.html')

@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, id=pk, user=request.user)
    tasks = Task.objects.filter(project=project)
    
    # Quick filtering
    status_filter = request.GET.get('status', '')
    if status_filter == 'completed':
        tasks = tasks.filter(completed=True)
    elif status_filter == 'pending':
        tasks = tasks.filter(completed=False)
        
    completed = tasks.filter(completed=True).count()
    pending = tasks.filter(completed=False).count()
    
    return render(request, "tasks/dashboard.html", {
        "tasks": tasks,
        "current_project": project,
        "completed": completed,
        "pending": pending,
        "status_filter": status_filter,
    })

@login_required
def update_project(request, pk):
    project = get_object_or_404(Project, id=pk, user=request.user)
    if request.method == "POST":
        project.name = request.POST["name"]
        project.description = request.POST.get("description", "")
        project.save()
        messages.success(request, f'Project "{project.name}" updated successfully!')
        return redirect('project_list')
    return render(request, 'tasks/update_project.html', {'project': project})

@login_required
def delete_project(request, pk):
    project = get_object_or_404(Project, id=pk, user=request.user)
    if request.method == "POST":
        name = project.name
        project.delete()
        messages.success(request, f'Project "{name}" deleted successfully!')
        return redirect('project_list')
    return redirect('project_list')


# ==========================================
# SUBTASKS API
# ==========================================

@login_required
def create_subtask(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            task_id = data.get('task_id')
            title = data.get('title')
            
            task = get_object_or_404(Task, id=task_id, user=request.user)
            subtask = Subtask.objects.create(title=title, task=task)
            
            return JsonResponse({
                'status': 'success',
                'subtask': {
                    'id': subtask.id,
                    'title': subtask.title,
                    'completed': subtask.completed
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required
def toggle_subtask(request, pk):
    if request.method == "POST":
        subtask = get_object_or_404(Subtask, id=pk, task__user=request.user)
        subtask.completed = not subtask.completed
        subtask.save()
        return JsonResponse({'status': 'success', 'completed': subtask.completed})
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def delete_subtask(request, pk):
    if request.method == "POST":
        subtask = get_object_or_404(Subtask, id=pk, task__user=request.user)
        subtask.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)