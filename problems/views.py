from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView


from problems.models import Theme, Category, ThemeCategory, Type, Problem, ProblemCategory
from problems.forms import TaskForm, ThemeForm


class LogView(LoginView):
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True
    redirect_field_name = ''
    template_name = 'problems/login.html'


def start_view(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    return render(request, 'problems/main.html')

a = ThemeCategory.objects.values_list('id', flat=True).filter(id_theme=1)
print(a)
b = Problem.objects.filter(problemcategory__id_theme_cat__in=a)
print(b)

def problems_view(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.GET.get('theme', None):
        problems_list = Problem.objects.filter()
    else:
        problems_list = Problem.objects.all()
    paginator = Paginator(problems_list, 10)
    page_number = request.GET.get('page')
    if not page_number:
        page_number = 1
    page_obj = paginator.get_page(page_number)
    return render(request, 'problems/problems.html',
                  context={'problems': page_obj,
                           'paginator': paginator,
                           'pages_before': [i for i in range(int(page_number) - 3, int(page_number)) if i > 0],
                           'pages_after': [i for i in range(int(page_number)+1, int(page_number)+4) if i <= paginator.num_pages],
                           'ThemeForm': ThemeForm})


def task_view(request, id):
    if not request.user.is_authenticated:
        return redirect('/login')
    task = Problem.objects.get(id=id)
    return render(request, 'problems/task.html',
                  context={'task': task})


def task_edit_view(request, id):
    if not request.user.is_authenticated:
        return redirect('/login')
    task = get_object_or_404(Problem, id=id)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save(commit=False)
            task.save()
            return redirect('/task_'+str(id))
    else:
        form = TaskForm(instance=task)
    return render(request, 'problems/task_edit.html', {'form': form})


def new_task_view(request):
    if not request.user.is_authenticated:
        return redirect('/login')
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.id_google = 0
            task.save()
            return redirect('/task_'+str(task.id))
    else:
        form = TaskForm()
    return render(request, 'problems/task_edit.html', {'form': form})
