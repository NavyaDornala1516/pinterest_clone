from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import BoardForm, PinForm
from boards.models import Board
from .models import Pin, Comment, Like
from django.http import JsonResponse


@login_required
def home(request):
    pins = Pin.objects.filter(user=request.user)  
    return render(request, 'home.html', {'pins': pins})

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username').strip()
        email = request.POST.get('email').strip()
        password = request.POST.get('password').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()  

        if not username or not email or not password:
            messages.error(request, 'Please fill in all required fields.')
            return redirect('register')

        if confirm_password and password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, 'Account created successfully! You can now log in.')
        return redirect('login')

    return render(request, 'register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('login')


@login_required
def create_board(request):
    if request.method == 'POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board = form.save(commit=False)
            board.user = request.user  
            board.save()
            return redirect('boards_list')
    else:
        form = BoardForm()
    return render(request, 'boards/create_board.html', {'form': form})


@login_required
def create_pin(request):
    boards = Board.objects.filter(user=request.user) 
    
    if not boards.exists():
        messages.error(request, "You need to create a board first!")
        return redirect('create_board')

    if request.method == 'POST':
        form = PinForm(request.POST, request.FILES)
        form.fields['board'].queryset = boards
        if form.is_valid():
            pin = form.save(commit=False)
            pin.user = request.user
            pin.save()
            return redirect('home')
    else:
        form = PinForm()
        form.fields['board'].queryset = boards

    return render(request, 'pins/create_pin.html', {'form': form})


def board_list(request):
    boards = Board.objects.all()
    return render(request, 'boards/board_list.html', {'boards': boards})


@login_required
def pin_list(request):
    pins = Pin.objects.filter(user=request.user)
    return render(request, 'pins/pin_list.html', {'pins': pins})

def delete_pin(request, pk):
    pin = get_object_or_404(Pin, pk=pk)
    if request.user == pin.owner:
        pin.delete()
    return redirect('home')

def pin_detail(request, pin_id):
    pin = get_object_or_404(Pin, id=pin_id)
    other_pins = Pin.objects.exclude(id=pin.id)[:10]

    liked_by_user = pin.likes.filter(user=request.user).exists() if request.user.is_authenticated else False

    context = {
        'pin': pin,
        'other_pins': other_pins,
        'liked_by_user': liked_by_user,
    }
    return render(request, 'pins/pin_detail.html', context)


@login_required
def add_comment(request, pin_id):
    pin = get_object_or_404(Pin, id=pin_id)

    if request.method == "POST":
        text = request.POST.get("comment")
        if text:
            Comment.objects.create(
                pin=pin,
                user=request.user,
                text=text
            )
    return redirect('pin_detail', pin_id=pin_id)


@login_required
def toggle_like(request, pin_id):
    pin = get_object_or_404(Pin, id=pin_id)
    user = request.user

    existing_like = Like.objects.filter(pin=pin, user=user).first()

    if existing_like:
        existing_like.delete()
        liked = False
    else:
        Like.objects.create(pin=pin, user=user)
        liked = True

    pin.refresh_from_db()

    return JsonResponse({
        'liked': liked,
        'likes_count': pin.likes.count()
    })


@login_required
def save_pin(request, pin_id):
    pin = get_object_or_404(Pin, id=pin_id)
    if request.user in pin.saved_by.all():
        pin.saved_by.remove(request.user)
        saved = False
    else:
        pin.saved_by.add(request.user)
        saved = True
    return JsonResponse({'saved': saved})


def profile_view(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    saved_pins = profile.user.saved_pins.all()  
    context = {
        'profile': profile,
        'saved_pins': saved_pins,
    }
    return render(request, 'profile.html', context)