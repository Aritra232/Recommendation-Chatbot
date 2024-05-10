from django.contrib import admin
from django.urls import path, include  # Include the include function to include URLs from your chatbot app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('chatbot.urls')),  # Include URLs from your chatbot app
]
