from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.contrib.auth.models import User
from tinymce.models import HTMLField
from datetime import datetime
from cloudinary.models import CloudinaryField
import re

class Language(models.Model):
    name = models.CharField(
        blank=True, max_length=250, help_text=_("Language guide able speak on")
    )
    slug = models.SlugField(default="")
    flag_icon = models.CharField(
        blank=True,
        max_length=250,
        help_text=_(
            "URL to Language flag icon, use: https://iconarchive.com/show/all-country-flag-icons-by-custom-icon-design.html"
        ),
    )
    # https://iconarchive.com/show/all-country-flag-icons-by-custom-icon-design.html

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Language, self).save(*args, **kwargs)


class Country(models.Model):
    name = models.CharField(blank=True, max_length=250, help_text=_("Country name"))
    slug = models.SlugField(default="")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Country, self).save(*args, **kwargs)


class Region(models.Model):
    name = models.CharField(blank=True, max_length=250, help_text=_("Region name"))
    slug = models.SlugField()
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Region, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(blank=True, max_length=250, help_text=_("Location name"))
    slug = models.SlugField()
    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, null=True, blank=True
    )
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Location, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    # def number_of_offers(self):
    #     return self.killertrip_set.count()


class Currency(models.Model):
    name = models.CharField(blank=True, max_length=50)
    symbol = models.CharField(blank=True, max_length=1)

    def __str__(self):
        return self.name + " " + self.symbol
   

class SiteSettings(models.Model):
    """
    Settings for a web site
    """

    active = models.BooleanField(default=True)

    title = models.CharField(
        blank=True, max_length=250, help_text=_("Site title / main name")
    )
    slogan = models.CharField(
        blank=True, max_length=250, help_text=_("Slogan, marketing phrase")
    )
    main_text = HTMLField(
        blank=True,
        help_text=_("Text to be displayed on main (index) page under H1 title"),
    )
    main_text_bottom = HTMLField(
        blank=True,
        help_text=_(
            "Text to be displayed on main (index) page under content, before footer"
        ),
    )
    footer_text = HTMLField(blank=True, help_text=_("Text to be displayed in footer"))

    meta_keywords = models.TextField(blank=True, help_text=_("Keywords for META tag"))
    meta_description = models.TextField(
        blank=True, help_text=_("Description for META tag")
    )

    register_text = HTMLField(
        blank=True, help_text=_("Text to be displayed on guide registration page")
    )

    booking_help = HTMLField(
        blank=True, help_text=_("Text to be displayed on booking page")
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.active:
            for item in SiteSettings.objects.all():
                if item.active:
                    item.active = False
                    item.save()
        super(SiteSettings, self).save(*args, **kwargs)


class Guide(models.Model):
    """
    Trip with guide / offering / local guide.
    """

    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL,
        help_text=_("User, author/owner of this trip"),
        related_name="guide",
    )
    
    active = models.BooleanField(
        default=False, help_text=_("Display it in trips list / search results?")
    )
    featured = models.BooleanField(
        default=False, help_text=_("Display it on main/index page?")
    )
    confirmed = models.BooleanField(default=False,help_text=_("Is guide confirmed"))
    # image = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True,null = True)
    image = CloudinaryField('image', blank=True,null=True)

    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)

    name = models.CharField(blank=True, max_length=250, help_text=_("Guide name"))

    locations = models.ManyToManyField(Location, blank=True)

    languages = models.ManyToManyField(Language, blank=True)

    description = HTMLField(blank=True, help_text=_("Text about this trip"))

    price = models.IntegerField(
          blank=True, default=0
    )
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, null=True, blank=True
    )

    youtube_video_url = models.URLField(
        blank=True,
        max_length=250,
        help_text=_("Link/URL to youtube video, copy it from browser address bar"),
    )

    phone = models.CharField(blank=True, max_length=250, help_text=_("Phone number"))
    phone2 = models.CharField(
        blank=True, max_length=250, help_text=_("Phone number #2")
    )
    facebook = models.CharField(
        blank=True, max_length=250, help_text=_("Facebook page URL")
    )
    instagram = models.CharField(
        blank=True, max_length=250, help_text=_("Instagram page URL")
    )
    telegram = models.CharField(
        blank=True, max_length=250, help_text=_("Telegram user")
    )
    whatsapp = models.CharField(
        blank=True, max_length=250, help_text=_("WhatsApp user")
    )
    skype = models.CharField(blank=True, max_length=250, help_text=_("Skype user"))
    index = models.TextField(blank=True,null=True)
    def __str__(self):
        return self.name 

    def video_id(self):
        # if not self.youtube_video_url:
        #     return ""
        # return self.youtube_video_url.split("?v=")[1]
        if not self.youtube_video_url:
            return ""
        url = re.split("(vi\/|v=|\/v\/|youtu\.be\/|\/embed\/)",self.youtube_video_url)
        if url[2]:
            return re.split("[^0-9a-z_\-]",url[2],flags=re.IGNORECASE)[0]
        else:
            return url[0]

    def video_img(self):
        return f"https://img.youtube.com/vi/{self.video_id()}/default.jpg"

    def video_embed(self):
        return "https://www.youtube.com/embed/" + self.video_id()
    def country(self):
        return self.region.country
    def rating(self):
        rating = 0
        count = self.review_set.count()
        for item in self.review_set.all():
            if item.isModerated:
                rating += int(item.rating)
            else:
                count = count - 1
        if count:
            return round(rating / count, 1)
        return 0
    def waiting_bookings(self):
        return Booking.objects.filter(trip = self,isCanceled = False,isConfirmed = False,preferredDate__gt=datetime.today()).count()
    
    def get_special(self):
        return self.special.splitlines()
    def trip_count(self):
        return Booking.objects.filter(trip=self,isConfirmed = True).__len__()
    def save(self, *args, **kwargs):
        if not self.pk is None: 
            self.index = self.name + self.region.name + self.region.slug + self.region.country.name + self.region.country.slug + self.description
            for location in self.locations.all():
                self.index = self.index + location.name + location.slug
        super(Guide, self).save(*args, **kwargs)


