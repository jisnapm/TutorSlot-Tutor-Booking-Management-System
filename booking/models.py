from django.db import models

# Create your models here.

class TutorDB(models.Model):
    tutor_name = models.CharField(max_length=50)
    subject = models.CharField(max_length=100)
    experience = models.PositiveIntegerField()
    hourly_rate = models.PositiveIntegerField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.tutor_name


class StudentDB(models.Model):
    student_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    tutor_id = models.IntegerField()
    course = models.CharField(max_length=100)
    class_date = models.DateField()
    class_token = models.PositiveIntegerField(editable=False, null=True)
    class_time = models.TimeField(editable=False, null=True)
    status = models.CharField(max_length=50, default="pending")
    remarks = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.student_name