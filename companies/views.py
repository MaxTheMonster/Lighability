from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.http import HttpResponse, JsonResponse

from . import models, forms

from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .mixins import LoginRequiredMixin


def validate_company(request):
  id = request.GET.get('company_id', None)
  company_query = models.Company.objects.filter(api_id__iexact=id).values()
  data = {
      'is_taken': company_query.exists(),
      'company_pk': company_query[0]["id"],
      'company_name': company_query[0]["name"],
      'company_slug': company_query[0]["slug"],
  }
  return JsonResponse(data)


class IndexView(generic.TemplateView):
  template_name = "index.html" 
  def dispatch(self, request, *args, **kwargs):
    if request.user.is_authenticated():
      return redirect("home")
    else:
      return super(IndexView, self).dispatch(request, *args, **kwargs)


class HomeView(generic.CreateView):
  template_name = "home.html"
  model = models.Image
  fields = ("file",)
  success_url = "/"

  def dispatch(self, request, *args, **kwargs):
    self.current_user = request.user
    self.company_images = []
    self.companies = models.Company.objects.filter(user__exact=self.current_user)

    for company in self.companies:
      latest_company_image = models.Image.objects.filter(company=company)[:1]
      self.company_images.append([company.pk, latest_company_image])

    if not request.user.is_authenticated():
      return redirect("index")
    else:
      return super(HomeView, self).dispatch(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super(HomeView, self).get_context_data(**kwargs)
    if self.companies.exists():
      context['companies'] = self.companies

    context['company_images'] = self.company_images
    return context

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super(HomeView, self).form_valid(form)

class AddImage(LoginRequiredMixin, generic.CreateView):
  model = models.Image
  template_name = "add_company_image.html"
  fields = ("file",)

  def dispatch(self, request, *args, **kwargs):
    self.current_company = models.Company.objects.get(pk__iexact=self.kwargs["company_id"])

    return super(AddImage, self).dispatch(request, *args, **kwargs)

  def get_success_url(self):
    return reverse('company_detail', kwargs={'company_id': self.current_company.pk, 'company_slug': self.current_company.slug})

  def form_valid(self, form):
    form.instance.company = self.current_company
    form.instance.user = self.request.user
    return super(AddImage, self).form_valid(form)

# class CheckCompanyExistance(generic.TemplateView):
#   def
#   if models.Company.objects.filter(api_id=self.cleaned_data['api_id']).exists():


class CompanyDelete(LoginRequiredMixin, generic.DeleteView):
  model = models.Company
  template_name = "confirm_company_delete.html"
  success_url = reverse_lazy("home")
  pk_url_kwarg = 'company_id'
  slug_url_kwarg = 'company_slug'

  def get_queryset(self):
    return self.model.objects.all()

class AddCompany(LoginRequiredMixin, generic.CreateView):
  form_class = forms.CompanyCreationForm
  model = models.Company
  queryset = models.Image
  template_name = "add_company.html"
  success_url = reverse_lazy("")

  def get_success_url(self):
    return reverse('company_detail', kwargs={'company_id': self.object.pk, 'company_slug': self.object.slug})

  def form_valid(self, form):
    # self.queryset = form.save()
    if models.Company.objects.filter(api_id=self.get_form()['api_id']).exists():
      print("Exists")
    form.instance.user = self.request.user
    return super(AddCompany, self).form_valid(form)



class EditCompany(LoginRequiredMixin, generic.DeleteView, generic.UpdateView):
  fields = ("severity", )
  model = models.Company
  pk_url_kwarg = 'company_id'
  slug_url_kwarg = 'company_slug'
  template_name = "update_company.html"


class CompanyDetail(generic.CreateView):
  model = models.Image
  fields = ("file",)
  success_url = "/"
  template_name = "company_detail.html"

  def get_context_data(self, **kwargs):
    context = super(CompanyDetail, self).get_context_data(**kwargs)
    context['images'] = models.Image.objects.filter(company__pk=self.kwargs["company_id"])
    # self.current_company = models.Company.objects.get(pk=self.kwargs["company_id"], slug=self.kwargs["company_slug"])
    context['company'] = models.Company.objects.get(pk=self.kwargs["company_id"], slug=self.kwargs["company_slug"])
    return context

  def form_valid(self, form, **kwargs):
    form.instance.company = models.Company.objects.get(pk=self.kwargs["company_id"], slug=self.kwargs["company_slug"])
    form.instance.user = self.request.user
    return super(CompanyDetail, self).form_valid(form)


# class AddImageToCompany(generic.CreateView):
#   model = models.Image
#   fields = ("file", )
#   success_url = reverse_lazy("company_detail", self.kwargs["company_id"], self.kwargs["company_name"])
#   template_name = "add_image.html"



class RegisterView(generic.CreateView):
  template_name = "register.html"
  form_class = forms.UserCreationForm
  success_url = "/login/"


class EditUser(LoginRequiredMixin, generic.UpdateView):
  model = models.User
  template_name = "edit_user.html"
  fields = ("profile_picture", "email")

  def get_object(self, queryset=None):
    obj = get_object_or_404(models.User.objects.filter(username=self.kwargs["username"]))
    return obj


class UserProfile(generic.DetailView):
  model = models.User
  template_name = "user_profile.html"
  context_object_name = "current_user"

  def get_object(self, queryset=None):
    user = get_object_or_404(models.User.objects.filter(username=self.kwargs["username"]))
    return user

  def dispatch(self, request, *args, **kwargs):
    self.current_user = self.get_object()

    self.company_images = []
    self.companies = models.Company.objects.filter(user__exact=self.current_user)

    for company in self.companies:
      latest_company_image = models.Image.objects.filter(company=company)[:1]
      self.company_images.append([company.pk, latest_company_image])


    return super(UserProfile, self).dispatch(request, *args, **kwargs)

  def get_context_data(self, **kwargs):
    context = super(UserProfile, self).get_context_data(**kwargs)
    context['companies'] = self.companies
    context['company_images'] = self.company_images
    return context

class LoginView(generic.FormView):
  template_name = "login.html"
  form_class = AuthenticationForm
  success_url = "/home/"

  @method_decorator(sensitive_post_parameters('password'))
  @method_decorator(csrf_protect)
  @method_decorator(never_cache)
  def dispatch(self, request, *args, **kwargs):
    if request.user.is_authenticated():
      return redirect("home")
    else:
      request.session.set_test_cookie()

      return super(LoginView, self).dispatch(request, *args, **kwargs)

  def form_valid(self, form):
    login(self.request, form.get_user())

    if self.request.session.test_cookie_worked():
      self.request.session.delete_test_cookie()

    return super(LoginView, self).form_valid(form)


class LogoutView(generic.RedirectView):
  url = "/"

  def get(self, request, *args, **kwargs):
    logout(request)
    return super(LogoutView, self).get(request, *args, **kwargs)