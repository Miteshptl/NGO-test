from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Extended User model
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
        ('volunteer', 'Volunteer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='volunteer')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

# Contact model
class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

# Media model
class Media(models.Model):
    MEDIA_TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
        ('document', 'Document'),
    )
    title = models.CharField(max_length=100)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    file = models.FileField(upload_to='media/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Blog model
class Blog(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    content = models.TextField()
    image = models.ImageField(upload_to='blogs/', blank=True, null=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title

# Project model
class Project(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

# Donation model
class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)

    def __str__(self):
        return f"Donation of ₹{self.amount}"

# OurWork model
class OurWork(models.Model):
    title = models.CharField(max_length=150)
    summary = models.TextField()
    image = models.ImageField(upload_to='ourwork/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Dashboard model (user-specific summary info)
def get_default_user():
    return User.objects.first().id

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE,default=get_default_user)  
#     full_name=models.CharField(max_length=50)
#     gender_choices=(("Male","Male"),("Female","Female"),("Other","Other"))
#     gender=models.CharField(max_length=50,choices=gender_choices)
#     date_of_birth=models.DateField()
#     mobile_number=models.CharField(max_length=10)
#     email=models.CharField(max_length=50)
#     address=models.TextField()
#     image=models.ImageField(upload_to="./profile/images/")
#     def __str__(self):
#         return self.full_name

# Task model
class Task(models.Model):
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class Admin_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=get_default_user)  
    full_name=models.CharField(max_length=50)
    gender_choices=(("Male","Male"),("Female","Female"),("Other","Other"))
    gender=models.CharField(max_length=50,choices=gender_choices)
    date_of_birth=models.DateField()
    mobile_number=models.CharField(max_length=10)
    email=models.CharField(max_length=50)
    address=models.TextField()
    image=models.ImageField(upload_to="./profile/images/")
    def __str__(self):
        return self.full_name
    
class Emp_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=get_default_user)  
    full_name=models.CharField(max_length=50)
    gender_choices=(("Male","Male"),("Female","Female"),("Other","Other"))
    gender=models.CharField(max_length=50,choices=gender_choices)
    date_of_birth=models.DateField()
    mobile_number=models.CharField(max_length=10)
    email=models.CharField(max_length=50)
    address=models.TextField()
    image=models.ImageField(upload_to="./profile/images/")
    def __str__(self):
        return self.full_name
    
class Vol_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,default=get_default_user)  
    full_name=models.CharField(max_length=50)
    gender_choices=(("Male","Male"),("Female","Female"),("Other","Other"))
    gender=models.CharField(max_length=50,choices=gender_choices)
    date_of_birth=models.DateField()
    mobile_number=models.CharField(max_length=10)
    email=models.CharField(max_length=50)
    address=models.TextField()
    image=models.ImageField(upload_to="./profile/images/")
    def __str__(self):
        return self.full_name