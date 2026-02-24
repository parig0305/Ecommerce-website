from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')

        if password1 != password2:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists!')
            return redirect('register')

        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )

        # Create user profile
        UserProfile.objects.create(
            user=user,
            phone=phone,
            address=address
        )

        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')

    return render(request, 'register.html')


def user_login(request):
    if request.method == 'POST':
        # Try to get username from email
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Try to find user by email
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            username = email

        # Authenticate using username
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            
            # Redirect to next page if provided
            next_page = request.GET.get('next')
            if next_page:
                return redirect(next_page)
            return redirect('home')
        else:
            messages.error(request, 'Invalid email or password!')
            return redirect('login')

    return render(request, 'login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out!')
    return redirect('login')


@login_required
def profile(request):
    # Get or create user profile
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email', user.email)
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.save()

        user_profile.phone = request.POST.get('phone', user_profile.phone)
        user_profile.address = request.POST.get('address', user_profile.address)
        user_profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    return render(request, 'profile.html', {'profile': user_profile})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'profile.html', {'form': form, 'profile': request.user.userprofile})
