from django.db import models
from django.contrib.auth import get_user_model

from .managers import SurveyManager, DoneSurveyManager


User = get_user_model()


class Survey(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    start_date = models.DateField()
    finish_date = models.DateField()
    description = models.CharField(max_length=200)
    objects = SurveyManager()

    def __str__(self):
        return self.name


class Question(models.Model):
    TEXT_ANSWER = 'T'
    SINGLE_OPTION = 'SO'
    MULTIPLE_OPTIONS = 'MO'
    QUESTION_TYPE_CHOICES = [
        (TEXT_ANSWER, 'Text answer'),
        (SINGLE_OPTION, 'Single option'),
        (MULTIPLE_OPTIONS, 'Multiple options'),
    ]

    text = models.CharField(max_length=300, db_index=True)
    question_type = models.CharField(max_length=100, default=TEXT_ANSWER, choices=QUESTION_TYPE_CHOICES)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.text


class Option(models.Model):
    text = models.CharField(max_length=200, db_index=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')

    def __str__(self):
        return self.text


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text_answer = models.CharField(max_length=300, blank=True)
    option_selections = models.ManyToManyField(Option, blank=True)


class DoneSurvey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='done_surveys')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='done_surveys')
    answers = models.ManyToManyField(Answer, related_name='done_surveys')
    objects = DoneSurveyManager()
