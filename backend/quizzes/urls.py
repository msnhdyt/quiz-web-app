from django.urls import path, re_path
from django.urls.conf import include
from rest_framework.urlpatterns import format_suffix_patterns
from quizzes.views import QuizzesView, TakeQuizView, QuizTakenView, AllReportView, DetailReportView, SubmitView, CalculateView
from question.views import QuestionView

extra_patterns = [
    path('question-answer/', QuestionView.as_view()),
    # path('answer/', )
    path('report/',AllReportView.as_view()),
    path('calculate/', CalculateView.as_view()),
    path('<str:user_id>/', QuizTakenView.as_view()),
    path('<str:user_id>/take/', TakeQuizView.as_view()),
    path('<str:user_id>/submit/', SubmitView.as_view()),
    path('<str:user_id>/report/', DetailReportView.as_view()),
]
urlpatterns = [
    # path('', QuizzesView.as_view()),
    path('<str:quiz_id>/', include(extra_patterns)),
]

urlpatterns = format_suffix_patterns(urlpatterns)