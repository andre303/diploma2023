"""
Page controllers.

Application: trips
"""

from trips.admin import GuideAdmin
from trips.statistic import addBooking, addLogin, addRegister
from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect,Http404,FileResponse
from django.contrib.auth import authenticate, login, logout, views 
from .models import *
from .forms import *
from django.core.paginator import Paginator
from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from cloudinary.forms import cl_init_js_callbacks
import cloudinary
import cloudinary.uploader
import cloudinary.api
import json
import base64

def list(request, location_slug=None, country_slug=None):
    """
    Page with list of trips/guides, search results page.
    """
    query = request.GET.get("query", "")
    location = None
    if location_slug:
        location = Location.objects.get(slug=location_slug)

    country = None
    if country_slug:
        country = Country.objects.get(slug=country_slug)

    items = Guide.objects.filter(active=True)

    if country:
        items = items.filter(country=country)
    if location:
        items = items.filter(locations=location)
    if query:
        items = items.filter(index__icontains=query)
    paginator = Paginator(items, 5) 
    page_number = 1
    if request.method == "GET":
     page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"country": country, "location": location, "query": query, "items": page_obj}
    return render(request, "list.html", context)
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
def live_search(request):
    if is_ajax(request=request) and request.method == "GET":
        response = {}
        i = 0
        query = request.GET.get("query")
        items = Location.objects.filter(name__icontains = query or None)
        if items:
            for item in items:
                response.update({i:item.name})
                i += 1
        items = Location.objects.filter(slug__icontains = query or None)
        if items:
            for item in items:
                response.update({i:item.name})
                i += 1
        items = Region.objects.filter(slug__icontains = query or None)
        if items:
            for item in items:
                response.update({i:item.name})
                i += 1
        items = Region.objects.filter(name__icontains = query or None)
        if items:
            for item in items:
                response.update({i:item.name})
                i+=1
        items = Country.objects.filter(name__icontains = query or None)
        if items:
            for item in items:
                response.update({i:item.name})
                i += 1
        items = Country.objects.filter(slug__icontains = query or None)
        if items:
            for item in items:
                response.update({i:item.name})
                i += 1
    return JsonResponse(response)

def detail(request, trip_id):
    """
    Trip / guide detail page
    """
    item = get_object_or_404(Guide, pk=trip_id)
    items = Guide.objects.filter(featured = True) 
    reviews = item.review_set.all().order_by('-created')
    paginator = Paginator(reviews, 5) 
    if request.method == "GET" and is_ajax(request=request):
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        data = {}
        i = 0
        for obj in page_obj:
            data[i] = {'name':obj.user_name,
            'date':obj.created,
            'rate':obj.rating,
            'text':obj.text
            }
            i = i + 1
        return JsonResponse(data)
    page_obj = paginator.get_page(1)
    if request.method == "POST":
        item = get_object_or_404(Guide, pk=trip_id)
        form = BookingForm(request.POST)
        if form.is_valid() and item:
            book = form.save()
            if request.user.is_authenticated:
                book.user = request.user
            book.trip = item
            book.save()
            addBooking()
            return render(request,"success_message.html",{'success_message':'Гід отримав вашу заявку! Ви можете перевірити стан бронювання у себе в профілі'})
        else:         
            context = {"item": item, "items": items,"BookingForm":form,"reviews":page_obj}
            return render(request, "detail.html", context)
    form = BookingForm()
    if request.user.is_authenticated:
        form.initial["user_name"] = request.user.first_name + " " + request.user.last_name
    context = {"item": item, "items": items,"BookingForm":form,"reviews":page_obj}
    return render(request, "detail.html", context)

def review(request, trip_id):
    item = get_object_or_404(Guide, pk=trip_id)
    items = []  # related items
    context = {"item": item, "items": items,"user":"","review_text":"","rating":""}
    if Review.objects.filter(user_name = request.user, trip = item):
        return HttpResponseRedirect("/trip/"+str(trip_id)+"/")
    if request.method == "POST":
        context["review_text"] = request.POST.get("review_text");
        context["rating"] = request.POST.get("rating_field");
        
        Review.objects.create(
            user_name = request.user,
            trip = Guide.objects.get(pk=trip_id),
            text = context["review_text"],
            rating =  context["rating"]
        )
    return HttpResponseRedirect("/trip/"+str(trip_id)+"/")

