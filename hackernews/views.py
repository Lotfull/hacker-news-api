import os

from rest_framework import generics, filters, pagination

from . import api
from .models import Post


class PostsLimitOffsetPagination(pagination.LimitOffsetPagination):
    default_limit = os.environ.get('POSTS_API_LIMIT_DEFAULT', 5)
    max_limit = os.environ.get('POSTS_API_LIMIT_MAX', 100)


class PostsView(generics.ListAPIView):
    serializer_class = api.serializers.PostSerializer
    pagination_class = PostsLimitOffsetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['created']

    def get_queryset(self):
        force = self.request.GET.get('force')
        force = force is True or force == '1' or force == 'true' or force == 'True'
        if force or not Post.objects.exists():
            api.posts.scrap()

        return Post.objects.all()
