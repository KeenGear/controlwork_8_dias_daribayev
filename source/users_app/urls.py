from django.urls import path
from .views import LoginView, logout_view, signup, ProfileView, UpdateUserProfileView

urlpatterns = [
    path('signin/', LoginView.as_view(), name='signin'),
    path('signout/', logout_view, name='signout'),
    path('signup/', signup, name='signup'),
    path('profile/<int:pk>', ProfileView.as_view(), name='profile'),
    path('profile_update/<int:pk>', UpdateUserProfileView.as_view(), name='update'),
]
