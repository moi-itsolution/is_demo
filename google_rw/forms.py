from django import forms


def get_form(var):

    class UrlForm(forms.Form):
        url = forms.URLField(widget=forms.TextInput(attrs={'class': 'form-control'}))
        url.label = 'Введите ссылку на таблицу'
        if var == 'export':
            json_file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))
            json_file.label = 'Выберите .json файл'

        action = forms.CharField(initial=var)
        action.widget = forms.HiddenInput()

    return UrlForm


def get_choice_form(choices):
    class ChoiceForm(forms.Form):
        choice = forms.ChoiceField(choices=choices)
        choice.label = 'Выберите действие'

    return ChoiceForm
