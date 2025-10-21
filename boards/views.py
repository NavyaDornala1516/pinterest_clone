from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Board
from .forms import BoardForm

def boards_list(request):
    boards = Board.objects.all()
    return render(request, 'boards/boards_list.html', {'boards': boards})

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
