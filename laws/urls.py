from django.urls import path
from . import views

urlpatterns = [
    path("", views.law_list, name="law_list"),
    path("law/<int:id>/", views.law_detail, name="law_detail"),
    path("law/<int:id>/add-version/", views.add_version, name="add_version"),
    path("bookmark/<int:id>/", views.add_bookmark, name="add_bookmark"),
    path("my-bookmarks/", views.my_bookmarks, name="my_bookmarks"),
    path("activity_logs/", views.activity_logs, name="activity_logs"),
    path("law/<int:law_id>/compare/", views.compare_versions, name="compare_versions"),
]