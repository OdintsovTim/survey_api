import datetime

from django.db import models


class SurveyManager(models.Manager):
    def get_active_surveys(self):
        current_date = datetime.date.today()
        return self.filter(finish_date__gte=current_date)


class DoneSurveyManager(models.Manager):
    def get_own_done_surveys(self, user):
        return self.filter(user__id=user.id)