class SavedGuides(models.Model):
    user = models.OneToOneField(
        User,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL,
        help_text=_("User"),
    )
    guides = ManyToManyField(Guide, blank=True)

class Review(models.Model):
    created = models.DateField(auto_now_add=True)
    
    user_name = models.CharField(
        blank=True, max_length=50, help_text=_("User name (maybe anonymous)")
    )
    trip = models.ForeignKey(Guide, on_delete=models.CASCADE, null=True, blank=True)
    text = models.CharField(max_length=250,blank=True, help_text=_("Review text"))
    rating = models.CharField(
        max_length=1,
        default="5",
        choices=(("5", "5"), ("4", "4"), ("3", "3"), ("2", "2"), ("1", "1")),
    )
    isModerated = models.BooleanField(default = True, help_text = _("Is this review should be shown"))
    def __str__(self):
        # return f"{self.user_name} about {self.trip.name}"
        return f"{self.user_name}"

    def rating_range(self):
        if self.rating:
            return range(int(self.rating))
        return range(5)

class Booking(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_NULL,
        help_text=_("User, who booked trip"),
    )
    user_name = models.CharField(
        blank=True, max_length=250, help_text=_("User name")
    )
    preferredDate = models.DateField(null=True,help_text=_("Preferred date"))
    preferredTime = models.TimeField(null=True,help_text=_("Preferred time"),)
    trip = models.ForeignKey(Guide, on_delete=models.CASCADE, null=True, blank=True)
    text = HTMLField(blank=True, help_text=_("Special wishes text"),max_length=250)
    numberOfParticipants = models.CharField(blank=True, max_length=3, help_text=_("Number of participants in tour"))
    phone = models.CharField(blank=True, max_length=13, help_text=_("Phone number"))
    isConfirmed = models.BooleanField(default = False, help_text = _("Does booking was confirmed by guide"))
    isCanceled = models.BooleanField(default = False, help_text = _("Does booking was canceled by guide"))
    cancel_message = models.CharField(blank=True,null=True,max_length=250,help_text=_("Why booking was canceled?"))

class Statistic(models.Model):
    date = models.DateField(auto_now_add=True,primary_key=True)
    logins = models.IntegerField(default=0,help_text="Кількість логінів за день")
    registers = models.IntegerField(default=0,help_text="Кількість логінів за день")
    bookings = models.IntegerField(default=0,help_text="Кількість бронювань за день")
    def incLogin(self):
        self.logins += 1
        self.save()
    def incRegister(self):
        self.registers += 1
        self.save()
    def incBooking(self):
        self.bookings += 1
        self.save()
class Feedback(models.Model):
     date = models.DateField(auto_now_add=True)
     text = HTMLField(help_text = _("Ваші зауваження, або побажання"))
