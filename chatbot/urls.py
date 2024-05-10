from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.signuppage,name='sign'),
    path('login', views.loginpage,name='login'),
    path('home', views.home,name='home'),
    path('logout', views.logoutpage,name='logout'),
    #path('', views.home, name='home'),
    path('get-response/', views.get_response, name='get_response'),
]

