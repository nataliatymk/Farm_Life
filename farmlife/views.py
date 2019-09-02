from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.views.generic import UpdateView

from farmlife.forms import LoginForm, LandForm
from farmlife.models import AgriculturalLand


class LandingPageView(View):
    def get(self, request):
        form = LoginForm()

        return render(request, "base.html", context={"form":form})

    def post (self, request):
        form = LoginForm (request.POST)
        if form.is_valid ():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate (username=username, password=password)
            if user is not None:
                login (request, user)
                return redirect (reverse ("lands"))
            else:
                return HttpResponse ("Błędny login lub hasło")

class LogoutView (View):
    def get (self, request):
        logout (request)
        return redirect (reverse ("landing"))


class LandsView(View):
    def get(self, request):
        lands = AgriculturalLand.objects.all().order_by("land_name")
        return render (request, "land.html", context={"lands": lands})

class AddLandView(View):
    def get(self, request):
        add_new = "Dodaj nowy użytek"
        form = LandForm()
        return render (request, "land_add.html", context={"form":form, "add_new":add_new})

    def post(self, request):
        add_new = "Dodaj nowy użytek"
        form = LandForm (request.POST)
        if form.is_valid():
            land_name = form.cleaned_data["land_name"]
            type = form.cleaned_data["type"]
            area = form.cleaned_data["area"]
            comments = form.cleaned_data["comments"]
            AgriculturalLand.objects.create(land_name=land_name, type=type, area=area, comments=comments)
            return redirect ("lands")
        return render (request, "land_add.html", context={"form": form, "add_new": add_new})

class DetailsLandView(View):
    def get(self, request, land_id):
        land = AgriculturalLand.objects.get(id=land_id)
        return render (request, "land_details.html", context={"land": land})

    def post(self, request, land_id):
            land = AgriculturalLand.objects.get (id=land_id)
            btn_del = request.POST.get("delete")
            if btn_del:
                land.delete()
                return redirect ("lands")

class EditLandView(View):
    def get(self,request, land_id):
        add_new = "Edytuj!"
        land = AgriculturalLand.objects.get(id=land_id)
        form = LandForm (instance=land)
        return render (request, "land_add.html", context={"form": form, "add_new": add_new})

    def post(self, request, land_id):
        land = AgriculturalLand.objects.get (id=land_id)
        form = LandForm (request.POST, instance=land)
        if form.is_valid():
            form.save()
            return redirect ("lands")



