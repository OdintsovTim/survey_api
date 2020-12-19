from django.db import models


class Survey(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    finish_date = models.DateField()
    description = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Question(models.Model):
    text = description = models.CharField(max_length=300)
    response_type = models.CharField()
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.text
