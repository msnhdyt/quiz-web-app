from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('topic/', include('topic.urls')),
    path('quiz/', include('quizzes.urls')),
    # path('question/', include('question.urls')),
]
