from django.shortcuts import render
from .models import Board
from django.contrib import messages

def boards_list(request):
    boards = Board.objects.all()
    return render(request, 'boards/boards_list.html', {'boards': boards})


def create_board(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')

        if not title:
            messages.error(request, "Title is required.")
            return render(request, 'boards/create_board.html')

        # Save the board
        Board.objects.create(title=title, description=description)
        messages.success(request, "Board created successfully!")
        return redirect('boards_list')  # redirect to list page

    return render(request, 'boards/create_board.html')