def register(request):
    """
    Register as a guide page
    """
    return render(request, "register.html")

def social_login(request):
    if request.user.is_authenticated:
        if abs(request.user.date_joined - request.user.last_login).seconds < 20:
            addRegister()
            mail_subject = 'Вітаємо в TravelFindo'
            message = render_to_string('email_templates/greetings_email.html', {
                    'user': request.user,
                        })
            to_email = request.user.email
            email = EmailMessage( mail_subject, message, to=[to_email]  )
            email.content_subtype = "html"
            email.send()
            if request.COOKIES.get('type', 'default') == "guide":
                return HttpResponseRedirect('/guide_register/?type=new_user')
            else:
                return HttpResponseRedirect('/profile/?type=First')
        addLogin()
    return HttpResponseRedirect('/')

def agent(request):
    return render(request, "agent.html")

def guide_register(request):
    # context = {"locations": Location.objects.all(),"languages":Language.objects.all(),"currencys":Currency.objects.all(),"regions":Region.objects.all()}
    if request.user.is_authenticated and not Guide.objects.filter(user = request.user).exists():
        context = {"form":None,"isNew":False}
        if request.method == "GET":
            if request.GET.get("type") == "new_user":
             context["isNew"] = True
        if not request.method == "POST":
            context["form"] = GuideRegisterForm()
            return render(request,'guide_register_form.html', context)
        else:  
            context["form"] = GuideRegisterForm(request.POST)
            if context["form"].is_valid():
                new_guide = context["form"].save()
                new_guide.user = request.user
                new_guide.save()
            else:
                return render(request,'guide_register_form.html',context)
    # return render(request,"success_message.html",{"success_message":"Ваша заявка відправлена на оброблення"})
    return HttpResponseRedirect('/profile/')

def profile(request,form=None):
    if request.user.is_authenticated == True:
        if Guide.objects.filter(user=request.user):
            return guide_profile(request)
        else:
            return tourist_profile(request)
    else:
        return render(request,"index.html")

def guide_profile(request):
    imageForm = ChangeImageForm()
    item = Guide.objects.get(user=request.user)
    if not request.method == "POST":
        form = GuideProfileForm(instance=item)
    else:
        form = GuideProfileForm(request.POST,instance=item)
        if form.is_valid():
            form.save()
    return render(request, "guide_profile.html",{'item':item,'form':form,'imageForm':imageForm})

def change_photo(request):
    if request.user.is_authenticated and Guide.objects.filter(user = request.user).exists():
        item = Guide.objects.get(user=request.user)
        if request.method == "POST":
            Photoform = ChangeImageForm(request.POST or None, request.FILES or None, instance = item)
            if Photoform.is_valid():
                if item.image:
                    cloudinary.uploader.destroy(item.image.public_id,invalidate=True)
                item.image = request.FILES['file']
                item.save()
                return JsonResponse({"success":item.image.url})
            return JsonResponse({"error":"validationError"})
        return JsonResponse({"error":"No Data"})
    return JsonResponse({"error":"user not authenticated or user is not guide"})

def tourist_profile(request):
    context = {"form":None,"Message":""}
    if not request.method == "POST":
        form = TouristProfileForm(initial=dict(
        username = request.user.username or None,
        first_name = request.user.first_name or None,
        last_name = request.user.last_name or None)) 
    else:
        form = TouristProfileForm(request.POST)
        if form.is_valid():
            tourist = User.objects.get(pk = request.user.pk)
            tourist.username = form.cleaned_data['username']
            tourist.first_name = form.cleaned_data['first_name']
            tourist.last_name = form.cleaned_data['last_name']
            tourist.save()
    if request.method == "GET":
        if request.GET.get("type") == "First":
         context["Message"] = "Дякуємо за реєстрацію, гарних подорожей"
    context["form"] = form 
    return render(request, "tourist_profile.html",context)

