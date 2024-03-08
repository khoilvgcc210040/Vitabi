from django.contrib import admin
from .models import DistanceInfo, HospitalImage, Patient, Hospital, Language, Insurance, Question, Answer, Conclusion, SymptomCheckSession, FavouriteHospital

admin.site.register(Patient)
admin.site.register(Hospital)
admin.site.register(Language)
admin.site.register(Insurance)
admin.site.register(Question)

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['text', 'question']
admin.site.register(Answer, AnswerAdmin)

admin.site.register(Conclusion)
admin.site.register(SymptomCheckSession)
admin.site.register(FavouriteHospital)
admin.site.register(HospitalImage)
admin.site.register(DistanceInfo)


