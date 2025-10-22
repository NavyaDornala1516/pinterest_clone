from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Profile
from .forms import ProfileForm


def view_profile(request, username):
    profile = get_object_or_404(Profile, user__username=username)

    saved_pins = Pin.objects.filter(saved_by=profile.user)

    context = {
        'profile': profile,
        'saved_pins': saved_pins,
    }
    return render(request, 'profile.html', context)

@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user, defaults={'bio': ''})
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('view_profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'profile/edit_profile.html', {'form': form})


@login_required
def my_profile(request):
    return redirect('view_profile', username=request.user.username)