def tourist_profile_edit(request):
    if request.method == "POST":
        form = TouristProfileForm(request.POST)
        if not form.is_valid():
            #  reverse(profile(request,form=form))
            return HttpResponseRedirect("/profile/")



def bookings_list(request):
    if request.user.is_authenticated:
        if Guide.objects.filter(user=request.user):
            # items = sorted(Booking.objects.filter(trip = Guide.objects.get(user=request.user),preferredDate__gt = datetime.today() ), key = lambda Booking: Booking.preferredDate)
            items = sorted(Booking.objects.filter(trip = Guide.objects.get(user=request.user),preferredDate__gt = datetime.today() ), key = lambda Booking:(False if Booking.isCanceled == False and Booking.isConfirmed == False else True, Booking.preferredDate))
            context = {"list":items,"type":"guide"}
            return render(request,"booking_list.html", context)
        else:
            items = sorted(Booking.objects.filter(user = request.user, preferredDate__gt = datetime.today() ), key = lambda Booking: Booking.preferredDate)
            context = {"list":items,"type":"tourist"}
            return render(request,"booking_list.html",context)
    return render(request,"index.html")

def bookings_archive(request):
     if request.user.is_authenticated:
        if Guide.objects.filter(user=request.user):
            items = sorted(Booking.objects.filter(trip = Guide.objects.get(user=request.user),preferredDate__lt = datetime.today() ), key = lambda Booking: Booking.preferredDate)
            context = {"list":items,"type":"guide"}
            return render(request,"booking_archive.html", context)
        else:
            items = sorted(Booking.objects.filter(user = request.user, preferredDate__lt = datetime.today() ), key = lambda Booking: Booking.preferredDate)
            context = {"list":items,"type":"tourist"}
            return render(request,"booking_archive.html",context)
     return render(request,"index.html")

def confirm_booking(request, book_id):
     if request.user.is_authenticated:
        if Guide.objects.filter(user=request.user):
            if Booking.objects.get(pk = book_id).trip == Guide.objects.get(user=request.user):
                item = Booking.objects.get(pk = book_id)
                item.isCanceled = False
                item.isConfirmed = True
                item.save()
                current_site = get_current_site(request)
                mail_subject = 'Підтвердження бронювання.'
                message = render_to_string('email_templates/confirm_booking_email.html', {
                        'name': item.trip.name,
                        'url': current_site,
                        'trip_pk':item.trip.pk,
                        })
                to_email = item.user.email
                email = EmailMessage(
                                mail_subject, message, to=[to_email]
                        )
                email.content_subtype = "html"
                email.send()
                return HttpResponseRedirect('/booking_list/')
     return render(request,"index.html")

def cancel_booking(request):
    if request.method == "POST":
        item = Booking.objects.get(pk = request.POST.get('trip_pk') or None)
        if request.user.is_authenticated and item:
            if Guide.objects.filter(user=request.user):
                if item.trip == Guide.objects.get(user=request.user):
                    item.cancel_message = request.POST.get('cancel-reason')
                    item.isCanceled = True
                    item.isConfirmed = False
                    item.save()
                    mail_subject = 'Відміна бронювання.'
                    message = render_to_string('email_templates/cancel_booking_email.html', {
                        'name': item.trip.name,
                        'reason':item.cancel_message,

                        })
                    to_email = item.user.email
                    email = EmailMessage(
                                mail_subject, message, to=[to_email]
                        )
                    email.content_subtype = "html"
                    email.send()
                    return HttpResponseRedirect('/booking_list/')
            elif item.user == request.user:
                item.cancel_message = request.POST.get('cancel-reason')
                item.isCanceled = True
                wasConfirmed = item.isConfirmed
                item.isConfirmed = False
                item.save()
                if wasConfirmed:
                    mail_subject = 'Відміна бронювання.'
                    message = render_to_string('email_templates/cancel_booking_email.html', {
                        'name': item.user_name,
                        'reason':item.cancel_message,

                        })
                    to_email = item.trip.user.email
                    email = EmailMessage(
                                mail_subject, message, to=[to_email]
                        )
                    email.content_subtype = "html"
                    email.send()
                return HttpResponseRedirect('/booking_list/')
    return render(request,"index.html")

