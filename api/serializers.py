import datetime

from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from .models import Survey, Question, Answer, Option, DoneSurvey


class OptionSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        if attrs['question'].question_type == 'T':
            raise ValidationError('It is text question')

        return attrs

    class Meta:
        model = Option
        fields = ('text', 'question')


class OptionQuestionSerializer(OptionSerializer):
    class Meta(OptionSerializer.Meta):
        fields = ('text',)


class QuestionSerializer(WritableNestedModelSerializer):
    survey = serializers.SlugRelatedField(slug_field='name', queryset=Survey.objects.all())
    options = OptionQuestionSerializer(many=True, required=False)

    class Meta:
        fields = ('text', 'question_type', 'survey', 'options')
        model = Question


class QuestionSurveySerializer(QuestionSerializer):
    class Meta(QuestionSerializer.Meta):
        fields = ('text', 'question_type', 'options')


class SurveySerializer(WritableNestedModelSerializer):
    questions = QuestionSurveySerializer(many=True, required=True)

    def validate(self, attrs):
        if self.context['request'].method == 'PATCH':
            if attrs.get('start_date'):
                raise ValidationError('You must not change start_date field.')

            start_date = self.instance.start_date
            finish_date = attrs.get('finish_date', self.instance.finish_date)
            self.validate_finish_later_start(start_date, finish_date)
        else:
            self.validate_finish_later_start(attrs['start_date'], attrs['finish_date'])

            if attrs['start_date'] < datetime.date.today():
                raise ValidationError('You cannot create a survey retroactively')

        return attrs

    @staticmethod
    def validate_finish_later_start(start_date, finish_date):
        if finish_date <= start_date:
            raise ValidationError('Finish date must be later than start date!')

    class Meta:
        fields = ('name', 'start_date', 'finish_date', 'description', 'questions')
        model = Survey


class AnswerSerializer(WritableNestedModelSerializer):
    user = serializers.SlugRelatedField('username', read_only=True)
    question = serializers.SlugRelatedField(
        slug_field='text',
        queryset=Question.objects.all(),
    )
    option_selections = OptionSerializer(many=True, required=False)

    def validate(self, attrs):
        if attrs['question'].question_type == 'T' and not attrs.get('text_answer'):
            raise ValidationError('You have to write answer')
        if attrs['question'].question_type == 'SO' and not attrs.get('option_selections'):
            raise ValidationError('You have to select one option')
        elif (attrs['question'].question_type == 'SO'
              and (len(attrs['option_selections']) > 1 or self.initial_data.get('option_selections'))):
            raise ValidationError('You have to select only one option')
        if attrs['question'].question_type == 'MO' and not len(attrs.get('option_selections')):
            raise ValidationError('You have to select one option')

        return attrs

    class Meta:
        fields = ('user', 'question', 'text_answer', 'option_selections')
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
