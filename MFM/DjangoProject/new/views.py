from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from new.models import UserProfile


def register_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        gender = request.POST['Gender']
        phone = request.POST['phone']
        email = request.POST['email']
        username = request.POST['username']
        password = make_password(request.POST['password'])

        if UserProfile.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        UserProfile.objects.create(
            name=name,
            gender=gender,
            phone=phone,
            email=email,
            username=username,
            password=password
        )
        # messages.success(request, 'Account created successfully. Please login.')
        # return redirect('login')

        return HttpResponse("""
                    <script>
                        alert("Account created successfully. Please login.");
                        window.location.href = '/login';
                    </script>
                """)

    return render(request, 'register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = UserProfile.objects.get(username=username)
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                messages.success(request, f'Welcome {user.name}!')
                return redirect('products_index')
            else:
                messages.error(request, 'Invalid password.')
        except UserProfile.DoesNotExist:
            messages.error(request, 'User not found.')

    return render(request, 'login.html')

def products_index(request):
    if not request.session.get('user_id'):
        return redirect('login')

    user = UserProfile.objects.get(id=request.session['user_id'])
    return render(request, 'index.html', {"user": user})


