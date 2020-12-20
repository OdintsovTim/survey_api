import datetime

from django.db import models


class SurveyManager(models.Manager):
    def get_active_surveys(self):
        current_date = datetime.date.today()
        return self.filter(finish_date__gte=current_date)
