from django.urls import path,include
import user.views as views
import django.contrib.auth.views as auth_views
urlpatterns = [
    path('',views.index,name='home'),
    path('register/',views.register,name='register'),
    path('login/',auth_views.LoginView.as_view(template_name = 'login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'logout.html'),name='logout'),
    path('dashboard/',views.dashboard,name = 'dash'),
    path('explore/',views.explore,name = 'explore'),
    path('save/',views.saveresult,name = 'save'),
    path('share/',views.shareresult,name = 'share'),
    path('delete/',views.deleteLink,name='delete'),
]
