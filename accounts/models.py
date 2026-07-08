from django.db import models
import re
import bcrypt
from datetime import datetime

class UserManager(models.Manager):
  def validate_register(self, data):
    errors = {}
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')
    email = data.get('email', '')
    password = data.get('password', '')
    confirm_password = data.get('confirm_password', '')

    if not first_name:
      errors['first_name'] = 'First name is required'
    
    if first_name and len(first_name) < 2:
      errors['first_name'] = 'First name should be at least 2 characters'

    if not last_name:
      errors['last_name'] = 'Last name is required'
    
    if last_name and len(last_name) < 2:
      errors['last_name'] = 'Last name should be at least 2 characters'

    if not email:
      errors['email'] = 'Email is required'

    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

    if email and not EMAIL_REGEX.match(data['email']):
        errors['email'] = "Invalid email address!"

    exists = self.filter(email=email).exists()
    if exists:
      errors['email'] = 'This email is already exists'

    if not password:
      errors['password'] = 'Password is required'

    if not confirm_password:
      errors['confirm_password'] = 'Confirm Password is required'
      
    if password != confirm_password:
      errors['password'] = "Passwords are not matched"

    if password and len(password) < 8:
      errors['password'] = "Password should be at least 8 characters"

    return errors

  
  def create_user(self, data):
        hashed_password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
        user = User(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password=hashed_password)
        user.save()
        return user
    
  def validate_login(self, email, password):
        errors = {}
        if not email or not password:
          errors['login'] = 'Email and Password are required'
          return errors, None
        user = self.filter(email=email).first()

        if user:
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return errors, user
            else:
                errors['login'] = "Invalid email or password."
        else:
            errors['login'] = "Invalid email or password."

        return errors, None


class User(models.Model):
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  email = models.EmailField(max_length=100, unique=True)
  password = models.CharField(max_length=100)
  objects = UserManager()

