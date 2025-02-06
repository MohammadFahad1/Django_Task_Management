from django import forms


class TaskForm(forms.Form):
    title = forms.CharField(max_length=250, label="Task Title")
    description = forms.CharField( widget=forms.Textarea, label="Task Description")
    due_date = forms.DateField( widget=forms.SelectDateWidget(years=[2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]))
