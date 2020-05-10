from django.urls import path
from .views import UserCreateView,  UserProfileDelete, UserProfileView, UserProfileUpdate

# URLs for User related views
urlpatterns = [
    path('profile/create', UserCreateView.as_view(), name='user_create'),
    path('profile/update', UserProfileUpdate.as_view(), name='user_update'),
    path('profile/retrieve', UserProfileView.as_view(), name='user_detail'),
    path('profile/delete', UserProfileDelete.as_view(), name='user_delete'),
]