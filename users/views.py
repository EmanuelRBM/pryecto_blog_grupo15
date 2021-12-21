from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.decorators import login_required

from .models import User, Profile

from django.contrib import messages

from  .forms import SignUpForm, LoginForm, EditProfileForm

from django.urls import reverse

# request para el registro

def signup(request):
    if request.user.is_authenticated:
        return redirect('nucleo:home')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Mostramos un mensaje cuando se termina el registro
            messages.success(request, "Felicidades, Te registraste con exito, ahora sos un nuevo Usurio!")
            return redirect('nucleo:home')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


# request para el login

def log_in(request):
    if request.user.is_authenticated:
        return redirect('nucleo:home')
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            # Comprobamos aca si los datos son correctos
            user = authenticate(email=email, password=password)

            if user: 
                login(request, user)  # Se conecta con el usuario
                return redirect('nucleo:home')
            else:  # sino nos da un error
                messages.error(request, 'Correo electrónico o contraseña no válidos')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})

    # request para el log-out

def log_out(request):
    logout(request)
    return redirect(reverse('users:login'))


# Perfil

@login_required
def profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user)
    return render(request, 'users/profile.html', {'profile': profile, 'user': user})


#edicion usuario

@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(request.user.username, request.POST, request.FILES)
        if form.is_valid():
            about_me = form.cleaned_data["about_me"]
            username = form.cleaned_data["username"]
            image = form.cleaned_data["image"]

            user = User.objects.get(id=request.user.id)
            profile = Profile.objects.get(user=user)
            user.username = username
            user.save()
            profile.about_me = about_me
            if image:
                profile.image = image
            profile.save()
            return redirect("users:profile", username=user.username)
    else:
        form = EditProfileForm(request.user.username)
    return render(request, "users/edit_profile.html", {'form': form})