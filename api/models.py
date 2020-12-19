from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Survey(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    finish_date = models.DateField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Question(models.Model):
    text = models.CharField(max_length=300)
    question_type = models.CharField(max_length=100)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')

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
