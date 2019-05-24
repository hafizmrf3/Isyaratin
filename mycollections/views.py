from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Q
from .models import SignLanguage, Huruf
from .forms import SignLanguageForm, HurufForm, UserForm

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

def index(request):
    if not request.user.is_authenticated():
        return render(request, 'mycollections/login.html')
    else:
        signlanguage = SignLanguage.objects.filter(user=request.user)
        huruf_results = Huruf.objects.all()
        query = request.GET.get("q")
        if query:
            signlanguage = signlanguage.filter(
                Q(name__icontains=query) |
                Q(website__icontains=query)
            ).distinct()
            huruf_results = huruf_results.filter(
                Q(huruf__icontains=query)
            ).distinct()
            return render(request, 'mycollections/index.html', {
                'signlanguage': signlanguage,
                'huruf': huruf_results,
            })
        else:
            return render(request, 'mycollections/index.html', {'signlanguage': signlanguage})


def login_user(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
          if user.is_active:
              login(request, user)
              signlanguage = SignLanguage.objects.filter(user=request.user)
              return render(request,'mycollections/index.html',{'signlanguage': signlanguage})
          else:
              return render(request, 'mycollections/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'mycollections/login.html', {'error_message': 'Invalid login'})
    return render(request, 'mycollections/login.html')


def detail(request, signlanguage_id):

    if not request.user.is_authenticated():
        return render(request, 'mycollections/login.html')
    else:
        user = request.user
        signlanguage = get_object_or_404(SignLanguage, pk=signlanguage_id)
        return render(request, 'mycollections/detail.html', {'signlanguage': signlanguage, 'user': user})


def favorite(request, huruf_id):

    huruf = get_object_or_404(Huruf, pk=huruf_id)
    try:
        if huruf.is_favorite:
            huruf.is_favorite = False
        else:
            huruf.is_favorite = True
        huruf.save()
    except (KeyError, Huruf.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def favorite_signlanguage(request, signlanguage_id):

    signlanguage = get_object_or_404(SignLanguage, pk=signlanguage_id)
    try:
        if signlanguage.is_favorite:
            signlanguage.is_favorite = False
        else:
            signlanguage.is_favorite = True
        signlanguage.save()
    except (KeyError, SignLanguage.DoesNotExist):
        return JsonResponse({'success': False})
    else:
        return JsonResponse({'success': True})


def hurufs(request, filter_by):

    if not request.user.is_authenticated():
        return render(request, 'mycollections/login.html')
    else:
        try:
            huruf_ids = []
            for signlanguage in SignLanguage.objects.filter(user=request.user):
                for huruf in signlanguage.huruf_set.all():
                    huruf_ids.append(huruf.pk)
            users_hurufs = Huruf.objects.filter(pk__in=huruf_ids)
            if filter_by == 'favorites':
                users_hurufs = users_hurufs.filter(is_favorite=True)
        except SignLanguage.DoesNotExist:
            users_hurufs = []
        return render(request, 'mycollections/hurufs.html', {
            'huruf_list': users_hurufs,
            'filter_by': filter_by,
        })


def logout_user(request):

    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'mycollections/login.html', context)


def register(request):

    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                signlanguages = SignLanguage.objects.filter(user=request.user)
                return render(request, 'mycollections/index.html', {'signlanguages': signlanguages})
    context = {
        "form": form,
    }
    return render(request, 'mycollections/register.html', context)


def create_signlanguage(request):

    if not request.user.is_authenticated():
        return render(request, 'mycollections/login.html')
    else:
        form = SignLanguageForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            signlanguage = form.save(commit=False)
            signlanguage.user = request.user
            signlanguage.logo = request.FILES['logo']
            file_type = signlanguage.logo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'signlanguage': signlanguage,
                    'form': form,
                    'error_message': 'The image must be PNG, JPG or JPEG'
                }
                return render(request, 'mycollections/create_signlanguage.html', context)
            signlanguage.save()
            return render(request,'mycollections/detail.html',{'signlanguage': signlanguage })
        context = {
            "form": form
        }
        return render(request, 'mycollections/create_signlanguage.html', context)


def create_huruf(request, signlanguage_id):

    form = HurufForm(request.POST or None, request.FILES or None)
    signlanguage = get_object_or_404(SignLanguage, pk=signlanguage_id)
    if form.is_valid():
        signlanguages_hurufs = signlanguage.huruf_set.all()
        for s in signlanguages_hurufs:
            if s.huruf == form.cleaned_data.get("huruf"):
                context = {
                    'signlanguage': signlanguage,
                    'form': form,
                    'error_message': 'Anda Sudah Menyimpan Data Huruf Tersebut !',
                }
                return render(request, 'mycollections/create_huruf.html', context)
        huruf = form.save(commit=False)
        huruf.signlanguage = signlanguage
        
        huruf.save()
        return render(request, 'mycollections/detail.html', {'signlanguage': signlanguage})
    context = {
        'signlanguage': signlanguage,
        'form': form,
    }
    return render(request, 'mycollections/create_huruf.html', context)

def edit_huruf(request, signlanguage_id):

    form = HurufForm(request.POST or None, request.FILES or None)
    signlanguage = get_object_or_404(SignLanguage, pk=signlanguage_id)
    if form.is_valid():
        signlanguages_hurufs = signlanguage.huruf_set.all()
        for s in signlanguages_hurufs:
            if s.huruf == form.cleaned_data.get("huruf"):
                context = {
                    'signlanguage': signlanguage,
                    'form': form,
                    'error_message': 'Anda sudah menyimpan data untuk SignLanguage tersebut !',
                }
                return render(request, 'mycollections/edit_huruf.html', context)
        huruf = form.save(commit=False)
        huruf.signlanguage = signlanguage
        
        huruf.save()
        return render(request, 'mycollections/detail.html', {'signlanguage': signlanguage})
    context = {
        'signlanguage': signlanguage,
        'form': form,
    }
    return render(request, 'mycollections/edit_huruf.html', context)






def delete_signlanguage(request, signlanguage_id):

    signlanguage = SignLanguage.objects.get(pk=signlanguage_id)
    signlanguage.delete()
    signlanguage = SignLanguage.objects.filter(user=request.user)
    return render(request, 'mycollections/index.html', {'signlanguage': signlanguage})


def delete_huruf(request, signlanguage_id, huruf_id):

    signlanguage = get_object_or_404(SignLanguage, pk=signlanguage_id)
    huruf = Huruf.objects.get(pk=huruf_id)
    huruf.delete()
    return render(request, 'mycollections/detail.html', {'signlanguage': signlanguage})
