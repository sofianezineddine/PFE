from django.shortcuts import redirect, render
from userauth.forms import UserRegisterForm
from django.contrib.auth import login , authenticate,logout
from django.contrib import messages
from django.conf import settings
from userauth.models import User,Profile
from userauth.forms import ProfileForm 


def register_view(request):

    if request.method == "POST":

        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            new_user= form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,f"Hey {username}, You Account Was Created Successfully")
            new_user = authenticate(username=form.cleaned_data['email'],password= form.cleaned_data['password1'])
            login(request,new_user)
            return redirect("core:index")
    else :
        form = UserRegisterForm()
    
    context = {
        'form' : form,
        'page_name': "S'inscrire",
    }

    return render(request,"userauth/sign-up.html",context)



def login_view(request):
    # if request.user.is_authenticated:
    #      messages.warning(request, f"Hey you are already Logged In.")
    #      return redirect("core:index")
    
    if request.method == "POST":
        email = request.POST.get("email") # peanuts@gmail.com
        password = request.POST.get("password") # getmepeanuts

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, email=email, password=password)
            if user is not None:
                    login(request, user)
                    messages.success(request, "You are logged in.")
                    if user.is_superuser :
                        next_url = request.GET.get("next", 'http://127.0.0.1:8000/admin')
                        return redirect(next_url)
                    else :
                        next_url = request.GET.get("next", 'core:index')
                        return redirect(next_url)
                         
            else:
                    messages.warning(request, "User Does Not Exist, create an account.")
        except:
            messages.warning(request, f"User with {email} does not exist")
    context = {
         'page_name' : 'Se Connecter',
    }    
    return render(request, "userauth/sign-in.html",context)



def logout_view(request):
    del request.user
    logout(request)
    messages.success(request, "You logged out.")
    return redirect("core:index")



def profile_update(request):
    profile = Profile.objects.get(user=request.user)
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
        "profile": profile,
        "page_name":"Edit Profile",
    }

    return render(request, "userauth/profile-edit.html", context)