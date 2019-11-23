import os

from rest_framework import generics, filters, pagination, response

from .api.scrap import scrap
from .api.serializers import PostSerializer
from .models import Post


class PostsLimitOffsetPagination(pagination.LimitOffsetPagination):
    default_limit = int(os.environ.get('POSTS_API_LIMIT_DEFAULT', 5))
    max_limit = int(os.environ.get('POSTS_API_LIMIT_MAX', 100))

    def get_paginated_response(self, data):
        return response.Response(data)


class PostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PostsLimitOffsetPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
    ordering = ['created']

    def get_queryset(self):
        force = self.request.GET.get('force')
        force = force is True or force == '1' or force == 'true' or force == 'True'
        if force or not Post.objects.exists():
            scrap()

        return Post.objects.all()
