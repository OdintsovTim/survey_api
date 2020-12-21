from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from .models import Survey, Question, Answer
from .permissions import IsAdminOrReadOnly
from .serializers import SurveySerializer, QuestionSerializer, AnswerSerializer


class SurveyViewSet(viewsets.ModelViewSet):
    serializer_class = SurveySerializer
    # permission_classes = (IsAdminOrReadOnly,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Survey.objects.all()
        return Survey.objects.get_active_surveys()


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminUser,)


class AnswerViewSet(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    queryset = Answer.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DoneSurveyViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DoneSurveySerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return DoneSurvey.objects.all()
        return DoneSurvey.objects.get_own_done_surveys(self.request.user)
