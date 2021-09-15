from django import forms
from problems.models import Problem, Theme


class TaskForm(forms.ModelForm):

    class Meta:
        model = Problem
        fields = ('task', 'solution', 'img_task', 'img_solution', 'id_orig', 'comment', )


class ThemeForm(forms.Form):
    theme = forms.ModelChoiceField(
        queryset=Theme.objects.all(),
        empty_label=None
    )