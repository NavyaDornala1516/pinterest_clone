from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Board
from .forms import BoardForm
from pins.models import Pin
from django.shortcuts import get_object_or_404



@login_required
def boards_list(request):
    boards = Board.objects.filter(user=request.user)  
    return render(request, 'boards/board_list.html', {'boards': boards})

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

def delete_board(request, pk):
    board = get_object_or_404(Board, pk=pk)
    if request.user == board.user:  
        board.delete()
    return redirect('boards_list') 

def board_detail(request, board_id):
    board = get_object_or_404(Board, id=board_id)
    pins = Pin.objects.filter(board=board)  

    context = {
        'board': board,
        'pins': pins
    }
    return render(request, 'boards/board_detail.html', context)

from django.contrib.auth.models import User

def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)

    if request.user == profile_user:
        boards = Board.objects.filter(user=profile_user)
    else:
        boards = Board.objects.filter(user=profile_user, is_private=False)

    return render(request, 'users/profile.html', {
        'profile_user': profile_user,
        'boards': boards
    })
