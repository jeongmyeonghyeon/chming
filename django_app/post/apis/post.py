from rest_framework import generics, permissions

from group.models import Group
from utils.permissions import AuthorIsRequestUser
from ..models import Post, Comment

from ..serializer import PostSerializer

__all__ = (
    'PostListView',
    'PostCreateView',
    'PostRetrieveAPIView',
    'PostUpdateAPIView',
    'PostDestroyAPIView',
)


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        group_pk = self.kwargs['group_pk']
        group = Group.objects.get(pk=group_pk)
        return Post.objects.filter(group=group)


class PostCreateView(generics.CreateAPIView):
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        group_pk = self.kwargs['group_pk']
        group = Group.objects.get(pk=group_pk)
        instance = serializer.save(author=self.request.user, group=group)
        comment_content = self.request.data.get('comment')
        if comment_content:
            instance.comment_set = Comment.objects.create(
                post=instance,
                author=instance.author,
                content=comment_content,
            )
        instance.save()

    def get_queryset(self):
        group_pk = self.kwargs['group_pk']
        group = Group.objects.get(pk=group_pk)
        return Post.objects.filter(group=group)


class PostRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorIsRequestUser,
    )

    def get_queryset(self):
        group_pk = self.kwargs['group_pk']
        group = Group.objects.get(pk=group_pk)
        return Post.objects.filter(group=group)


class PostUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorIsRequestUser,
    )

    def get_queryset(self):
        group_pk = self.kwargs['group_pk']
        group = Group.objects.get(pk=group_pk)
        return Post.objects.filter(group=group)


class PostDestroyAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorIsRequestUser,
    )
