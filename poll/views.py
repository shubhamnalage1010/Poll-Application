from django.http import HttpResponse
from django.shortcuts import render, redirect 
from .forms import CreatePollForm, NewUserForm
from .models import Poll
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout

# Create your views here.

def register_view(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("/")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request, "poll/register.html", context={"crispy_form":form})

def login_view(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request, "poll/login.html", context={"crispy_form":form})


def logout_view(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/login/")

def home(request):
    polls = Poll.objects.all()
    context = {'polls' : polls}
    return render(request, 'poll/home.html', context)


def create(request):
    if request.method == 'POST':
        form = CreatePollForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = CreatePollForm()
    context = {'form' : form }
    return render(request, 'poll/create.html', context)



def vote(request, poll_id):
    poll  = Poll.objects.get(pk = poll_id)
    if request.method == 'POST':
        selected_option = request.POST['poll']
        if selected_option == 'option1':
            poll.option_one_count += 1
        elif selected_option == 'option2':
            poll.option_two_count += 1
        elif selected_option == 'option3':
            poll.option_three_count += 1
        else:
                return HttpResponse(400, 'Invalid')
        
        poll.save()
        return redirect('results', poll_id)
        
    context = {'poll' : poll}
    return render(request, 'poll/vote.html', context)


def results(request, poll_id):
    poll = Poll.objects.get(pk = poll_id)
    context = { 'poll' : poll}
    return render(request, 'poll/results.html', context)
