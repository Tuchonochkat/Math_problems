from django import forms
from problems.models import Problem, Theme, Category


class TaskForm(forms.ModelForm):

    class Meta:
        model = Problem
        fields = ('task', 'solution', 'img_task', 'img_solution', 'id_orig', 'comment', )


class ThemeForm(forms.Form):
    theme = forms.ModelChoiceField(
        queryset=Theme.objects.all().order_by('name'),
        empty_label=None
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        empty_label=None
    )

    def __init__(self, *args, **kwargs):
        qs = kwargs.pop('qs', None)
        super(ThemeForm, self).__init__(*args, **kwargs)
        if qs:
            self.fields['category'].queryset = qs
