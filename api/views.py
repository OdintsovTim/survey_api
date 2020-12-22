from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Survey, Question, Answer, UsersSurveyState, DoneSurvey
from .permissions import IsAdminOrReadOnly
from .serializers import SurveySerializer, QuestionSerializer, AnswerSerializer, DoneSurveySerializer


class SurveyViewSet(viewsets.ModelViewSet):
    serializer_class = SurveySerializer
    permission_classes = (IsAdminOrReadOnly,)
    queryset = Survey.objects.all()

    def get_queryset(self):
        if self.request.user.is_staff:
            return Survey.objects.all()
        return Survey.objects.get_active_surveys()

    @action(detail=True, methods=['get'])
    def start(self, request, pk=None):
        current_questions_number = 0
        survey = self.get_object()

        try:
            current_questions_number = UsersSurveyState.objects.get(
                user=request.user,
                survey=survey
            ).current_questions_number
        except ObjectDoesNotExist:
            UsersSurveyState.objects.create(
                user=request.user,
                survey=survey,
                current_questions_number=0,
                is_finished=False
            )

        question = Question.objects.filter(survey=pk)[current_questions_number]
        serializer = QuestionSerializer(question)

        return Response(serializer.data)


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
