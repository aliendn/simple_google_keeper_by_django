from django.contrib.auth import decorators
from django.contrib.auth.models import User
from django.db.models.fields import AutoField
from django.shortcuts import redirect, render
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, logout as _logout, login as _login
from django.contrib.auth.decorators import login_required
from note.models import Note
from django.views.decorators.http import require_GET, require_http_methods
from django.http import Http404



def register_user(request):
    register_form = RegisterForm(request.POST or None)

    if register_form.is_valid():
        user_name = register_form.cleaned_data.get('user_name')
        password = register_form.cleaned_data.get('password')
        email = register_form.cleaned_data.get('email')
        User.objects.create_user(username=user_name, email=email, password=password)
        return redirect('/')
    context = {
        'register_form' : register_form
    }
    return render(request, 'user/register.html', context)


def login_user(request):
    login_form = LoginForm(request.POST or None)
    if login_form.is_valid():
        user_name = login_form.cleaned_data.get('user_name')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            _login(request, user)
            return redirect('/')
        else:
            login_form.add_error('user_name', 'کاربری با مشخصات وارد شده یافت نشد')

    context = {
        'login_form': login_form
    }
    return render(request, 'user/login.html', context)


def logout(request):
    _logout(request)
    return redirect('/')


@login_required(login_url="/login")
@require_http_methods(["GET", "POST"])
def note_creator(request):
    user_username = request.user.username
    user = User.objects.get(username=user_username)
    subscribers_get = User.objects.all()
    # print(subscribers_get.username)
    if user is None:
        raise Http404('کاربر مورد نظر یافت نشد')
    if request.method == "GET":
        show_note_form = Note.objects.all()
        context = {
            'show_note_form' : show_note_form,
            'subscribers' : subscribers_get
        }
        return render(request, 'user/create.html', context)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        # subscriber_note = request.POST.get('subscribers')
        # subs = list(subscribers_get.values_list("username", flat=True))
        # subs_1 = User.objects.all()
        
        # print(subs_1.username)

        # for elm in subs.username:
        #     if subscriber_note in subs:
        #         subscriber_note = elm
        # Django value error. model field must be an instance
        # subs=User.objects.filter(username=subscriber_note)

        # subs = User.objects.filter(id,username=subscriber_note)
        # print(subs)
        
        # subs = Note.objects.get(subscribers__username=subscriber_note)
        # print(subs)

        writing_note = Note.objects.create(title=title, description = description, writer=user)
        context  = {
            'writing_note' : writing_note,
        }
        return redirect('/')


@login_required(login_url="/login")
def shownotes(request):
    user_username = request.user.username
    user = User.objects.get(username=user_username)
    subscribers = Note.objects.values_list('subscribers', flat=True)
    notes = Note.objects.all().filter(writer=user)
    context = {
        'notes' : notes
    }
    return render(request, 'user/profile.html', context)


@login_required(login_url="/login")
def edit_notes(request, id):
    user_username = request.user.username
    user = User.objects.get(username=user_username)
    note = list(Note.objects.filter(id=id, writer=user))
    subscribers_get = User.objects.all()
    if note is None:
        raise Http404('همچین نوتی یافت نشد')
    
    if request.method == "GET":
        context = {
            'note_detail' : note,
            'subscribers' : subscribers_get
        }
        return render(request, 'user/edit.html', context)
    
    elif request.method == "POST":
        title = request.POST.get('new_title')
        description = request.POST.get('new_description')
        subscribers = request.POST.get("subscribers")
        subs = User.objects.filter(username=subscribers).first()
        # subs = Note.objects.get(subscribers__username=subscribers)
        # print(subs)
        # user.subscribers=subscribers
        # user.save()
        note[0].title = title
        note[0].description = description
        # note[0].subscribers = subs.username
        note[0].save()
        # note.add(user)
        note_delete = Note.objects.get(id=id)

        note_delete.delete()

        

        context = {
            'updating_note' : note,
            'note_delete' : note_delete
        }
        return redirect('user:profile')
