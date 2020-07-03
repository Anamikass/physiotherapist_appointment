from datetime import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
class state(models.Model):
    state_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.state_name


class city(models.Model):
    state_id = models.ForeignKey(state, on_delete=models.CASCADE, related_name='cities')
    city_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.city_name


class area(models.Model):
    city_id = models.ForeignKey(city, on_delete=models.CASCADE)
    area_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.area_name


class security_question(models.Model):
    que_name = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.que_name


class patient_master(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    address = models.CharField(max_length=150)
    area_id = models.ForeignKey(area, on_delete=models.CASCADE)
    city_id = models.ForeignKey(city, on_delete=models.CASCADE)
    state_id = models.ForeignKey(state, on_delete=models.CASCADE)
    dob = models.DateField()
    age = models.CharField(max_length=3)
    email = models.EmailField(max_length=50)
    ph_no = models.CharField(max_length=10)
    gender = models.CharField(max_length=6)
    image = models.ImageField(upload_to='patient/images', blank=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    security_que_id = models.ForeignKey(security_question, on_delete=models.CASCADE)
    ans = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name


class degree(models.Model):
    degree_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.degree_name


class specialization(models.Model):
    degree_id = models.ForeignKey(degree, on_delete=models.CASCADE)
    specialization_name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.specialization_name


class physio_master(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    dob = models.DateField()
    area_id = models.ForeignKey(area, on_delete=models.CASCADE)
    city_id = models.ForeignKey(city, on_delete=models.CASCADE)
    state_id = models.ForeignKey(state, on_delete=models.CASCADE)
    address = models.CharField(max_length=150)
    email = models.EmailField(max_length=50)
    ph_no = models.CharField(max_length=10)
    gender = models.CharField(max_length=6)
    image = models.ImageField(upload_to='media/physio/images/')
    degree_id = models.ForeignKey(degree, on_delete=models.CASCADE)
    specialization_id = models.ForeignKey(specialization, on_delete=models.CASCADE)
    experience = models.CharField(max_length=4)
    proof_image = models.ImageField(upload_to='physio/proof_images')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    security_que_id = models.ForeignKey(security_question, on_delete=models.CASCADE)
    ans = models.CharField(max_length=30)

    def __str__(self):
        return self.first_name


class feedback(models.Model):
    physio_id = models.ForeignKey(physio_master,on_delete=models.CASCADE)
    patient_id = models.ForeignKey(patient_master, on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.description


class contact(models.Model):
    user_name = models.CharField(max_length=30)
    ph_no = models.CharField(max_length=10)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user_name


class treatment(models.Model):
    treatment_name = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    image = models.ImageField(upload_to='physio/treatment')
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.treatment_name


class sub_treatment(models.Model):
    treatment_id = models.ForeignKey(treatment,on_delete=models.CASCADE)
    sub_treatment_name = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.sub_treatment_name


class appointment(models.Model):
    patient_id = models.ForeignKey(patient_master, on_delete=models.CASCADE)
    physio_id = models.ForeignKey(physio_master, on_delete=models.CASCADE)
    time = models.CharField(max_length=10,null=True,default='')
    date_of_appointment = models.DateField(max_length=10,null=True,default='')
    treatment_id = models.ForeignKey(treatment, on_delete=models.CASCADE)
    patient_description = models.CharField(max_length=150, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default='',null=True)
    note = models.CharField(max_length=30,default='',null=True)
    is_active = models.IntegerField(default=0,validators=[MaxValueValidator(2), MinValueValidator(0)])

    def __str__(self):
        return self.date_of_appointment


class posts(models.Model):
    physio_id = models.ForeignKey(physio_master, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=30)
    video_photo = models.CharField(max_length=500)
    treatment_id = models.ForeignKey(treatment, on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
    type=models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.post_title


class tips(models.Model):
    physio_id = models.ForeignKey(physio_master, on_delete=models.CASCADE)
    tips_title = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    treatment_id = models.ForeignKey(treatment,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.tips_title


class recruitment(models.Model):
    recruitment_title =  models.CharField(max_length=30)
    recruitment_photo = models.CharField(max_length=300,null=True)
    description = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.recruitment_title


class complaint(models.Model):
    physio_id = models.ForeignKey(physio_master,on_delete=models.CASCADE)
    patient_id = models.ForeignKey(patient_master, on_delete=models.CASCADE)
    description = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)