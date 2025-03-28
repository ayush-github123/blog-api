from rest_framework import generics, permissions
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.contrib.contenttypes.models import ContentType
from posts.permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from posts.models import Post, Comment, Tag, Category, LikeDislike
from posts.serializers import PostSerializer, CommentSerializer, LikeDislikeSerializers, TagSerializer, CategorySerializer


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class TagDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAdminUser]


class PostListCreateView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def get_queryset(self):
        queryset = Post.objects.all()
        category_id = self.request.query_params.get('category')
        tag_id = self.request.query_params.get('tag')

        if category_id:
            queryset = queryset.filter(category__id=category_id)
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """Get all comments for a specific post"""
        post_id = self.kwargs.get('pk')
        if not post_id:
            raise NotFound(detail="Post ID is required in the URL.", code=400)
        return Comment.objects.filter(post__id=post_id)

    def perform_create(self, serializer):
        """Create a comment for a specific post"""
        post_id = self.kwargs.get('pk')
        if not post_id:
            raise NotFound(detail="Post ID is required in the URL.", code=400)

        post = get_object_or_404(Post, id=post_id)
        serializer.save(user=self.request.user, post=post)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer    
    permission_classes = [IsOwnerOrReadOnly]


class LikeDisklikeListView(generics.ListAPIView):
    serializer_class = LikeDislikeSerializers
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Get all likes and dislikes of a specific user"""
        user = self.request.user
        return LikeDislike.objects.filter(user=user).select_related('content_type')


class LikeDislikeCreateView(generics.CreateAPIView):
    serializer_class = LikeDislikeSerializers
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """Create a like or dislike for a specific content"""
        user = self.request.user
        content_type_model = self.request.data.get('content_type') # content type tells us what type of content we are dealing with
        object_id = self.request.get('object_id') # object id tells us which specific content we are dealing with
        value = self.request.data.get('value')

        try:
            content_type = ContentType.objects.get(model=content_type_model)
        except ContentType.DoesNotExist:
            raise Response({"error": "Invalid content type"}, status=status.HTTP_400_BAD_REQUEST)


        existing_reaction = LikeDislike.objects.filter(
            user=user, content_type=content_type, object_id=object_id
        ).first()

        if existing_reaction:
            existing_reaction.value = value # if the user has already reacted, update the value
            existing_reaction.save()
            return Response({ existing_reaction.content_object.id: existing_reaction.value}, status=status.HTTP_200_OK)
        else:
            serializer.save(user=user, content_type=content_type, object_id=object_id, value=value)




