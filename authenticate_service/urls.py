from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView
from django.urls import path,include
from . import views

urlpatterns = [
    path('create-user/',views.UserCreateView.as_view()),
    path('api/token/', views.CustomView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('get-user/',views.GetUser.as_view()),
    path('google-signup/',views.GoogleUserCreateView.as_view(),name='google-signup'),
]