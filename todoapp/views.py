
# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.http import JsonResponse
from .models import Task, Category, UserProfile
from .forms import TaskForm, CustomUserCreationForm, UserProfileForm
from django.utils import timezone
from django.db.models import Q
import json
from django.db.models import Count
from django.utils.timezone import now, timedelta
from .models import Task

@login_required
def overdue_tasks(request):
    now = timezone.now()
    tasks = Task.objects.filter(user=request.user, status='pending', due_date__lt=now).order_by('due_date')
    query = request.GET.get('q')
    if query:
        tasks = tasks.filter(title__icontains=query)
    return render(request, 'todoapp/overdue_tasks.html', {'tasks': tasks, 'query': query})

@login_required
def dashboard(request):
    # Last 7 days labels
    today = now().date()
    last_7_days = [(today - timedelta(days=i)).strftime("%b %d") for i in reversed(range(7))]

    # Completed tasks per day
    completed_per_day = []
    for i in reversed(range(7)):
        day = today - timedelta(days=i)
        count = Task.objects.filter(status='completed', completed_at__date=day).count()
        completed_per_day.append(count)

    # Pending vs completed
    pending_count = Task.objects.filter(status='pending').count()
    completed_count = Task.objects.filter(status='completed').count()

    # Priority counts
    priority_counts = Task.objects.values('priority_level').annotate(count=Count('id'))
    priority_dict = {'High': 0, 'Medium': 0, 'Low': 0}
    for p in priority_counts:
        if p['priority_level'] == 'H':
            priority_dict['High'] = p['count']
        elif p['priority_level'] == 'M':
            priority_dict['Medium'] = p['count']
        elif p['priority_level'] == 'L':
            priority_dict['Low'] = p['count']

    context = {
        'last_7_days': last_7_days,
        'completed_per_day': completed_per_day,
        'pending_count': pending_count,
        'completed_count': completed_count,
        'priority_counts': priority_dict
    }
    return render(request, 'todoapp/dashboard.html', context)


@login_required
def task_list(request):
    query = request.GET.get('q', '')
    tasks = Task.objects.filter(user=request.user, status='pending').order_by('priority', '-created')    
    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(categories__name__icontains=query)
        ).distinct()
    
    context = {
        'tasks': tasks,
        'query': query,
    }
    return render(request, 'todoapp/task_list.html', context)

@login_required
def completed_tasks(request):
    query = request.GET.get('q', '')
    tasks = Task.objects.filter(user=request.user, status='completed').order_by('-completed_at')
    
    if query:
        tasks = tasks.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(categories__name__icontains=query)
        ).distinct()
    
    context = {
        'tasks': tasks,
        'query': query,
    }
    return render(request, 'todoapp/completed_tasks.html', context)


from .models import ActivityLog

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import TaskForm
from .models import ActivityLog

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.status = 'pending'  # Default status on creation
            # priority_level is saved by form automatically
            task.save()
            form.save_m2m()  # Save many-to-many relationships like categories

            # Log activity
            ActivityLog.objects.create(
                user=request.user,
                task=task,
                action='created',
                description=f"Task '{task.title}' was created."
            )
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'todoapp/task_form.html', {
        'form': form,
        'title': 'Create Task'
    })


@login_required
def update_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    old_status = task.status
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            updated_task = form.save()
            
            # Determine action type
            if old_status != updated_task.status:
                if updated_task.status == 'completed':
                    action = 'completed'
                    desc = f"Task '{updated_task.title}' marked as completed."
                else:
                    action = 'updated'
                    desc = f"Task '{updated_task.title}' status changed to {updated_task.status}."
            else:
                action = 'updated'
                desc = f"Task '{updated_task.title}' was updated."
            
            ActivityLog.objects.create(
                user=request.user,
                task=updated_task,
                action=action,
                description=desc
            )
            
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'todoapp/task_form.html', {'form': form, 'title': 'Update Task'})

@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    if request.method == 'POST':
        ActivityLog.objects.create(
            user=request.user,
            task=task,
            action='deleted',
            description=f"Task '{task.title}' was deleted."
        )
        task.delete()
        return redirect('task_list')
    return render(request, 'todoapp/confirm_delete.html', {'task': task})


def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
        # form errors will be passed back to template automatically
    else:
        form = CustomUserCreationForm()
    return render(request, 'todoapp/register.html', {'form': form, 'errors': form.errors if request.method == 'POST' else None})

def login_view(request):
    if request.method == 'POST':
        # Implement authentication logic
        # For simplicity, using Django's built-in auth
        from django.contrib.auth import authenticate, login
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('task_list')
        else:
            return render(request, 'todoapp/login.html', {'error': 'Invalid credentials'})
    return render(request, 'todoapp/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def profile_view(request):
    return render(request, 'todoapp/profile_view.html')

@login_required
def profile_edit(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_view')  # or wherever you want to redirect
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'todoapp/profile_edit.html', {'form': form})



@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'todoapp/category_list.html', {'categories': categories})

@login_required
def create_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            Category.objects.create(name=name)
            return redirect('category_list')
    return render(request, 'todoapp/category_form.html')


@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'todoapp/confirm_delete_category.html', {'category': category})


@login_required
def edit_category(request, pk):
    category = get_object_or_404(Category, id=pk)
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            category.name = name
            category.save()
            return redirect('category_list')
    return render(request, 'todoapp/category_form.html', {'category': category})



@login_required
def activity_log(request):
    query = request.GET.get('q', '').strip()

    logs = ActivityLog.objects.filter(user=request.user).select_related('task')

    if query:
        logs = logs.filter(
            Q(action__icontains=query) |
            Q(description__icontains=query) |
            Q(task__title__icontains=query)
        )

    logs = logs.order_by('-timestamp')

    return render(request, 'todoapp/activity_log.html', {
        'logs': logs,
        'query': query
    })



@login_required
def update_priority(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for task_data in data:
                task = Task.objects.get(id=task_data['id'], user=request.user)
                task.priority = task_data['priority']
                task.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'error'}, status=400)



from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone

@login_required
def complete_task(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk, user=request.user)
        task.status = 'completed'
        task.completed_at = timezone.now()  # Optional, if you track completed time
        task.save()
    return redirect('task_list')


# views.py
@login_required
def mark_task_pending(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(Task, pk=pk, user=request.user)
        if task.status == 'completed':
            task.status = 'pending'
            task.completed_at = None
            task.save()
    return redirect(request.META.get('HTTP_REFERER', 'task_list'))


