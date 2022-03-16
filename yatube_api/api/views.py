from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from rest_framework import viewsets, status
from rest_framework.response import Response

from serializers import GroupSerializer, PostSerializer, CommentSerializer

from posts.models import Comment, Group, Post


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def post_create(self, serializer):
        serializer.save(author=self.request.user)

    def post_update(self, serializer):
        if self.request.user != serializer.instance.author:
            raise PermissionDenied()
        serializer.save(author=self.request.user, status=status.HTTP_200_OK)

    def post_delete(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        return Comment.objects.filter(post=post)

    def comment_create(self, serializer):
        post_id = self.kwargs.get('post_id')
        serializer.save(author=self.request.user,
                        post=get_object_or_404(Post, id=post_id))

    def comment_update(self, serializer):
        post_id = self.kwargs.get('post_id')
        if self.request.user != serializer.instance.author:
            raise PermissionDenied()
        serializer.save(author=self.request.user, 
                        post=get_object_or_404(Post, id=post_id),
                        status=status.HTTP_200_OK)

    def comment_delete(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
