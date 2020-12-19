from django.contrib import admin

from .models import Survey, Question


class SurveyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'start_date', 'finish_date', 'description')


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'response_type', 'survey')


admin.site.register(Survey, SurveyAdmin)
admin.site.register(Question, QuestionAdmin)
