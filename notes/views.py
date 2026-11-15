from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Note
from django.db import connection

@login_required
def index(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title and content:
            Note.objects.create(owner=request.user, title=title, content=content)
            return redirect("index")
    
    # Flaw: Broken Access Control
    # Issue: All users can view each other's notes even if they are not the owner
    notes = Note.objects.all()
    # Fix: Only show notes belonging to the logged-in user
    # notes = Note.objects.filter(owner=request.user)

    search = request.GET.get("search", "")

    if search:
        # Flaw: Injection
        # Issue: Users can manipulate the SQL query through the search bar
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT id FROM notes_note WHERE owner_id = {request.user.id} "
                f"AND title LIKE '%{search}%'"
            )
            ids = [row[0] for row in cursor.fetchall()]

        notes = Note.objects.filter(id__in=ids)

    # Fix: Use Django's filter() method instead of raw SQL
    # notes = Note.objects.filter(owner=request.user, title__icontains=search)

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