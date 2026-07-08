from .models import *

def user_exists(request):
  return 'user_id' in request.session

def get_user(request):
  return User.objects.get(id=request.session['user_id'])