from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', index, name="index"),
    path('trees/create', create_tree, name="create_tree"),
    path('trees/<int:pk>/edit', edit_tree, name="edit_tree"),
    path('trees/<int:pk>/delete', delete_tree, name="delete_tree"),
    path('trees/<int:pk>', tree_details, name="tree_details"),
    path('trees/<str:zip>/display-zip-code-trees', display_zip_code_trees, name="display_zip_code_trees"),
    path('trees/<int:pk>/add-to-visiting', add_to_visiting, name="add_to_visiting"),
]
