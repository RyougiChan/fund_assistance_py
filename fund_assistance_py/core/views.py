from django.shortcuts import render


def signin(request):
    return render(request, 'signin.html')
