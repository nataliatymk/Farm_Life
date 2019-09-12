from django.contrib import admin
from django.urls import path, re_path
from django.views.i18n import JavaScriptCatalog

from farmlife.views import (LandingPageView, LandsView, LogoutView, CreateUser,
                            MainView, AboutView, EditUser,
                            ContactView, AddLandView, DetailsLandView, EditLandView,
                            MachineryView, AddMachineryView, DetailsMachineryView, EditMachineryView,
                            PlantsView, AddPlantView, DetailsPlantView,EditPlantView,
                            IncomesView, ExpensesView, BalanceView, AddIncomesView, AddExpensesView)

urlpatterns = [
    re_path(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    re_path('^admin/', admin.site.urls),
    re_path('^$', LandingPageView.as_view(), name="landing"),
    re_path('^login/$', LandingPageView.as_view(), name="login"),
    re_path('^logout/$', LogoutView.as_view(), name="logout"),
    re_path('^create_user/$', CreateUser.as_view(), name="create_user"),
    re_path('^edit_user/(?P<user_id>(\d+))/$', EditUser.as_view(), name="edit_user"),


    re_path('^main/$', MainView.as_view(), name="main"),
    re_path('^about/$', AboutView.as_view(), name="about"),
    re_path('^contact/$', ContactView.as_view(), name="contact"),

    re_path('^lands/$', LandsView.as_view(), name="lands"),
    re_path('^lands/add/$', AddLandView.as_view(), name="add_land"),
    re_path('^lands/details/(?P<land_id>(\d+))/$', DetailsLandView.as_view(), name="details_land"),
    re_path('^lands/edit/(?P<land_id>(\d+))/$', EditLandView.as_view(), name="edit_land"),

    re_path ('^machinery/$', MachineryView.as_view (), name="machinery"),
    re_path ('^machinery/add/$', AddMachineryView.as_view (), name="add_machinery"),
    re_path ('^machinery/details/(?P<machinery_id>(\d+))/$', DetailsMachineryView.as_view (), name="details_machinery"),
    re_path ('^machinery/edit/(?P<machinery_id>(\d+))/$', EditMachineryView.as_view (), name="edit_machinery"),

    re_path ('^plants/$', PlantsView.as_view (), name="plants"),
    re_path ('^plants/add/$', AddPlantView.as_view (), name="add_plant"),
    re_path ('^plants/details/(?P<plant_id>(\d+))/$', DetailsPlantView.as_view (), name="details_plant"),
    re_path ('^plants/edit/(?P<plant_id>(\d+))/$', EditPlantView.as_view (), name="edit_plant"),

    re_path ('^incomes/$', IncomesView.as_view (), name="incomes"),
    re_path ('^incomes/add$', AddIncomesView.as_view (), name="add_incomes"),
    re_path ('^expenses/$', ExpensesView.as_view (), name="expenses"),
    re_path ('^expenses/add/$', AddExpensesView.as_view (), name="add_expenses"),
    re_path ('^balance/$', BalanceView.as_view (), name="balance"),
    # re_path ('^balance/pdf/download$', GeneratePDF.as_view(), name="pdf_balance"),


]
