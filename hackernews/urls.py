from django.conf.urls import url
from . import views

urlpatterns = [
    url('', views.PostsView.as_view(), name='posts_view'),
]
