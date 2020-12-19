from rest_framework import serializers

from .models import Survey, Question


class SurveySerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        instance = Survey(**attrs)
        instance.clean()

        return attrs

    class Meta:
        fields = ('name', 'start_date', 'finish_date', 'description')
        model = Survey


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('text', 'response_type', 'survey')
        model = Question
