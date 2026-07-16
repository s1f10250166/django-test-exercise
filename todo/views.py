from django.shortcuts import render, redirect
from django.http import Http404
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task

# Create your views here.


def index(request):
    if request.method == 'POST':
        task = Task(title=request.POST['title'],
                    description=request.POST.get('description', ''),
                    due_at=make_aware(parse_datetime(request.POST['due_at'])))
        task.save()
    # search query
    q = request.GET.get('q', '').strip()
    base = Task.objects.filter(completed=False)
    if q:
        base = base.filter(title__icontains=q)

    if request.GET.get('order') == 'due':
        tasks = base.order_by('due_at')
    else:
        tasks = base.order_by('-posted_at')

    context = {
        'tasks': tasks,
        'q': q,
    }
    return render(request, 'todo/index.html', context)


def completed_list(request):
    tasks = Task.objects.filter(completed=True).order_by('-posted_at')

    context = {
        'tasks': tasks
    }
    return render(request, 'todo/completed.html', context)


def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    context = {
        'task': task,
    }
    return render(request, 'todo/detail.html', context)
 

def update(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    if request.method == 'POST':
        task.title = request.POST['title']
        due_at_value = request.POST.get('due_at')
        task.due_at = make_aware(parse_datetime(due_at_value)) if due_at_value else None
        task.save()

    return redirect('detail', task_id=task_id)


def toggle_completed(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    if request.method == 'POST':
        task.completed = not task.completed
        task.save()

    return redirect(request.POST.get('next') or 'index')


def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.delete()
    return redirect(index)


def update(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    if request.method == 'POST':
        task.title = request.POST['title']
        task.description = request.POST.get('description', '')
        task.due_at = make_aware(parse_datetime(request.POST['due_at']))
        task.save()
        return redirect(detail, task_id)

    context = {
        'task': task
    }
    return render(request, "todo/edit.html", context)