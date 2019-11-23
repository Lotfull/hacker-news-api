from rest_framework import response, views

from . import api


class PostsView(views.APIView):
    def get(self, request):
        posts = api.posts.get(request.GET)
        posts_serialized = api.serializers.PostSerializer(posts, many=True).data
        return response.Response(posts_serialized)
