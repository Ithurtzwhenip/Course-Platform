from django.shortcuts import render
from emails.forms import EmailForm
from django.conf import settings

from src.courseplatform.settings import EMAIL_ADDRESS

EMAIL_ADDRESS = settings.EMAIL_ADDRESS


def home_view(request, *args, **kwargs):
    template_name = "home.html"
    form = EmailForm(request.POST or None)
    context = {
        "form": form,
        "message": ""
    }
    if form.is_valid():
        form.save()
        context['form'] = EmailForm()
        context["message"] = f"Success! Check your email for verification from {EMAIL_ADDRESS}"
    return render(request, template_name, context)
