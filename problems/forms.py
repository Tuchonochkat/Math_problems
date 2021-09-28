from django import forms
from problems.models import Problem, Theme, Category


class TaskForm(forms.ModelForm):
    theme1 = forms.ModelChoiceField(
        label='Тема 1',
        queryset=Theme.objects.all().order_by('name'),
        empty_label='Тема не выбрана',
        required=False
    )
    category1 = forms.ModelChoiceField(
        label='Категория 1',
        queryset=Category.objects,
        empty_label='Категория не выбрана',
        required=False
    )
    theme2 = forms.ModelChoiceField(
        label='Тема 2',
        queryset=Theme.objects.all().order_by('name'),
        empty_label='Тема не выбрана',
        required=False
    )
    category2 = forms.ModelChoiceField(
        label='Категория 2',
        queryset=Category.objects,
        empty_label='Категория не выбрана',
        required=False
    )
    theme3 = forms.ModelChoiceField(
        label='Тема 3',
        queryset=Theme.objects.all().order_by('name'),
        empty_label='Тема не выбрана',
        required=False
    )
    category3 = forms.ModelChoiceField(
        label='Категория 3',
        queryset=Category.objects,
        empty_label='Категория не выбрана',
        required=False
    )
    theme4 = forms.ModelChoiceField(
        label='Тема 4',
        queryset=Theme.objects.all().order_by('name'),
        empty_label='Тема не выбрана',
        required=False
    )
    category4 = forms.ModelChoiceField(
        label='Категория 4',
        queryset=Category.objects,
        empty_label='Категория не выбрана',
        required=False
    )
    theme5 = forms.ModelChoiceField(
        label='Тема 5',
        queryset=Theme.objects.all().order_by('name'),
        empty_label='Тема не выбрана',
        required=False
    )
    category5 = forms.ModelChoiceField(
        label='Категория 5',
        queryset=Category.objects,
        empty_label='Категория не выбрана',
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for i in range(5):
            theme = self['theme'+str(i+1)].initial
            if theme:
                self.fields['category' + str(i + 1)].queryset = Category.objects.filter(
                    themecategory__id_theme=theme).order_by('name')

    def clean_category2(self):
        return self.cleaned_data['category2']

    def clean(self):
        cleaned_data = super().clean()
        for i in range(5):
            theme = cleaned_data.get('theme'+str(i+1))
            category = cleaned_data.get('category' + str(i+1))
            if theme and category not in Category.objects.filter(themecategory__id_theme=theme):
                self.add_error('category' + str(i+1), 'Категория не относится к данной теме')

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
