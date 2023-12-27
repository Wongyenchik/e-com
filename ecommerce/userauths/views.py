from django.shortcuts import redirect, render
from userauths.forms import UserRegisterForm,ProfileForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from userauths.models import Profile, User

# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            # Create new user
            new_user = form.save()
            # Get the username from the model
            username = form.cleaned_data.get("username")
            # Display username and success message
            messages.success(request, f"Hey {username}, Your account was created successfully.")
            # Match the email and password
            new_user = authenticate(username=form.cleaned_data['email'],
                                    password=form.cleaned_data['password1']
            )
            # Login the user and direct to the index page
            login(request, new_user)
            return redirect("core:index")
    else:
        form = UserRegisterForm()

    context = {
        'form' : form,
    }
    return render(request, "userauth/sign-up.html", context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request, f"Hey, you already logged in.")
        return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "You are logged in.")
                return redirect("core:index")
            else:
                messages.warning(request, "User Does Not Exist. Create an account.")
        except:
            messages.warning(request, f"User with {email} does not exist")

    return render(request, "userauth/sign-in.html")

def logout_view(request):
    logout(request)
    messages.success(request, "You logged out.")
    return redirect("userauths:sign-in")

def profile_update(request):
    try:
        profile = Profile.objects.get(user=request.user)   
    except:
        profile = None
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            messages.success(request, "Profile Updated Successfully.")
            return redirect("core:dashboard")
        
    else:
        form = ProfileForm(instance=profile)

    context = {
        "form": form,
        "profile":profile
    }
    return render(request, "userauth/profile-edit.html", context)
