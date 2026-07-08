from django.shortcuts import render, redirect
from accounts.utils import user_exists, get_user
from .models import *
from django.contrib import messages

def index(request):
    if not user_exists(request):
        return redirect('auth')
    
    user = get_user(request)

    if request.method == 'POST':
        return redirect('index')

    trees = Tree.objects.all()

    context = {
        'user': user,
        'trees': trees
    }

    return render(request, "index.html", context)

def create_tree(request):
    if not user_exists(request):
        return redirect('auth')
    
    user = get_user(request)

    if request.method == 'POST':
        errors = Tree.objects.validate(request.POST)
        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return render(request, "create_tree.html", {
                'saved_data': request.POST,
                'user': user,
                'errors': errors
            })
        
        tree = Tree.objects.create_tree(request.POST, user)
        messages.success(request, 'Tree created successfully !!')
        return redirect('index')
    
    context = {
        'user': user
    }

    return render(request, "create_tree.html", context)

def edit_tree(request, pk):
  if not user_exists(request):
    return redirect('auth')

  user = get_user(request)
  
  tree = Tree.objects.get(pk=pk)

  can_edit_and_delete = tree.creator.id == user.id
    
  user = get_user(request)

  if not can_edit_and_delete:
    return redirect('index')

  if request.method == 'POST':
    errors = Tree.objects.validate(request.POST)
    if errors:
      for key, value in errors.items():
        messages.error(request, value)
      return render(request, "edit_tree.html", {
        'saved_data': request.POST,
        'user': user,
        'tree': tree
      })
    
    tree.edit(request.POST)
    messages.success(request, 'Tree updated successfully !!')
    return redirect('index')

  return render(request, "edit_tree.html", {
    'user': user,
    "tree": tree,
  })

def delete_tree(request, pk):
  if not user_exists(request):
    return redirect('auth')
  
  tree = Tree.objects.get(pk=pk)

  user = get_user(request)

  can_edit_and_delete = tree.creator.id == user.id

  if not can_edit_and_delete:
    return redirect('index')
  
  if request.method == 'POST':
    tree.delete()
    messages.success(request, "Tree deleted successfully !!")
    return redirect('index')
  
  return render(request, "index.html")

def tree_details(request, pk):
  if not user_exists(request):
    return redirect('auth')
  
  user = get_user(request)

  tree = Tree.objects.get(pk=pk)

  visitors = tree.visitors.all()
  is_visited = Visiting.objects.filter(user=user, tree=tree).exists()

  if request.method == 'POST':
    return redirect('index')
  
  return render(request, "tree_details.html", {
    'tree': tree,
    'user': user,
    'visitors': visitors,
    'is_visited': is_visited
  })

def display_zip_code_trees(request, zip):
    if not user_exists(request):
        return redirect('auth')

    user = get_user(request)

    if request.method == 'POST':
        return redirect('index')

    trees = Tree.objects.filter(zip_code=zip)

    context = {
        'user': user,
        'trees': trees,
        'zip': zip,
    }

    return render(request, "display_zip_code_trees.html", context)

def add_to_visiting(request, pk):
  if not user_exists(request):
    return redirect('login')
  
  user = get_user(request)

  tree = Tree.objects.get(pk=pk)
  
  user.visited_trees.add(tree)

  messages.success(request, "Tree added successfully to the visiting list")
  
  return redirect('index')






