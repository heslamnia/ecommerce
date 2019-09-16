from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import ContactForm, LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, get_user_model


def home_page(request):
    context = {
        "title" : "this is my home",
        "content" : "this is the home page"
    }

    if request.user.is_authenticated():
        context["premium_content"] = "yeahhhhhhh"
        print(context)
    return render(request, 'home_page.html', context)


def about_page(request):
    context = {
        "title" : "about us",
        "content" : "this is the about us"
    }
    return render(request, 'home_page.html', context)


def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    # if request.method == "POST":
        # print(request.POST)
        # print(request.POST.get("fullname"))
        # print(request.POST.get("email"))
        # print(request.POST.get("content"))

    context = {
        "title" :   "this contact",
        "content" : "this is the contact",
        "form"      : contact_form
    }
    # is_valid check if all data are filled and are correct for example
    # if an email doesn't have a @ it won't be valid
    if contact_form.is_valid():
        # cleaned_data is a dictionary which contains form information.
        # it is part of Form class and every class which is inherited from that
        print(contact_form.cleaned_data)
    return render(request, 'contact/view.html', context)


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {"form":form}
    # print("user loged in is:")
    # print(request.user.is_authenticated())

    if form.is_valid():
        # print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            # print(request.user.is_authenticated())
            return redirect("/")
        else:
            print("user is none")

    return render(request, 'auth/login.html', context)


User = get_user_model()


def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {"form":form}
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        email = form.cleaned_data.get("email")
        new_user = User.objects.create_user(username, email, password)

    return render(request, 'auth/register.html', context)
