from django.urls import path, include, re_path

from srproj.accounts.views import user_profile, user_registration, UserLoginView, \
    logout_view, UserPassChangeView

urlpatterns = (
    path('register/', user_registration, name='register user'),
    path('profile/<int:pk>/', user_profile, name='user profile'),
    path('login/', UserLoginView.as_view(), name='login user'),
    path('logout/', logout_view, name='logout user'),
    path('password/', UserPassChangeView.as_view(), name='change password'),
)