def email_register(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = RegisterForm(request.POST)
            if form.is_valid():
               user = form.save()
               user.is_active = False
               user.set_password(form.cleaned_data.get('password'))
               user.save()
               current_site = get_current_site(request)
               mail_subject = 'Активуйте ваш аккаунт.'
               message = render_to_string('email_templates/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
                'type':request.COOKIES["type"]
                })
               to_email = form.cleaned_data.get('email')
               email = EmailMessage(
                        mail_subject, message, to=[to_email]
                )
               email.content_subtype = "html"
               email.send()
               addRegister()
               return render(request,'success_message.html',{"success_message":'На вашу електронну пошту було вислано повідомлення з посиланням для підтвердження'})
            else:
                return render(request,"index.html",{"RegisterForm":form})
    else:
        return render(request,"error_message.html",{"error":"Ви авторизовані"})

    return render(request, "booking_finish.html", context)

def activate(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        if request.GET.get("type") == "guide":
            return HttpResponseRedirect('/guide_register/')
        return render (request,'success_message.html',{"success_message":'Дякуємо за реєстрацію. Насолоджуйтесь подорожами!'})
    else:
        return render (request,'error_message.html',{"error":'Activation link is invalid!'})

def password_recover(request):
    if not request.user.is_authenticated:
        if not request.method == "POST":
         form = PasswordRecoveryForm()
         return render(request,"password_recovery.html",{"PasswordRecoveryForm":form})
        else:
            form = PasswordRecoveryForm(request.POST)
            if form.is_valid():
                user = get_object_or_404(User, email= form.cleaned_data['email'])
                current_site = get_current_site(request)
                mail_subject = 'Відновлення паролю.'
                message = render_to_string('email_templates/password_recovery_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                    'token':account_activation_token.make_token(user),
                    })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                    )
                email.content_subtype = "html"
                email.send()
                return render(request,'success_message.html',{"success_message":'На вашу електронну пошту було вислано повідомлення з посиланням для підтвердження'})
            else:
                return render(request,"password_recovery.html",{"PasswordRecoveryForm":form})
    return render(request,"error_message.html",{"error":"Ви авторизовані"})

