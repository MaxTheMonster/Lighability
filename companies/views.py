from django.shortcuts import render, redirect
from django.views import generic

from . import models

from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


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
  fields = ("file", "company")
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
    context['companies'] = self.companies
    context['company_images'] = self.company_images
    return context

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super(HomeView, self).form_valid(form)


class AddCompany(generic.CreateView):
  fields = ("name", "location", "severity")
  model = models.Company
  template_name = "add_company.html"
  success_url = "/"
 
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super(AddCompany, self).form_valid(form)


class EditCompany(generic.UpdateView):
  fields = ("name", "location", "severity")
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


class RegisterView(generic.CreateView):
  template_name = "register.html"
  form_class = UserCreationForm
  success_url = "/home/"


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