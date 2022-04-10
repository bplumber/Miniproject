from django.urls import path,include
import user.views as views
urlpatterns = [
    path('',views.index,name='home')
]