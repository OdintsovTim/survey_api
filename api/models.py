import datetime

from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from .managers import SurveyManager


User = get_user_model()


class Survey(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    finish_date = models.DateField()
    description = models.CharField(max_length=200)
    objects = SurveyManager()

    def clean(self):
        if self.finish_date <= self.start_date:
            raise ValidationError('Finish date must be later than start date!')
        if self.start_date < datetime.date.today():
            raise ValidationError('You cannot create a survey retroactively')

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Survey, self).save(*args, **kwargs)

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

    text = models.CharField(max_length=300)
    question_type = models.CharField(max_length=100, default=TEXT_ANSWER, choices=QUESTION_TYPE_CHOICES)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.text



    def __str__(self):
        return self.text


class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer = models.CharField(max_length=100)


class UsersSurveyState(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='serveys_state')
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='serveys_state')
    last_question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='serveys_state')
    is_finished = models.BooleanField()
