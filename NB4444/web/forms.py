# from ckeditor.fields import RichTextFormField
from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator

from B4 import models


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль ")

    class Meta:
        model = models.User
        fields = ('username', 'password')


def get_custom_model_form(model_name, fields_list="__all__", exclude_fields=None):
    class CustomModelForm(forms.ModelForm):
        class Meta:
            model = model_name
            if exclude_fields:
                exclude = exclude_fields
            else:
                fields = fields_list
    return CustomModelForm


class TaskModelForm(forms.ModelForm):
    # description = RichTextFormField(label="")

    class Meta:
        model = models.Task
        fields = ("plan", "section", "description", "is_ready", "priority")
        widgets = {
            "plan": forms.HiddenInput
        }


class DefaultDeductionModelForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=models.User.objects.all(),
        widget=forms.HiddenInput
    )

    class Meta:
        model = models.DefaultDeductions
        fields = ("house", "travel", "phone", "food", "user")


class UserModelForm(forms.ModelForm):
    username = forms.CharField(label="Логин", required=True, min_length=3, validators=[UnicodeUsernameValidator()])
    first_name = forms.CharField(label="Имя", required=True, min_length=3)
    last_name = forms.CharField(label="Фамилия", required=True, min_length=3)
    email = forms.EmailField(label="Адрес электронной почты", required=True)

    class Meta:
        model = models.User
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        widgets = {
            'password': forms.PasswordInput()
        }

    def save(self, commit=True):
        obj = super().save(commit)
        obj.set_password(obj.password)
        obj.save()
        return obj


class NoteModelForm(forms.ModelForm):
    # text = RichTextFormField(label="", required=False)

    class Meta:
        model = models.Note
        fields = ["text", "image", "user"]
        widgets = {
            "user": forms.HiddenInput()
        }

    def clean(self):
        cd = self.cleaned_data
        image = cd.get("image")
        text = cd.get("text")
        if not image and not text:
            self.add_error("text", "Поле текст не может быть пустым! Заполните его либо выберите файл для загрузки.")
        return cd

