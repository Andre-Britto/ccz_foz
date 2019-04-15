from django import forms

from apps.accounts.models import User


class SignUpForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)),
                                 label='Primeiro Nome')
    last_name = forms.CharField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label='Sobrenome')
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label='Email')
    password = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
                               label='Senha')
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)),
        label='Repita a senha')

    def clean_username(self):
        try:
            user = User.objects.get(email__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError("Esse usuário já existe")

    def clean(self):
        if 'password' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password'] != self.cleaned_data['password2']:
                raise forms.ValidationError("O campo repita a senha deve ser igual a senha")

        return self.cleaned_data
