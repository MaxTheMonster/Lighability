from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User, Company

class UserCreationForm(UserCreationForm):
  email = forms.EmailField(label = "Email")
  profile_picture = forms.FileField(label = "Profile Picture", required=False)

  class Meta:
      model = User
      fields = ("username", "profile_picture", "email",)

class CompanyCreationForm(forms.ModelForm):
  address = forms.CharField(widget=forms.HiddenInput())
  lat = forms.CharField(widget=forms.HiddenInput())
  lng = forms.CharField(widget=forms.HiddenInput())
  foursquare_id = forms.CharField(widget=forms.HiddenInput())
  country = forms.CharField(widget=forms.HiddenInput())
  city = forms.CharField(widget=forms.HiddenInput())
  name = forms.CharField(widget=forms.HiddenInput())

  class Meta:
    model = Company
    fields = ("severity","name", "address", "lat", "lng", "foursquare_id", "country", "city",)