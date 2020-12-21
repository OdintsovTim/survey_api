import datetime

from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import Survey, Question, Answer


class SurveySerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        print(attrs)
        if attrs['finish_date'] <= attrs['start_date']:
            raise ValidationError('Finish date must be later than start date!')
        if attrs['start_date'] < datetime.date.today():
            raise ValidationError('You cannot create a survey retroactively')

        return attrs

    def update(self, instance, validated_data):
        if 'finish_date' in validated_data:
            raise ValidationError('You must not change finish_date field.')

        return super().update(instance, validated_data)

    class Meta:
        fields = ('name', 'start_date', 'finish_date', 'description')
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


class DoneSurveyAnswerSerializer(AnswerSerializer):
    class Meta(AnswerSerializer.Meta):
        fields = ('question', 'text_answer', 'option_selections')


class DoneSurveySerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    survey = serializers.SlugRelatedField(slug_field='name', read_only=True)
    answers = DoneSurveyAnswerSerializer(many=True)

    class Meta:
        fields = ('user', 'survey', 'answers')
        model = DoneSurvey
