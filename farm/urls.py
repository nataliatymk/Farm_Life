from django.contrib import admin
from django.urls import path, re_path

from farmlife.views import (LandingPageView, LandsView, AddLandView, DetailsLandView, EditLandView)

urlpatterns = [
    re_path('^admin/', admin.site.urls),
    re_path('^$', LandingPageView.as_view(), name="landing"),
    re_path('^lands/$', LandsView.as_view(), name="lands"),
    re_path('^lands/add/$', AddLandView.as_view(), name="add_land"),
    re_path('^lands/details/(?P<land_id>(\d+))/$', DetailsLandView.as_view(), name="details_land"),
    re_path('^lands/edit/(?P<land_id>(\d+))/$', EditLandView.as_view(), name="edit_land"),

]
