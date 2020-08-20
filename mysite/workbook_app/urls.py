from django.urls import path
from . import views

app_name = 'workbook_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('course/', views.CourseView.as_view(), name='course-list'),
    path('course/<slug:course_id>/quiz', views.CourseQuizList.as_view(), name='course-quiz-list'),
    path('course/<slug:course_id>/quiz/<slug:quiz_id>/question', views.QuizQuestionList.as_view(), name='quiz-question-list'),
    path('course/<str:course_id>/quiz/<str:quiz_id>/question/<slug:slug>/detail', views.QuestionDetailView.as_view(), name='question-detail'),
    path('course/<slug:course_id>/quiz/<slug:quiz_id>/question/choose', views.choose, name='choose'),
    path('course/<slug:course_id>/quiz/<slug:quiz_id>/question/choose/results/<str:rate>/<str:percent_rate>', views.results, name='results')
]

