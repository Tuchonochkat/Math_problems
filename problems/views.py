from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


from problems.models import Theme, Category, ThemeCategory, Problem, ProblemCategory, Trajectory, Syllabus, \
    Cart, CartTask
from problems.forms import TaskForm, FilterForm


class LogView(LoginView):
    authentication_form = AuthenticationForm
    redirect_authenticated_user = True
    redirect_field_name = ''
    template_name = 'problems/login.html'


@login_required(login_url='/login')
def start_view(request):
    cart = Cart.objects.get(user=request.user)
    items = Problem.objects.filter(carttask__id_cart=cart)
    return render(request, 'problems/main.html', context={'items': items})


# функция от реквеста, возвращает список задач в корзине юзера
def cart_items(request):
    cart = Cart.objects.get(user=request.user)
    items = Problem.objects.filter(carttask__id_cart=cart)
    return items


# процедура добавления товара в корзину
def into_cart(request):
    id_task = request.GET.get('into_cart', None)
    if id_task:
        cart = Cart.objects.get(user=request.user)
        task = Problem.objects.get(id=id_task)
        enum_task = len(CartTask.objects.filter(id_cart=cart))+1
        CartTask.objects.get_or_create(id_cart=cart, id_task=task, enum_task=enum_task)


def load_categories(request):
    theme = request.GET.get('theme')
    if theme:
        categories = Category.objects.filter(themecategory__id_theme=theme).order_by('name')
    else:
        categories = []
    selected = request.GET.get('category', None)
    return render(request, 'problems/categories_dropdown_list_options.html', {'categories': categories,
                                                                              'selected': selected})


@login_required(login_url='/login')
def problems_view(request):
    theme = request.GET.get('theme', None)
    category = request.GET.get('category', None)
    into_cart(request)
    if theme:
        if category:
            theme_cat = ThemeCategory.objects.values_list('id', flat=True).filter(id_theme=theme, id_category=category)
            form = FilterForm(qs=Category.objects.filter(themecategory__id_theme=theme).order_by('name'),
                              initial={'theme': Theme.objects.get(id=theme), 'category': Category.objects.get(id=category)})
        else:
            theme_cat = ThemeCategory.objects.values_list('id', flat=True).filter(id_theme=theme)
            form = FilterForm(qs=Category.objects.filter(themecategory__id_theme=theme).order_by('name'),
                              initial={'theme': Theme.objects.get(id=theme)})
    else:
        theme_cat = ThemeCategory.objects.values_list('id', flat=True).all()
        form = FilterForm
    problems_list = Problem.objects.filter(problemcategory__id_theme_cat__in=theme_cat).distinct('id').order_by('id')
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
                           'FilterForm': form,
                           'theme': theme,
                           'category': category,
                           'items': cart_items(request)})


@login_required(login_url='/login')
def task_view(request, id):
    task = Problem.objects.get(id=id)
    return render(request, 'problems/task.html',
                  context={'task': task,
                           'items': cart_items(request)})


@login_required(login_url='/login')
def task_edit_view(request, id):
    # начальное значение для полей задачи
    task = get_object_or_404(Problem, id=id)
    # задаем начальные значения тем и категорий
    theme_cat = ThemeCategory.objects.filter(problemcategory__id_task=task.id).values_list('id', 'id_theme',
                                                                                           'id_category')
    initial = {}
    for i, item in enumerate(theme_cat):
        initial['theme' + str(i + 1)] = Theme.objects.get(id=item[1])
        if item[2]:
            initial['category' + str(i + 1)] = Category.objects.get(id=item[2])

    if request.method == "POST":
        print('post')
        form = TaskForm(request.POST, instance=task, initial=initial)
        if form.is_valid():
            print('valid')
            task = form.save(commit=False)
            task.save()
            theme_cat_old = ThemeCategory.objects.filter(problemcategory__id_task=task)
            theme_cat_new = ThemeCategory.objects.none()
            for i in range(5):
                theme = form.cleaned_data.get('theme' + str(i+1), None)
                category = form.cleaned_data.get('category'+str(i+1), None)
                if theme:
                    theme_cat_new = theme_cat_new.union(ThemeCategory.objects.filter(id_theme=theme, id_category=category))
            category_to_remove = theme_cat_old.difference(theme_cat_new)
            category_to_add = theme_cat_new.difference(theme_cat_old)
            for cat in category_to_remove:
                ProblemCategory.objects.filter(id_task=task, id_theme_cat=cat).delete()
            for cat in category_to_add:
                ProblemCategory.objects.create(id_task=task, id_theme_cat=cat)
            return redirect('/task_'+str(id))
        print('errors:')
        for field in form:
            print(field.name, field.errors)
    else:
        form = TaskForm(instance=task,
                        initial=initial)
        print('not post')
    return render(request, 'problems/task_edit.html', {'form': form, 'id': id})


@login_required(login_url='/login')
def new_task_view(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.id_google = 0
            task.save()
            if not task.id_orig:
                task.id_orig = task.id
                task.save()
            for i in range(5):
                theme = form.cleaned_data.get('theme'+str(i+1), None)
                category = form.cleaned_data.get('category'+str(i+1), None)
                if theme:
                    theme_category = ThemeCategory.objects.get(id_theme=theme, id_category=category)
                    ProblemCategory.objects.get_or_create(id_task=task, id_theme_cat=theme_category)
            return redirect('/task_'+str(task.id))
    else:
        form = TaskForm()
    return render(request, 'problems/task_edit.html', {'form': form})


@login_required(login_url='/login')
def sets_view(request):
    return render(request, 'problems/trajectories.html',
                  context={'trajectories': Trajectory.objects.all(),
                           'items': cart_items(request)})


@login_required(login_url='/login')
def syllabus_view(request, id_syllabus):
    return render(request, 'problems/syllabus.html',
                  context={'syllabus': Syllabus.objects.get(id=id_syllabus),
                           'items': cart_items(request)})