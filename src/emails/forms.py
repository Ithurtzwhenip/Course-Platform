from django import forms

from .models import Email,EmailVerificationEvent
from . import css


class EmailForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'id': 'email-login-input',
                'class': css.EMAIL_FILED_CSS,
                "placeholder": "Email Address"
            }
        )
    )

    class Meta:
        model = EmailVerificationEvent
        fields = ['email']
