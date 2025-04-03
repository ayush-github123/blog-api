from django.urls import path
from posts import views


urlpatterns = [
    path('posts/', views.PostListCreateView.as_view(), name='post_list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),

    path('categories/', views.CategoryListCreateView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),

    path('tags/', views.TagListCreateView.as_view(), name='tag_list'),
    path('tags/<int:pk>/', views.TagDetailView.as_view(), name='tag_detail'),

    path('posts/<int:pk>/comments/', views.CommentListCreateView.as_view(), name='comment_list'),
    path('posts/<int:pk>/comments/<int:comment_pk>/', views.CommentDetailView.as_view(), name='comment_detail'),

    path('likes/', views.LikeDislikeListView.as_view(), name='react'),  # For listing liking/disliking
    path('like/', views.LikeDislikeCreateView.as_view(), name='react'),  # For liking/disliking

]
