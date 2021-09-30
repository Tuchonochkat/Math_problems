from django import forms
from problems.models import Problem, Theme, Category, ThemeCategory


class TaskForm(forms.ModelForm):
    theme1 = forms.ModelChoiceField(
        label='Тема 1',
        queryset=ThemeCategory.objects.all().order_by('id_theme'),
        empty_label='Тема не выбрана',
        required=False
    )
    theme2 = forms.ModelChoiceField(
        label='Тема 2',
        queryset=ThemeCategory.objects.all().order_by('id_theme'),
        empty_label='Тема не выбрана',
        required=False
    )
    theme3 = forms.ModelChoiceField(
        label='Тема 3',
        queryset=ThemeCategory.objects.all().order_by('id_theme'),
        empty_label='Тема не выбрана',
        required=False
    )
    theme4 = forms.ModelChoiceField(
        label='Тема 4',
        queryset=ThemeCategory.objects.all().order_by('id_theme'),
        empty_label='Тема не выбрана',
        required=False
    )
    theme5 = forms.ModelChoiceField(
        label='Тема 5',
        queryset=ThemeCategory.objects.all().order_by('id_theme'),
        empty_label='Тема не выбрана',
        required=False
    )

    class Meta:
        model = Problem
        exclude = ['id_google']
        label = {
            'id_type': 'Тип задачи',
            'task': 'Условие',
            'solution': 'Решение',
            'comment': 'Комментарий к задаче',
            'img_task': 'Рисунок к условию',
            'img_solution': 'Рисунок к решению',
            'id_orig': 'Оригинал задачи',
            'date_using': 'Задачу нельзя использовать в подборках до даты',
        }


class FilterForm(forms.Form):
    theme = forms.ModelChoiceField(
        label='Тема',
        queryset=Theme.objects.all().order_by('name'),
        empty_label='Тема не выбрана',
    )
    category = forms.ModelChoiceField(
        label='Категория',
        queryset=Category.objects.none(),
        empty_label='Категория не выбрана'
    )

    def __init__(self, *args, **kwargs):
        qs = kwargs.pop('qs', None)
        super(FilterForm, self).__init__(*args, **kwargs)
        if qs:
            self.fields['category'].queryset = qs
