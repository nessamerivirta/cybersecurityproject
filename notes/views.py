from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Note

@login_required
def index(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title and content:
            Note.objects.create(owner=request.user, title=title, content=content)
            return redirect("index")
    
    # Flaw: Broken Access Control
    notes = Note.objects.all()
    
    # Fix: Only show the current logged-in user's notes
    # notes = Note.objects.filter(owner=request.user)

    return render(request, "notes/index.html", {"notes": notes})

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = UserCreationForm()

    return render(request, "notes/register.html", {"form": form})