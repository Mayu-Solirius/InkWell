from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterForm


def register(response):
    # Check if the request method is POST (form submission)
    if response.method == "POST":
        # Create a RegisterForm instance with the POST data
        form = RegisterForm(response.POST)
        # Check if the form data is valid
        if form.is_valid():
            # Save the form to create a new user account
            form.save()

            # Log in the user after successful registration
            # Get the username and password from the form's cleaned_data
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            # Authenticate the user with the provided username and password
            user = authenticate(username=username, password=password)
            # Check if the user is successfully authenticated
            if user:
                # Log in the user by creating a session for the response object
                login(response, user)

            # Redirect the user to the homepage after successful registration and login
            return redirect("/")
    else:
        # If the request method is not POST, create an empty RegisterForm instance
        form = RegisterForm()

    # Render the registration template with the form object
    return render(response, "register/register.html", {"form": form})
