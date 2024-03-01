from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User



class Patient(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    
    is_patient = models.BooleanField(default=True)

    fullname = models.CharField(max_length = 50)
    gender = models.BooleanField()
    dob = models.DateField()
    email = models.EmailField(max_length = 254)
    phone = models.CharField(max_length = 15)
    nationality = models.CharField(max_length = 40)
    language = models.CharField(max_length = 20)
    height = models.IntegerField(default=0)  
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    def __str__(self):
        return self.fullname

class Language(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='language_photos/', default='language_photos/default.jpg')

    def __str__(self):
        return self.name

class Insurance(models.Model):
    name = models.CharField(max_length=255)
    website_link = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='insurance_photos/', blank=True, null=True)

    def __str__(self):
        return self.name

class Hospital(models.Model):
    def get_current_time():
        return timezone.now().time()
    
    name = models.CharField(max_length=255, null=True, blank=True)
    working_time = models.CharField(max_length=255, null=True, blank=True)
    supported_languages = models.ManyToManyField(Language)
    supported_insurance = models.ManyToManyField(Insurance, blank=True)
    address = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=50, null=True, blank=True)
    direct_billing = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class HospitalImage(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='images')
    photo = models.ImageField(upload_to='hospital_photos/')

    def __str__(self):
        return f"{self.hospital.name}"

class Question(models.Model):
    text = models.TextField()
    is_first_question = models.BooleanField(default=False, help_text="Choose to ask this question as the first question.")

    def save(self, *args, **kwargs):
        if self.is_first_question:
            Question.objects.filter(is_first_question=True).update(is_first_question=False)
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.text
    
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    likelihood_ratio = models.FloatField(null=True, blank=True, help_text="Likelihood ratio for this answer if applicable.")
    next_question = models.ForeignKey(Question, on_delete=models.SET_NULL, null=True, blank=True)
    is_conclusive = models.BooleanField(default=False)
    conclusion_text = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.text} (Question: {self.question.text})"
    
class Conclusion(models.Model):
    text = models.TextField()
    odds_condition = models.CharField(max_length=10, choices=[('>=1', 'Odds >= 1'), ('<1', 'Odds < 1')])
    answers = models.ManyToManyField(Answer, related_name='conclusions')
    
    def __str__(self):
        return self.text
    
class SymptomCheckSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='symptom_sessions')
    created_at = models.DateTimeField(auto_now_add=True)
    conclusion_text = models.TextField()
    odds_percentage = models.TextField()
    id_conclusion = models.TextField(default=0)
    
    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"


class FavouriteHospital(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourite_hospitals')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='favourited_by')
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'hospital')
        verbose_name_plural = 'Favourite Hospitals'

    def __str__(self):
        return f"{self.user.username} - {self.hospital.name}"


    



