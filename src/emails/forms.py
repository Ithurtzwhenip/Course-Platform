from django import forms
from . import css, services


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
        verified = services.verify_email(email)
        if verified:
            raise forms.ValidationError('Invalid Email, please try again')
        return email
