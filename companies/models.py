from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.utils.text import slugify



class Company(models.Model):
  SEVERITY = (("1", "First"), ("2", "Second"), ("3", "Third"), ("4", "Fourth"), ("5", "Fifth"), ("6", "Sixth"), ("7", "Seventh"),)
  name = models.CharField(max_length=128)
  location = models.CharField(max_length=140)
  # image = models.FileField(upload_to='company_images/')
  severity = models.CharField(choices=SEVERITY, max_length=12, default="Second")
  time = models.DateTimeField(default=timezone.now())
  user = models.ForeignKey(User, related_name="company")
  slug = models.SlugField(editable=False)

  def __str__(self):
    return self.name

  def save(self, *args, **kwargs):
    if not self.pk:
        self.slug = slugify(self.name)
    super(Company, self).save(*args, **kwargs)

  def get_absolute_url(self):
    return reverse("detail", kwargs={"company_id": self.pk, "company_slug": self.slug})


class Image(models.Model):
  file = models.FileField(upload_to='company_images/')
  time = models.DateTimeField(default=timezone.now())
  user = models.ForeignKey(User, related_name="company_image")
  company = models.ForeignKey(Company, on_delete=models.CASCADE)

  def __str__(self):
    return self.file.url
    