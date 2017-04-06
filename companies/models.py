import os

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.text import slugify
from django.core.validators import RegexValidator

from Lighability.settings import STATIC_URL


class User(AbstractUser):
  username = models.CharField(
          max_length=20,
          unique=True,
          validators=[RegexValidator(
                regex='^(?=.{3,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$',
                message='Your username must be between 3-20 characters long, cannot have a _ or . at the beginning or end and cannot have a __ or _. or ._ or .. inside.',
            ),
          ],
          error_messages={
              'unique': ("A user with that username already exists."),
          },
      )
  points = models.IntegerField(default=1)
  profile_picture = models.FileField(upload_to='profile_pictures/', default="../static/img/profile.jpg")

  def get_absolute_url(self):
    return reverse("user_profile", kwargs={"username": self.username})

class Company(models.Model):
  SEVERITY = (("1", "First"), ("2", "Second"), ("3", "Third"), ("4", "Fourth"), ("5", "Fifth"), ("6", "Sixth"), ("7", "Seventh"),)
  name = models.CharField(max_length=128)
  address = models.CharField(max_length=140)
  api_id = models.CharField(max_length=200, unique=True)
  lng = models.CharField(max_length=50)
  lat = models.CharField(max_length=50)
  severity = models.CharField(choices=SEVERITY, max_length=12, default="Second")
  time = models.DateTimeField(default=timezone.now)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="company")
  slug = models.SlugField(editable=False)

  def __str__(self):
    return self.name

  def save(self, *args, **kwargs):
    if not self.pk:
        self.slug = slugify(self.name)
    super(Company, self).save(*args, **kwargs)

  def get_absolute_url(self):
    return reverse("company_detail", kwargs={"company_id": self.pk, "company_slug": self.slug})


class Image(models.Model):
  file = models.FileField(upload_to='company_images/')
  time = models.DateTimeField(default=timezone.now)
  user = models.ForeignKey(User, related_name="company_image")
  company = models.ForeignKey(Company, on_delete=models.CASCADE)

  def __str__(self):
    return self.file.url
    