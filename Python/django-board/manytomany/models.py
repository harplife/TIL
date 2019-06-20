from django.db import models

# Create your models here.
'''
python manage.py shell_plus
>> doctor = Doctor.objects.create(name='morpheous')
>> patient = Patient.objects.create(name='neo')
>> doctor.patients.add(patient)
>> doctor.patients.all()
<QuerySet [<Patient: 1번 환자 : neo>]>
>> patient.doctors.all()
<QuerySet [<Patient: 1번 의사 : morpheous>]>
>> patient.doctors.remove(doctor)
>> patient.doctors.all()
<QuerySet []>
>> doctor.patients.all()
<QuerySet []>

참고: DB를 비울려면 migrations> __init__.py 제외 모두 지우고, 프로젝트 경로 밑에 db.sqlite3 파일도 지워야 된다.
'''


class Doctor(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.id}번 의사 : {self.name}"


class Patient(models.Model):
    name = models.CharField(max_length=20)
    # patient.doctors.all()
    doctors = models.ManyToManyField(
        Doctor,
        # through='Reservation',  # Reservation이란 중계 DB가 있으면!
        related_name='patients'  # doctor.patients.all()
    )

    def __str__(self):
        return f"{self.id}번 환자 : {self.name}"

