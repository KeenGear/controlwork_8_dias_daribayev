from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import PostListView, PostCreateView, PostUpdateView, PostDeleteView, PostDetailView

urlpatterns = [
    path('', PostListView.as_view(), name='home'),
    path('create/', login_required(PostCreateView.as_view()), name='post_create'),
    path('update/<int:pk>', login_required(PostUpdateView.as_view()), name='post_update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:pk>', PostDetailView.as_view(), name='post_detail'),
]
