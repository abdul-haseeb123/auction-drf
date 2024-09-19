from auction import views
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView, TokenVerifyView)

urlpatterns = [
    path("users/", views.UserList.as_view()),
    path("users/<int:pk>/", views.UserDetail.as_view()),
    path("users/login", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("users/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/change-password", views.change_password)
]

urlpatterns = format_suffix_patterns(urlpatterns)