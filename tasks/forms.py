from django import forms
from tasks.models import Tasks

# Regular Django Form
class TaskForm(forms.Form):
    title = forms.CharField(max_length=250, label="Task Title")
    description = forms.CharField( widget=forms.Textarea, label="Task Description")
    due_date = forms.DateField( widget=forms.SelectDateWidget(years=[2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]))
    assigned_to = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=[], label="Assigned to")

    def __init__(self, *args, **kwargs):
        employees = kwargs.pop("employees", [])
        super().__init__(*args, **kwargs)
        self.fields['assigned_to'].choices = [(emp.id, emp.name) for emp in employees]


# Django Model Form
class TaskModelForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['title', 'description', 'due_date', 'assigned_to']
        # exclude = ['project', 'is_completed', 'created_at', 'updated_at']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'border-2 border-gray-500 p-2 mb-2 w-full rounded-lg shadow-sm focus:border-rose-400',
                'placeholder': 'Enter task title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'border-2 border-gray-500 p-2 mb-2 w-full rounded-lg shadow-sm focus:border-rose-400',
                'placeholder': 'Describe the task'
            }),
            'due_date': forms.SelectDateWidget(attrs={
                'class': 'border-2 border-gray-500 p-2 mb-2 rounded-lg shadow-sm focus:border-rose-400',
                'placeholder': 'Describe the task'
            }),
            'assigned_to': forms.CheckboxSelectMultiple(attrs={
                'class': 'mb-2'
            })
        }