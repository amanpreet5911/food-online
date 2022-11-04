from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import *
from .models import *
from django.contrib import messages

# Create your views here.


def registeruser(request):
    form = UserForms()
    if request.method == "POST":
        form = UserForms(request.POST)
        if form.is_valid():
            # user=form.save(commit=False)
            # user.role=User.CUSTOMER
            # user.save()
            first_name = form.cleaned_data["first_name"]
            last_name = form.cleaned_data["last_name"]
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password,
            )
            user.role = User.CUSTOMER
            user.save()
            messages.success(request,"Your form has been submitted successfully")
            return redirect("register")
     
        else:
            print(form.errors)
            context = {"forms": form}
            return render(request, "accounts/register.html", context)

    else:
        context = {"forms": form}

        return render(request, "accounts/register.html", context)
