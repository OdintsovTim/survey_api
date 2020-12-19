from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'surveys', views.SurveyViewSet)
router.register(r'questions', views.QuestionViewSet)

urlpatterns = [
    path('v1/', include(router.urls))
]
