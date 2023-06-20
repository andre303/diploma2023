from django.urls import path, include, re_path

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

admin.autodiscover()

import trips.views

urlpatterns = [
    path("", trips.views.list, name="list"),
    path("tourist_exchange/", TemplateView.as_view(template_name = "tourist_exchange.html"), name="tourist_exchange"),
    path("list/", trips.views.list, name="list"),
    path("live_search/",trips.views.live_search, name  = "live_search"),
    path("saveGuide/", trips.views.addToSaved, name="saveGuide"),
    path("unSaveGuide/", trips.views.removeFromSaved, name="saveGuide"),
    path("savedGuides/",trips.views.savedGuides, name = "savedGuides"),
    path("location/<str:location_slug>/", trips.views.list, name="list"),
    path("country/<str:country_slug>/", trips.views.list, name="list"),

    path("register/", trips.views.register, name="register"),
    path("login/", trips.views.social_login, name="social_login"),
    path("facebook_deletion/", trips.views.facebook_deletion,name = "facebook_deletion"),
    path("deleteProfile/", trips.views.deleteProfile,name = "deleteProfile"),
    path("password_recover/", trips.views.password_recover, name="password_recover"),
    path("agent/", trips.views.agent, name="agent"),

    path("profile/", trips.views.profile, name="profile"),
    path("profile/change_photo/",trips.views.change_photo,name="change_photo"),

    path("booking_list/",trips.views.bookings_list, name = "booking_list"),
    path("booking_list/booking_archive/",trips.views.bookings_archive, name = "booking_archive"),
    path("booking_list/confirm/<int:book_id>/",trips.views.confirm_booking, name = "confirm_booking"),
    path("booking_list/cancel/",trips.views.cancel_booking, name = "cancel_booking"),

    path("trip/<int:trip_id>/", trips.views.detail, name="detail"),
    path("review/<int:trip_id>/", trips.views.review, name="review"),

    

    path("guide_register/",trips.views.guide_register,name="guide_register"),
    path("email_register/",trips.views.email_register,name="email_register"),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        trips.views.activate, name='activate'),
    re_path(r'^recover/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        trips.views.recover, name='recover'),
    path("change_password/",trips.views.change_password, name = "change_password"),
    path("email_login/",trips.views.email_login,name="email_login"),
    # Footer
    path("feedback/",trips.views.feedback,name="feedback"),
    path("policy/",trips.views.policy,name="policy"),
    path("custom-agreement/",trips.views.custom_agreement,name="custom-agreement"),
    # auth
    path("", include("social_django.urls", namespace="social")),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    #############
    path("admin/", admin.site.urls),
    path("rosetta/", include("rosetta.urls")),
    path("tinymce/", include("tinymce.urls")),
]

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
