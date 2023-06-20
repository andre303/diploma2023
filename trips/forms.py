from django import forms
from django.db.models.fields import TimeField
from django.forms import fields,ModelForm
from django.forms import widgets
from django.forms.widgets import EmailInput, FileInput, PasswordInput, TimeInput, Widget
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset
import re


class TouristProfileForm(forms.Form):
    username = forms.CharField(min_length=2,max_length = 30,widget=forms.TextInput(attrs={"class":"form-control"}))
    first_name = forms.CharField(min_length=2,max_length = 30,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name = forms.CharField(min_length=1,max_length = 30,widget=forms.TextInput(attrs={"class":"form-control"}))
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["username"].label="Логін"
        self.fields["first_name"].label="Ім'я"
        self.fields["last_name"].label="Прізвище"


    def clean_first_name(self):
        first_name = self.cleaned_data["first_name"]
        if re.search("[\d.,:\$]",first_name):
            raise forms.ValidationError(f'Ім\'я не може містити цифри або спеціальні символи',
            code="Invalid name")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data["last_name"]
        if re.search("[\d.,:\$]",last_name):
            raise forms.ValidationError(f'Фамілія не може містити цифри або спеціальні символи',
            code="Invalid name")
        return last_name
    def clean_username(self):
        username = self.cleaned_data['username']
        if re.search("[.,:\$]",username):
            raise forms.ValidationError(f'Логін не може містити цифри або спеціальні символи',
            code="Invalid name")
        if User.objects.filter(username = username).exists():
             raise forms.ValidationError(f'Користувач з таким логіном вже існує',
            code="Invalid name")
        return username

class GuideRegisterForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(GuideRegisterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Зареєструватись', css_class='btn-primary'))
        self.helper.add_input(Reset('reset', 'Відмінити', css_class='btn-secondary'))
        for field in self.fields:
            self.fields[field].required = True
        
        self.fields['phone2'].required = False
        self.fields['facebook'].required = False
        self.fields['instagram'].required = False
        self.fields['telegram'].required = False
        self.fields['whatsapp'].required = False
        self.fields['skype'].required = False
    def clean_name(self):
        name = self.cleaned_data["name"]
        if re.search("[\d.,:\$]",name):
              raise forms.ValidationError(f'Ім\'я не може містити цифри або спеціальні символи',
                code="Invalid name")
        return name
    def clean_youtube_video_url(self):
        yt_url = self.cleaned_data["youtube_video_url"]
        if not re.search("(vi\/|v=|\/v\/|youtu\.be\/|\/embed\/)",yt_url):
            raise forms.ValidationError(f'Неправильне посилання',
                code="Invalid name")
        # print(re.split("(vi\/|v=|\/v\/|youtu\.be\/|\/embed\/)",yt_url))
        return yt_url
    class Meta:
        model = Guide
        exclude = ['user','active','featured','image','index','confirmed']

        labels = {
            'region': 'Область',
            'name':'Ім\'я',
            'locations':'Локації',
            'description':'Опис',
            'languages':'Мови',
            'price':'Ціна',
            'currency':'Валюта',
            'youtube_video_url':'Посилання на YouTube відео',    
            'phone':'Номер телефону',    
            'phone2':'Додатковий номер телефону',    
        }
        help_texts = {
            'region': 'Регіон в якому ви працюєте',
            'name':'',
            'locations':'Локації в яких проводите екскурсії',
            'description':'Чому клієнт повинен вибрати вас?',
            'languages':'Мови якими розмовляєте',
            'price':'',
            'currency':'',
            'youtube_video_url':'Посилання на відео про вас',    
            'phone':'',    
            'phone2':'',
            'facebook':'',
            'instagram':'',
            'telegram':'',
            'whatsapp':'',
            'skype':''    
        }
        

class GuideProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(GuideProfileForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Зберегти', css_class='btn-success'))
        self.helper.add_input(Reset('reset', 'Відмінити', css_class='btn-secondary'))
        for field in self.fields:
            self.fields[field].required = True
        
        self.fields['phone2'].required = False
        self.fields['facebook'].required = False
        self.fields['instagram'].required = False
        self.fields['telegram'].required = False
        self.fields['whatsapp'].required = False
        self.fields['skype'].required = False

    def clean_name(self):
        name = self.cleaned_data["name"]
        if re.search("[\d.,:\$]",name):
              raise forms.ValidationError(f'Ім\'я не може містити цифри або спеціальні символи',
                code="Invalid name")
        return name
    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not re.search("^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.\/0-9]*$",phone):
            raise forms.ValidationError(f'Номер телефону не може містити букви або спеціальні символи',
                code="Invalid name")
        return phone
    def clean_phone2(self):
        phone = self.cleaned_data["phone2"]
        if not re.search("^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.\/0-9]*$",phone):
            raise forms.ValidationError(f'Номер телефону не може містити букви або спеціальні символи',
                code="Invalid name")
        return phone
    def clean_youtube_video_url(self):
        yt_url = self.cleaned_data["youtube_video_url"]
        if not re.search("(vi\/|v=|\/v\/|youtu\.be\/|\/embed\/)",yt_url):
            raise forms.ValidationError(f'Неправильне посилання',
                code="Invalid name")
        # print(re.split("(vi\/|v=|\/v\/|youtu\.be\/|\/embed\/)",yt_url))
        return yt_url
    class Meta:
        model = Guide
        exclude = ['user','active','featured','image','index','confirmed']
        labels = {
            'region': 'Область',
            'name':'Ім\'я',
            'locations':'Локації',
            'description':'Опис',
            'languages':'Мови',
            'price':'Ціна',
            'currency':'Валюта',
            'youtube_video_url':'Посилання на YouTube відео',    
            'phone':'Номер телефону',    
            'phone2':'Додатковий номер телефону',

        }
        help_texts = {
            'region': 'Регіон в якому ви працюєте',
            'name':'',
            'locations':'Локації в яких проводите екскурсії',
            'description':'Чому клієнт повинен вибрати вас?',
            'languages':'Мови якими розмовляєте',
            'price':'',
            'currency':'',
            'youtube_video_url':'Посилання на відео про вас',    
            'phone':'',    
            'phone2':'',
            'facebook':'',
            'instagram':'',
            'telegram':'',
            'whatsapp':'',
            'skype':''    
        }


class ChangeImageForm(ModelForm):
    class Meta:
        model = Guide
        fields = ['image']
    def __init__(self, *args, **kwargs):
        super(ChangeImageForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget = FileInput(attrs={
            'name':'image',
            'class':'image',
            'id':'upload_image',
            'style':'display:none'
        })
        # <input type="file" name="image" class="image" id="upload_image" style="display:none" />


class RegisterForm(ModelForm):
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username__iexact = username).exists():
            raise forms.ValidationError(f'Користувач з таким логіном вже зареєстрований',
                code="Already used username")
        return username
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact = email).exists():
            raise forms.ValidationError(f'Користувач з таким email вже зареєстрований',
                code="Already used email")
        return email
    def clean_password(self):
        pattern_password = re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z$%#^]{8,}$')
        password = self.cleaned_data['password']
        if not bool(pattern_password.match(password)):
            raise forms.ValidationError(f'Надто легкий пароль, пароль повинен містити цифру, букву у верхньому і нижньому регістрі і бути довжиною не менше 8 символів',
                code="Bad password")
        return password
    class Meta:
        model = User
        fields = ['email','username','password']
        widgets = {
            'password':PasswordInput(),
            'email':EmailInput()
        }
        help_texts = {
            'username': '',
            'password':''
        }


class TimeInput(forms.TimeInput):
    input_type = "time"
    attrs = {'step' : "3600000"}


class DateInput(forms.TimeInput):
    input_type = "date"

TIME_CHOICES = [
    ('00:00','00:00'),
    ('01:00','01:00'),
    ('02:00','02:00'),
    ('03:00','03:00'),
    ('04:00','04:00'),
    ('05:00','05:00'),
    ('06:00','06:00'),
    ('07:00','07:00'),
    ('08:00','08:00'),
    ('09:00','09:00'),
    ('10:00','10:00'),
    ('11:00','11:00'),
    ('12:00','12:00'),
    ('13:00','13:00'),
    ('14:00','14:00'),
    ('15:00','15:00'),
    ('16:00','16:00'),
    ('17:00','17:00'),
    ('18:00','18:00'),
    ('19:00','19:00'),
    ('20:00','20:00'),
    ('21:00','21:00'),
    ('22:00','22:00'),
    ('23:00','23:00'),
    ('24:00','24:00'),
]
class BookingForm(ModelForm):
    # preferredTime = forms.TimeField(widget=forms.TimeInput(format='%H'))
    numberOfParticipants = forms.CharField(label='Кількість учасників',
     widget=forms.TextInput(attrs={'min':1,'max': 20,'type': 'number'}))
    preferredTime = forms.ChoiceField(choices=TIME_CHOICES,label="Бажаний час")
    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not re.search("^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\.\/0-9]*$",phone):
            raise forms.ValidationError(f'Номер телефону не може містити букви або спеціальні символи',
                code="Invalid name")
        return phone
    def clean_preferredDate(self):
        date = self.cleaned_data["preferredDate"]
        if date.isoformat() < datetime.today().isoformat():
            raise forms.ValidationError(f'Дата раніше сьогоднішньої',
                code="Invalid date")
        return date
    def __init__(self, *args, **kwargs):
        super(BookingForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Забронювати'))
        for field in self.fields:
            self.fields[field].required = True
        self.fields['text'].required = False
    class Meta:
        model = Booking
        fields = ["user_name",'preferredDate','preferredTime','numberOfParticipants','phone','text']
        widgets = {
            'preferredTime':TimeInput(),
            'preferredDate':DateInput()
        }
        labels = {
            'user_name':'Ваше ім\'я',
            'preferredDate':'Бажана дата',
            'preferredTime':'Бажаний час',
            'text':'Побажання, або додаткові дані для зв\'язку',
            'numberOfParticipants':'Кількість учасників',
            'phone':'Номер телефону',
        }
        help_texts = {
            'user_name':'',
            'preferredDate':'',
            'preferredTime':'',
            'text':'',
            'numberOfParticipants':'',
            'phone':'',
        }


class PasswordRecoveryForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(PasswordRecoveryForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget = EmailInput(attrs={
            'id': 'ID_recoveryEmail',
            # "autocomplete":"off"
            })
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Надіслати', css_class='btn-success'))
    def clean_email(self):
        email = self.cleaned_data["email"]
        if not User.objects.filter(email = email).exists():
            raise forms.ValidationError(f'Користувача з таким Email не існує',
                code="Invalid email")
        return email
    class Meta:
        model = User
        fields = ["email"]
        labels = {
            'email':'Електронна пошта:'
        }
class ChangePassword(ModelForm):
    class Meta:
        model = User
        fields = ["password"]
    passwordRepeat = forms.CharField(label="Повторіть пароль",min_length=1,max_length = 30,widget=forms.PasswordInput())
    def __init__(self, *args, **kwargs):
        super(ChangePassword, self).__init__(*args, **kwargs)
        self.fields['password'].widget = PasswordInput(attrs={
            'id': 'ID_changepassword',
            # "autocomplete":"off"
            })
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Змінити', css_class='red-button'))
    def clean(self):
        password = self.cleaned_data["password"]
        passwordRepeat = self.cleaned_data["passwordRepeat"]
        if not password == passwordRepeat:
            raise forms.ValidationError(f'Паролі не співпадають',
                code="passwords not exact")
        pattern_password = re.compile(r'^(?=.*[0-9].*)(?=.*[a-z].*)(?=.*[A-Z].*)[0-9a-zA-Z$%#^]{8,}$')
        if not bool(pattern_password.match(password)):
            raise forms.ValidationError(f'Надто легкий пароль, пароль повинен містити цифру, букву у верхньому і нижньому регістрі і бути довжиною не менше 8 символів',
                code="Bad password")
        return self.cleaned_data
class FeedbackForm(ModelForm):
    def __init__(self, *args,**kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Надіслати', css_class='btn-success'))
    class Meta:
        model = Feedback
        fields = ["text"]
        labels = {"text": "Ваші побажжання, або зауваження"}