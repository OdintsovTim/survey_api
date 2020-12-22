from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'surveys', views.SurveyViewSet, basename='surveys')
router.register(r'questions', views.QuestionViewSet)
router.register(r'answers', views.AnswerViewSet, basename='answers')
router.register(r'done-surveys', views.DoneSurveyViewSet, basename='done_surveys')

urlpatterns = [
    path('', include(router.urls)),
]
