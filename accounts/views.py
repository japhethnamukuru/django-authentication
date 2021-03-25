from django.shortcuts import render, redirect

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth.models import User 

from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .forms import SignUpForm, ProfileForm, UserEditForm
from .models import Profile


#default homepage view
def default_home_view(request):
	return render(request, 'index.html')


#user login view
@login_required
def car_index(request):
	return render(request, 'cars/car_index.html', {'section': 'index'}) 

#user registration
@transaction.atomic
def signup(request):
    if request.method == 'POST':
        user_form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()

            # load the Profile created by the Signal
            user.refresh_from_db()

            # Reload the profile form with the profile instance
            profile_form = ProfileForm(request.POST, instance=user.profile)

            # Manually clean the form this time. It is implicitly called by "is_valid()" method 
            profile_form.full_clean()

            # save the form  
            profile_form.save()

            current_site = get_current_site(request)
            email_subject = 'Activate your account'
            message = render_to_string('registration/account_activation_email.html',  {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user_form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()

            return render(request, 'registration/email_sent.html')
            
            
    else:
        user_form = SignUpForm()
        profile_form = ProfileForm()
    return render(request, 'registration/signup.html', {
        'user_form': user_form        
    })


#profile edit
@login_required
def profile_edit(request):
	if request.method == 'POST':
		user_form = UserEditForm(instance=request.user, data=request.POST)
		profile_form = ProfileForm(instance=request.user.profile, data=request.POST, files=request.FILES)

		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			profile_form.save()

			return render(request, 'registration/profile_edit_success.html')

	else:
		user_form = UserEditForm(instance=request.user)
		profile_form = ProfileForm(instance=request.user.profile)

	return render(request, 'registration/profile.html', {'user_form': user_form, 'profile_form': profile_form})


#account activation
def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'registration/activation_success.html')
    else:
        return HttpResponse('Activation link is invalid!')	
