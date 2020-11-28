from django.urls import path
from . import views
urlpatterns = [
    path('login/', views.getLogin, name="getLogin"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.user_logout, name="logout"),
    path('api/userData/', views.myData, name="myData"),
    path('update/profile/', views.update_profile, name="profile_update")
]