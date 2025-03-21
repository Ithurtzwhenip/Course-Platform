from django.shortcuts import render
from emails.forms import EmailForm
from django.conf import settings
from emails.models import Email, EmailVerificationEvent
from emails import services as email_services

EMAIL_ADDRESS = settings.EMAIL_ADDRESS


def login_logout_template_view(request):
    return render(request, 'auth/login-logout.html',{})


def home_view(request, *args, **kwargs):
    template_name = "home.html"
    form = EmailForm(request.POST or None)
    context = {
        "form": form,
        "message": ""
    }
    if form.is_valid():
        email_val = form.cleaned_data.get('email')
        obj = email_services.start_verification_event(email_val)
        print(obj)
        context['form'] = EmailForm()
        context["message"] = f"Success! Check your email for verification from {EMAIL_ADDRESS}"
    else:
        print("Form errors:", form.errors)
    print('email_id', request.session.get('email_id'))
    return render(request, template_name, context)
