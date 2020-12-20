from rest_framework import viewsets

from .models import Survey, Question
from .serializers import SurveySerializer, QuestionSerializer


class SurveyViewSet(viewsets.ModelViewSet):
    serializer_class = SurveySerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return Survey.objects.all()
        return Survey.objects.get_active_surveys()


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
