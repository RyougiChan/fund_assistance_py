from django.shortcuts import render, redirect

from analysis.conf.yconfig import YConfig


def entry(request):
    return render(request, 'entry.html')


def signin(request):
    return render(request, 'signin.html') if YConfig.get('jwt:enable') == 1 else redirect('/error')


def error(request):
    return render(request, 'error_500.html')
