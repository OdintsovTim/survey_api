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
    survey = serializers.SlugRelatedField(slug_field='name', queryset=Survey.objects.all())
    options = serializers.StringRelatedField(many=True)

    class Meta:
        fields = ('text', 'question_type', 'survey', 'options')
        model = Question
