from django.shortcuts import render, redirect
from accounts.models import User
from django.contrib import messages
from .utils import *

def auth(request):
  if user_exists(request):
    return redirect('index')
    
  if request.method == 'POST':
    if request.POST.get('type') == 'register':
      errors = User.objects.validate_register(request.POST)
      if errors:
        for key, value in errors.items():
          messages.error(request, value, extra_tags="register")
        return render(request, "accounts/auth.html", {
          'saved_data': request.POST
        })
      user = User.objects.create_user(request.POST)
      request.session['user_id'] = user.id
      return redirect('index')

    elif request.POST.get('type') == 'login':
      errors, user = User.objects.validate_login(request.POST.get('email'), request.POST.get('password'))
      if errors:
        for key, value in errors.items():
          messages.error(request, value, extra_tags="login")
        return render(request, "accounts/auth.html", {
          'login_saved_data': request.POST
        })
      
      if user:
        request.session['user_id'] = user.id
        return redirect('index')
      
  return render(request, "accounts/auth.html")


def logout(request):
  request.session['user_id'] = None
  return redirect('auth')
