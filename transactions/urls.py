from django.urls import path

from . import views

app_name = "transactions"
urlpatterns = [
    path("stats", views.StatsView.as_view(), name="stats"),
    path("", views.IndexView.as_view(), name="index"),
    path("upload/", views.upload, name="upload")
    # path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # path("<int:question_id>/vote/", views.vote, name="vote"),
]
