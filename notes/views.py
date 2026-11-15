from django.shortcuts import render, redirect
from .models import Note


def index(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if title and content:
            Note.objects.create(title=title, content=content)
            return redirect("index")
        
    notes = Note.objects.all()
    return render(request, "notes/index.html", {"notes": notes})