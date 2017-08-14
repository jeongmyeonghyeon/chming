from rest_framework import generics, permissions

from group.models import Group
from utils.permissions import AuthorIsRequestUser
from ..models import Post, Comment

from ..serializer import PostSerializer, PostDetailSerializer, PostPagination

__all__ = (
    'PostListView',
    'PostImageListView',
    'PostNoticeListView',
    'PostCreateView',
    'PostRetrieveView',
    'PostUpdateView',
    'PostDestroyView',
)


class PostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PostPagination

    def get_queryset(self):
        group_pk = self.kwargs['group_pk']
        group = Group.objects.get(pk=group_pk)
        queryset = Post.objects.filter(group=group)
        return queryset


class PostImageListView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PostPagination

    def get_queryset(self):
        group_pk = self.kwargs['group_pk']
        group = Group.objects.get(pk=group_pk)
        return Post.objects.filter(group=group).exclude(post_img='')


class PostNoticeListView(generics.ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        group_pk = self.kwargs['group_pk']
        group = Group.objects.get(pk=group_pk)
        return Post.objects.filter(group=group).exclude(post_type='False')


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


class PostRetrieveView(generics.RetrieveAPIView):
    serializer_class = PostDetailSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorIsRequestUser,
    )

    def get_queryset(self):
        group_pk = self.kwargs['group_pk']
        group = Group.objects.get(pk=group_pk)
        return Post.objects.filter(group=group)


class PostUpdateView(generics.UpdateAPIView):
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorIsRequestUser,
    )

    def get_queryset(self):
        group_pk = self.kwargs['group_pk']
        group = Group.objects.get(pk=group_pk)
        return Post.objects.filter(group=group)


class PostDestroyView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        AuthorIsRequestUser,
    )
