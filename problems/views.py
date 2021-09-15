from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required


from problems.models import Theme, Category, ThemeCategory, Type, Problem, ProblemCategory
from problems.forms import TaskForm, ThemeForm


class LogView(LoginView):
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True
    redirect_field_name = ''
    template_name = 'problems/login.html'


@login_required(login_url='/login')
def start_view(request):
    return render(request, 'problems/main.html')


def load_categories(request):
    theme = request.GET.get('theme')
    categories = Category.objects.filter(themecategory__id_theme=theme).order_by('name')
    selected = request.GET.get('category', None)
    return render(request, 'problems/categories_dropdown_list_options.html', {'categories': categories,
                                                                              'selected': selected})


@login_required(login_url='/login')
def problems_view(request):
    theme = request.GET.get('theme', None)
    category = request.GET.get('category', None)
    if theme:
        if category:
            theme_cat = ThemeCategory.objects.values_list('id', flat=True).filter(id_theme=theme, id_category=category)
            form = ThemeForm(qs=Category.objects.filter(themecategory__id_theme=theme).order_by('name'),
                             initial={'theme': Theme.objects.get(id=theme), 'category': Category.objects.get(id=category)})
        else:
            theme_cat = ThemeCategory.objects.values_list('id', flat=True).filter(id_theme=theme)
            form = ThemeForm(qs=Category.objects.filter(themecategory__id_theme=theme).order_by('name'),
                             initial={'theme': Theme.objects.get(id=theme)})
    else:
        theme_cat = ThemeCategory.objects.values_list('id', flat=True).all()
        form = ThemeForm
    problems_list = Problem.objects.filter(problemcategory__id_theme_cat__in=theme_cat)
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
                           'ThemeForm': form,
                           'theme': theme,
                           'category': category})


@login_required(login_url='/login')
def task_view(request, id):
    task = Problem.objects.get(id=id)
    return render(request, 'problems/task.html',
                  context={'task': task})


@login_required(login_url='/login')
def task_edit_view(request, id):
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


@login_required(login_url='/login')
def new_task_view(request):
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
