from rest_framework import serializers

from .models import Survey, Question


class SurveySerializer(serializers.ModelSerializer):
    questions = serializers.StringRelatedField(many=True)

    def validate(self, attrs):
        instance = Survey(**attrs)
        instance.clean()

        return attrs

    class Meta:
        fields = ('name', 'start_date', 'finish_date', 'description', 'questions')
        model = Survey


class QuestionSerializer(serializers.ModelSerializer):
    survey = serializers.StringRelatedField(source='survey.name')

    class Meta:
        fields = ('text', 'question_type', 'survey')
        model = Question
