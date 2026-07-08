from .models import *

def user_exists(request):
  if request.session.get('user_id'):
    return True
  return False

def get_user(request):
  return User.objects.get(id=request.session['user_id'])

