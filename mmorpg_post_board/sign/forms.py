from django import forms
from .models import SignupOtc
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignupOtcForm(forms.ModelForm):
    class Meta:
        model = SignupOtc
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise ValidationError({
                "passwords": "Пароли не совпадают"
            })
        username = cleaned_data.get("username")
        users = User.objects.all().values_list('username', flat=True)
        users_otc = SignupOtc.objects.all().values_list('username', flat=True)
        if username in users or username in users_otc:
            raise ValidationError({
                "username": "такой username уже существует"
            })

        return cleaned_data


class OtcForm(forms.Form):
    ot_code = forms.IntegerField(label="Код потверждения")

