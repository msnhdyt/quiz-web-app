from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from topic import views as topicviews
from quizzes import views as quizviews

urlpatterns = [
    path('', topicviews.TopicView.as_view()),
    path('<str:user_id>/join/', topicviews.Join.as_view()),
    path('<str:user_id>/', topicviews.UserTopicView.as_view()),
    path('<str:code>/detail/', topicviews.TopicDetailView.as_view()),
    #path('<str:code>/all-quiz/', topicviews.TopicQuizView.as_view()),
    #re_path(r'^(?P<user_id>)\w+/(?P<code>)\w{10}/$', quizviews.QuizzesView.as_view()),
    path('<int:user_id>/<str:code>/', quizviews.QuizzesView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)