def recover(request, uidb64, token, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        login(request, user, backend='django.contrib.auth.backends.ModelBackend') 
        return HttpResponseRedirect("/change_password/")
    else:
        return render (request,'error_message.html',{"error":'Recovey link is invalid!'})

def change_password(request):
    if request.user.is_authenticated:
     if not request.method == "POST":
        form = ChangePassword()
        return render(request,"passwordChanging.html",{"ChangeForm":form})
     else:
        form = ChangePassword(request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data.get('password'))
            request.user.save()
            return render (request,'success_message.html',{"success_message":'Ваш пароль успішно змінено!'})
        else:
            return render(request,"passwordChanging.html",{"ChangeForm":form})
    else:
        return render (request,'error_message.html',{"error":'Ви не авторизовані'})

def email_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get("log-email")
            password = request.POST.get("log-password")
            if(User.objects.filter(username = username).exists()):
                if(not User.objects.get(username = username).is_active):
                    return render(request,"error_message.html",{"error":"Підтвердіть вашу пошту"})
            if(User.objects.filter(email = username).exists()):
                if(not User.objects.get(email = username).is_active):
                    return render(request,"error_message.html",{"error":"Підтвердіть вашу пошту"})        
            user = authenticate(request, username=username, password=password)
            if user is not None:
                addLogin()
                login(request,user)
                return HttpResponseRedirect("/")
                # return render(request,"index.html")
            else:
                if User.objects.filter(email = username).exists():
                    username = User.objects.get(email = username)
                    user = authenticate(request, username=username, password=password)
                    if user is not None:
                      addLogin()
                      login(request,user)
                      return HttpResponseRedirect("/")
            return render(request,"error_message.html",{"error":"Неправильний логін або пароль"})
    return render(request,"error_message.html",{"error":"Ви авторизовані"})

def feedback(request):
    
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
         form.save()
         return render(request,"success_message.html",{"success_message":"Дякуємо, ваші відгуки дуже важливі для нас"})
        return render(request,"feedback.html",{"FeedbackForm":form})
    form = FeedbackForm()
    return render(request,"feedback.html",{"FeedbackForm":form})

def addToSaved(request):
    if request.user.is_authenticated and  is_ajax(request=request) and request.method == "POST":
        saved = SavedGuides.objects.filter(user = request.user).first()
        if not saved:
            saved = SavedGuides.objects.create(user = request.user)
        trip_pk = request.POST.get("trip_pk")
        item = Guide.objects.filter(pk = trip_pk).first()
        if saved.guides.filter(pk = trip_pk ).exists():
            return JsonResponse({"result":"already in"})
        if saved and item:
            saved.guides.add(item)
            saved.save()
            return JsonResponse({"result":"success"})
        return JsonResponse({"result":"wrong item"})
    if not  request.user.is_authenticated:
        return JsonResponse({"result":"not authenticated"})
    if not is_ajax(request=request):
        return JsonResponse({"result":"not ajax"})
    if not request.method == "POST":
        return JsonResponse({"result":"not POST"})

def removeFromSaved(request):
    if request.user.is_authenticated and  is_ajax(request=request) and request.method == "POST":
        saved = SavedGuides.objects.filter(user = request.user).first()
        if not saved:
            return JsonResponse({"result":"error"})
        trip_pk = request.POST.get("trip_pk")
        item = Guide.objects.filter(pk = trip_pk).first()
        if saved.guides.filter(pk = trip_pk ).exists() and item:
            saved.guides.remove(item)
            return JsonResponse({"result":"success"})
        return JsonResponse({"result":"error"})
    if not  request.user.is_authenticated:
        return JsonResponse({"result":"not authenticated"})
    if not is_ajax(request=request):
        return JsonResponse({"result":"not ajax"})
    if not request.method == "POST":
        return JsonResponse({"result":"not POST"})

def savedGuides(request):
    if request.user.is_authenticated:
        items,created = SavedGuides.objects.get_or_create(user = request.user)
        items = items.guides.all()
        return render(request,"savedGuides.html",{"items":items})

def policy(request):
    try:
        return FileResponse(open('trips/static/pdf/private_policy.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()

def custom_agreement(request):
    try:
        return FileResponse(open('trips/static/pdf/Koristuvatska-ugoda.pdf', 'rb'), content_type='application/pdf')
    except FileNotFoundError:
        raise Http404()

def base64_url_decode(s):
    return base64.urlsafe_b64decode(s.encode("utf-8") + '=' * (4 - len(s) % 4))

def parseSignedRequest(signed_request):
    # secret = "82b7a3a963bcb705e5ff82b492798046"
    
    try:
        (encoded_sig, payload) = signed_request.split(".", 2)
    except IndexError:
        raise ValueError("Signed Request is malformed")
    
    # sig = base64_url_decode(encoded_sig)
    data = json.loads(base64_url_decode(payload))
    
    return data
def deleteProfile(request):
    if request.user.is_authenticated and request.method == "POST":
        if request.POST.get('isSure') == 'on':
            user = User.objects.filter(id = request.user.id).first() 
            guide = Guide.objects.filter(user = user).first()
            if guide:
                guide.active = False
                guide.save()
            user.delete()
            user.save()
            logout(request)
            return render(request,"deleteProfile.html",{"Message":"Ми будемо сумувати за вами =("})
    return render(request,"deleteProfile.html")
def facebook_deletion(request):
    return render(request,"deleteProfile.html")