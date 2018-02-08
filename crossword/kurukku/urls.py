from django.urls import path

from . import views

urlpatterns = [
    path(r'', views.index, name='index'),
    path(r'', views.new_puzzle_view, name='new_puzzle'),
]