from django import forms

from .models import Email,EmailVerificationEvent
from . import css
from .models import Email


class EmailForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'id': 'email-login-input',
                'class': css.EMAIL_FILED_CSS,
                "placeholder": "Email Address"
            }
        )
    )

    # class Meta:
    #     model = EmailVerificationEvent
    #     fields = ['email']
    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = Email.objects.filter(email=email, active=False)
        if qs.exists():
            raise forms.ValidationError('Invalid Email, please try again')
        return email
