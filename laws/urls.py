from django.urls import path
from . import views

urlpatterns = [
    path('', views.law_list, name='law_list'),
    path('law/<int:id>/', views.law_detail, name='law_detail'),

    path('bookmark/<int:id>/', views.add_bookmark, name='add_bookmark'),
    path('my-bookmarks/', views.my_bookmarks, name='my_bookmarks'),
]