from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('user/list/', views.UserListView.as_view(), name='user_list'),
    path('user/<int:id>', views.UserDetailView.as_view(), name='profile'),
    path('user/update/', views.UpdateUserView.as_view(), name='update_profile'),
    path('user/currentuser/', views.CurrentUserView.as_view(), name='currentuser'),
]
