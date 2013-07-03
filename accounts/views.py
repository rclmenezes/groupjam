import random
import string
import pprint
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.mail import send_mail
from django.forms.util import ErrorList
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render_to_response
from django.template import loader, Context,  RequestContext
from accounts.forms import ConfirmationCodeForm, EmailForm, LoginForm, OrganizationForm, ProfileForm, UserEditForm, UserEditModelForm
from accounts.models import RegistrationManager
from groupapp.models import UserProfile

# Makes a random string
def random_string(length):
    s = string.lowercase+string.digits+string.uppercase
    return ''.join(random.sample(s, length))

# Just an email form. If acceptable email, send confirmation email and goes to /register/confirm
# Covers two paths: 
#   1) if by / (splash page that registers a user)
#   2) if by /register (page that registers first user in organization)
def register_start(request, template):
    form = EmailForm(request.GET or None)
    if form.is_valid():
        email = form.cleaned_data["email"]
        confirmation_code = random_string(15)
        
        try:
            registrationManager = RegistrationManager.objects.get(email=email)
        except RegistrationManager.DoesNotExist:
            registrationManager = RegistrationManager(email=email, confirmation_code=confirmation_code)
            registrationManager.save()
        
        url = registrationManager.confirmation_url()
        
        template = loader.get_template('registration/confirmation_email.html')
        context = RequestContext(request, {
                'email': email, 
                'url': url, 
        })
        send_mail('[Upright] Activate your account', template.render(context), 'donotreply@uprightapp.com', [email])
        
        return HttpResponseRedirect('/accounts/register/confirm')

    c = RequestContext(request, {'form': form, 'user': request.user })
    c.update(csrf(request))
    return render_to_response(template, c)
    
# GET form that takes confirmation code, writes email and confirmation_code into session and redirects to last step. A url with the right GET variable redirects automatically.
def register_email_confirm(request):
    form = ConfirmationCodeForm(request.GET or None)
    if form.is_valid():
        try:
            registrationManager = RegistrationManager.objects.get(confirmation_code=form.cleaned_data["confirmation_code"])
            request.session['confirmation_code'] = registrationManager.confirmation_code
            return HttpResponseRedirect('/accounts/register/person?confirmation_code=' + form.cleaned_data["confirmation_code"])
        except RegistrationManager.DoesNotExist: 
            form._errors["confirmation_code"] = ErrorList([u"Couldn't find it. Are you sure you copied it correctly?"])

    c = RequestContext(request, {'form': form })
    c.update(csrf(request))
    return render_to_response('registration/confirm.html', c)
    
# You need to have email and the confirmation_code in session. Creates user and either redirects to home
# or /register/organization, depending on whether the organization is already made.
def register_person(request):

    if not 'confirmation_code' in request.session:
        raise Http404
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            confirmation_code = request.session['confirmation_code']
            try:
                registrationManager = RegistrationManager.objects.get(confirmation_code=confirmation_code)
            except RegistrationManager.DoesNotExist:
                raise Http404
            email = registrationManager.email
    
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            picture = form.cleaned_data['picture']
    
            user = User(username=email, first_name=first_name, last_name=last_name, email=email)
            user.set_password(password)
            user.save()
    
            email_domain = email.split('@')[1]
            try:
                organization = Organization.objects.get(email_domain=email_domain)
                group = organization.primary_group
            except Organization.DoesNotExist: # first user for organization
                organization = None
                group = None
        
            person = Person(user=user, organization=organization, picture=picture, group=group)
            person.save()
    
            del request.session['confirmation_code']
            registrationManager.delete()
            user = authenticate(username=email, password=password)
            login(request, user)
            return HttpResponseRedirect('/')
    else:
        form = ProfileForm()

    c = RequestContext(request, {'form': form })
    c.update(csrf(request))
    return render_to_response('registration/register_person.html', c)
        
def register_organization(request):
    email_domain = request.user.email.split('@')[1]
    name_guess = email_domain.split('.')[0].title()

    form = OrganizationForm(request.POST or None, initial={'name': name_guess})
    if form.is_valid():
        name = form.cleaned_data['name']
        group = Group(name=name)
        group.save()
        organization = Organization(name=name, email_domain=email_domain, primary_group=group)
        organization.save()
        group.organization = organization
        group.save() # I know, this is silly.
        person = Person.objects.get(user=request.user)
        person.organization = organization
        person.group = group
        person.save()
        #domain = form.clean_data['domain']
        return HttpResponseRedirect('/')
    
    c = RequestContext(request, {'form': form })
    c.update(csrf(request))
    return render_to_response('registration/register_organization.html', c)

@login_required
def edit_organization(request):
    person = Person.objects.get(user=request.user)
    
    # You don't have an organization yet? Bad. Go away and make one.
    if not person.organization:
        return HttpResponseRedirect('/')
        
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            person.organization.name = name
            person.organization.save()
            return HttpResponseRedirect('/')
    else:
        form = OrganizationForm({'name': person.organization.name})
        
    c = RequestContext(request, {'form': form })
    c.update(csrf(request))
    return render_to_response('registration/edit_organization.html', c)
    
@login_required
def edit_person(request):
    person = Person.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = UserEditForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            picture = form.cleaned_data['picture']
    
            person.user.first_name = first_name
            person.user.last_name = last_name
            person.user.save()
            person.picture = picture

            person.save()

            return HttpResponseRedirect('/')
    else:
        form = UserEditModelForm({'first_name': person.user.first_name,
                             'last_name': person.user.last_name,
                            'picture': person.picture
                            })
        #form = UserEditModelForm(instance=person)

        c = RequestContext(request, {'form': form })
        c.update(csrf(request))
        return render_to_response('registration/edit_person.html', c)

