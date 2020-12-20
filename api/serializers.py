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


class AnswerSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField('username', read_only=True)

    def validate(self, attrs):
        if attrs['question'].question_type == 'T' and not attrs['text_answer']:
            raise ValidationError('You have to write answer')
        if attrs['question'].question_type == 'SO' and not attrs['option_selection']:
            raise ValidationError('You have to select one option')
        if attrs['question'].question_type == 'SO' and not len(attrs['option_selection']):
            raise ValidationError('You have to select one option')
        if attrs['question'].question_type == 'MO' and not len(attrs['option_selection']):
            raise ValidationError('You have to select one option')

        return attrs

    class Meta:
        fields = ('user', 'question', 'text_answer', 'option_selection')
        model = Answer
