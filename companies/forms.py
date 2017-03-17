from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

class UserCreationForm(UserCreationForm):
  email = forms.EmailField(label = "Email")
  profile_picture = forms.FileField(label = "Profile Picture")

  class Meta:
      model = User
      fields = ("username", "profile_picture", "email", )