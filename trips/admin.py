from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from import_export import fields
from .models import *


class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("title", "active")

@admin.action(description='Mark selected guides as active')
def make_active(modeladmin, request, queryset):
    queryset.update(active=True)

@admin.action(description='Mark selected guides as not active')
def make_not_active(modeladmin, request, queryset):
    queryset.update(active=False)

@admin.action(description='Mark selected guides as featured')
def make_featured(modeladmin, request, queryset):
    queryset.update(featured=True)

@admin.action(description='Mark selected guides as not featured')
def make_not_featured(modeladmin, request, queryset):
    queryset.update(featured=False)

@admin.action(description='Mark selected guides as confirmedd')
def make_confirmed(modeladmin, request, queryset):
    queryset.update(confirmed=True)

class GuideAdmin(admin.ModelAdmin):
    list_display = ("name","pk","user" ,"featured","active","confirmed")
    search_fields = ("pk","name","user__username")
    actions = [make_active,make_not_active,make_featured,make_not_featured,make_confirmed]

class CountryResource(resources.ModelResource):
    class Meta:
        model = Country
        fields = ["name","slug"]
class CountryAdmin(ImportExportModelAdmin):
    resource_class = CountryResource
    list_display = ("name",)

class RegionResource(resources.ModelResource):
    class Meta:
        model = Region
class RegionAdmin(ImportExportModelAdmin):
    resource_class = RegionResource
    list_display = ("name",)

class LocationResource(resources.ModelResource):
    class Meta:
        model = Location
class LocationAdmin(ImportExportModelAdmin):
    resource_class = LocationResource
    list_display = ("name", "country")

class CurrencyResource(resources.ModelResource):
    class Meta:
        model = Currency
        fields = ["name","symbol"]
class CurrencyAdmin(ImportExportModelAdmin):
    resource_class = CurrencyResource
    list_display = ("name", "symbol")

class LanguageResource(resources.ModelResource):
    class Meta:
        model = Language
        fields = ["name","slug","flag_icon"]
class LanguageAdmin(ImportExportModelAdmin):
    resource_class = LanguageResource
    list_display = ("name",)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ("created", "user_name", "trip", "rating")
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user_name", "trip","numberOfParticipants","isConfirmed","isCanceled")

class StatisticAdmin(admin.ModelAdmin):
    list_display = ("date","logins","registers","bookings")
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("date", "text")
class SavedAdmin(admin.ModelAdmin):
    list_display = ("user",)

admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(Guide, GuideAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Currency, CurrencyAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Statistic, StatisticAdmin)
admin.site.register(Feedback,FeedbackAdmin)
admin.site.register(SavedGuides,SavedAdmin)