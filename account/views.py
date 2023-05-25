from django.http import HttpResponse
from django.shortcuts import render
from .models import Name

def hello_world(request):
    """A simple view that returns a string "Hello, world!"""
    return HttpResponse("Hello, world!")

def add_numbers(request):
    """A view that returns the sum of two numbers."""
    if request.method == 'POST':
        num1 = int(request.POST.get('num1'))
        num2 = int(request.POST.get('num2'))
        sum = num1 + num2
        return HttpResponse(f"The sum of {num1} and {num2} is {sum}.")
    else:
        return HttpResponse("Please submit the form to add two numbers.")

def name_list(request):
    """A view that returns a list of names."""
    names = Name.objects.all()
    return render(request, 'account/name_list.html', {'names': names})

