from django.contrib.auth.models import User
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from datetime import datetime

from django.template.loader import get_template
from farm.utils import render_to_pdf

from farmlife.forms import LoginForm, LandForm, MachineryForm, PlantForm, IncomeForm, ExpensesForm, UserForm, \
    BalanceForm, EditUserForm
from farmlife.models import AgriculturalLand, AgriculturalMachinery, Plants, ExtraExpenses, AdditionalIncome


class LandingPageView (View):
    def get (self, request):
        form = LoginForm ()
        user = request.user
        return render (request, "landing_page.html", context={"form": form, "user": user})

    def post (self, request):
        form = LoginForm (request.POST)
        if form.is_valid ():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate (username=username, password=password)
            if user is not None:
                login (request, user)
                return redirect (reverse ("main"))
            else:
                return HttpResponse ("Błędny login lub hasło")


class LogoutView (View):
    def get (self, request):
        logout (request)
        return redirect (reverse ("landing"))


class MainView (View):
    def get (self, request):
        user = request.user
        return render (request, "index.html", context={"user": user})


class AboutView (View):
    def get (self, request):
        return render (request, "about.html")


class ContactView (View):
    def get (self, request):
        return render (request, "contact.html")


class CreateUser (View):
    def get (self, request):
        message = "Stwórz nowego użytkownika"
        form = UserForm ()
        return render (request, "create_user.html", context={"form": form, "message": message})

    def post (self, request):
        message = "Stwórz nowego użytkownika"
        form = UserForm (request.POST)
        if form.is_valid ():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            User.objects.create_user (username=username, email=email, password=password)

            return redirect ("login")
        else:
            form = UserForm ()
            return render (request, "create_user.html", context={"form": form, "message": message})


class LandsView (View):
    def get (self, request):
        lands = AgriculturalLand.objects.filter (user_log=request.user).order_by ("land_name")
        return render (request, "land.html", context={"lands": lands})


class AddLandView (View):
    def get (self, request):
        add_new = "Dodaj nowy użytek"
        form = LandForm ()
        return render (request, "land_add.html", context={"form": form, "add_new": add_new})

    def post (self, request):
        add_new = "Dodaj nowy użytek"
        form = LandForm (request.POST)
        if form.is_valid ():
            land_name = form.cleaned_data["land_name"]
            type = form.cleaned_data["type"]
            area = form.cleaned_data["area"]
            comments = form.cleaned_data["comments"]
            AgriculturalLand.objects.create (user_log=request.user, land_name=land_name, type=type, area=area, comments=comments)
            return redirect ("lands")
        return render (request, "land_add.html", context={"form": form, "add_new": add_new})


class DetailsLandView (View):
    def get (self, request, land_id):
        land = AgriculturalLand.objects.get (id=land_id)
        return render (request, "land_details.html", context={"land": land})

    def post (self, request, land_id):
        land = AgriculturalLand.objects.get (id=land_id)
        btn_del = request.POST.get ("delete")
        if btn_del:
            land.delete ()
            return redirect ("lands")


class EditLandView (View):
    def get (self, request, land_id):
        add_new = "Edytuj!"
        land = AgriculturalLand.objects.get (id=land_id)
        form = LandForm (instance=land)
        return render (request, "land_add.html", context={"form": form, "add_new": add_new})

    def post (self, request, land_id):
        land = AgriculturalLand.objects.get (id=land_id)
        form = LandForm (request.POST, instance=land)
        if form.is_valid ():
            form.save ()
            return redirect ("lands")


class MachineryView (View):
    def get (self, request):
        machinery = AgriculturalMachinery.objects.filter (user_log=request.user).order_by ("machinery_name")
        return render (request, "machinery.html", context={"machinery": machinery})


class AddMachineryView (View):
    def get (self, request):
        add_new = "Dodaj nową maszynę"
        user = request.user
        form = MachineryForm (user_log=user)
        return render (request, "machinery_add.html", context={"form": form, "add_new": add_new})

    def post (self, request):
        add_new = "Dodaj nowy użytek"
        user = request.user
        form = MachineryForm (request.POST, user_log=user)
        if form.is_valid ():
            machinery_name = form.cleaned_data["machinery_name"]
            fuel_consumption = form.cleaned_data["fuel_consumption"]
            land = form.cleaned_data["land_machinery"]
            accessories = form.cleaned_data["accessories"]
            accessories_width = form.cleaned_data["accessories_width"]
            time_add = form.cleaned_data["time_add"]
            new_machinery = AgriculturalMachinery.objects.create (user_log=request.user,
                                                                  machinery_name=machinery_name,
                                                                  fuel_consumption=fuel_consumption,
                                                                  accessories=accessories,
                                                                  accessories_width=accessories_width,
                                                                  time_add=time_add)
            new_machinery.land_machinery.set (land)
            return redirect ("machinery")
        return render (request, "machinery_add.html", context={"form": form, "add_new": add_new})


class DetailsMachineryView (View):
    def get (self, request, machinery_id):
        machinery = AgriculturalMachinery.objects.get (id=machinery_id)
        return render (request, "machinery_details.html", context={"machinery": machinery})

    def post (self, request, machinery_id):
        land = AgriculturalMachinery.objects.get (id=machinery_id)
        btn_del = request.POST.get ("delete")
        if btn_del:
            land.delete ()
            return redirect ("machinery")


class EditMachineryView (View):
    def get (self, request, machinery_id):
        add_new = "Edytuj!"
        machinery = AgriculturalMachinery.objects.get (id=machinery_id)
        user = request.user
        form = MachineryForm (instance=machinery, user_log=user)
        return render (request, "machinery_add.html", context={"form": form, "add_new": add_new})

    def post (self, request, machinery_id):
        machinery = AgriculturalMachinery.objects.get (id=machinery_id)
        user = request.user
        form = MachineryForm (request.POST, instance=machinery, user_log=user)
        if form.is_valid ():
            form.save ()
            return redirect ("machinery")


class PlantsView (View):
    def get (self, request):
        plants = Plants.objects.filter (user_log=request.user).order_by ("plant_name")
        return render (request, "plant.html", context={"plants": plants})


class AddPlantView (View):
    def get (self, request):
        add_new = "Dodaj nową roślinę"
        user = request.user
        form = PlantForm (user_log=user)
        return render (request, "plant_add.html", context={"form": form, "add_new": add_new})

    def post (self, request):
        add_new = "Dodaj nową roślinę"
        user = request.user
        form = PlantForm (request.POST, user_log=user)
        if form.is_valid ():
            plant_name = form.cleaned_data["plant_name"]
            expected_yield = form.cleaned_data["expected_yield"]
            plant_price = form.cleaned_data["plant_price"]
            land_plant = form.cleaned_data["land_plant"]
            harvest = form.cleaned_data["harvest"]
            sale = form.cleaned_data["sale"]
            comments = form.cleaned_data["comments"]
            time_add = form.cleaned_data["time_add"]
            new_plant = Plants.objects.create (user_log=request.user, plant_name=plant_name,
                                               expected_yield=expected_yield,
                                               plant_price=plant_price, harvest=harvest,
                                               sale=sale, comments=comments, time_add=time_add)
            new_plant.land_plant.set (land_plant)
            return redirect ("plants")
        return render (request, "plant_add.html", context={"form": form, "add_new": add_new})


class DetailsPlantView (View):
    def get (self, request, plant_id):
        plant = Plants.objects.get (id=plant_id)
        return render (request, "plant_details.html", context={"plant": plant})

    def post (self, request, plant_id):
        plant = Plants.objects.get (id=plant_id)
        btn_del = request.POST.get ("delete")
        if btn_del:
            plant.delete ()
            return redirect ("plants")


class EditPlantView (View):
    def get (self, request, plant_id):
        add_new = "Edytuj!"
        user = request.user
        plant = Plants.objects.get (id=plant_id)
        form = PlantForm (instance=plant, user_log=user)
        return render (request, "plant_add.html", context={"form": form, "add_new": add_new})

    def post (self, request, plant_id):
        plant = Plants.objects.get (id=plant_id)
        user = request.user
        form = PlantForm (request.POST, instance=plant, user_log=user)
        if form.is_valid ():
            form.save ()
            return redirect ("plants")


class BalanceView (View):
    def get (self, request):
        form = BalanceForm ()
        return render (request, "balance.html", context={"form": form})

    def post (self, request):
        form = BalanceForm (request.POST)
        fuel_price = (request.POST.get ("fuel_price"))

        sd = datetime.strptime ((request.POST.get ("start_date")), "%d.%m.%Y")
        start = datetime.strftime (sd, "%Y-%m-%d")
        ed = datetime.strptime ((request.POST.get ("end_date")), "%d.%m.%Y")
        end = datetime.strftime (ed, "%Y-%m-%d")

        area_dict = {}
        fuel_dict = {}
        harvest_dict = {}

        expenses = 0
        incomes = 0
        harvest_sale = 0
        plant_price = 0
        expected_sale = 0
        fuel = 0
        sale = 0

        machinery = AgriculturalMachinery.objects.filter (user_log=request.user).order_by ("machinery_name").filter (
            time_add__range=[start, end])
        plants = Plants.objects.filter (user_log=request.user).order_by ("plant_name").filter (
            time_add__range=[start, end])
        extra_expenses = ExtraExpenses.objects.filter (user_log=request.user).order_by ("expenses_name").filter (
            time_add__range=[start, end])
        additional_income = AdditionalIncome.objects.filter (user_log=request.user).order_by ("income_name").filter (
            time_add__range=[start, end])

        for i in machinery:
            area = 0
            machine = i.land_machinery.all ()
            machine_name = i.machinery_name
            if machine_name not in area_dict:
                for sum_area in machine:
                    area += int(sum_area.area)
                    area_dict[machine_name] = area

            if machine_name in area_dict:
                road = ((area_dict[machine_name]) / 100) / i.accessories_width
                fuel_cost = i.fuel_consumption * float(fuel_price)
                result = round (road * fuel_cost, 2)
                fuel_dict[machine_name] = round (result, 2)
                fuel += result
                fuel = round (fuel, 2)

        for i in plants:
            harvest_single_sale = i.harvest * i.sale
            expected_single_sale = i.expected_yield * i.sale
            harvest_dict[i.plant_name] = harvest_single_sale
            expected_sale += round (expected_single_sale, 2)
            harvest_sale += round (harvest_single_sale, 2)
            plant_price += round (i.plant_price, 2)

        for e in extra_expenses:
            expenses += e.cost

        for a in additional_income:
            incomes += a.cost

        for s in plants:
            sale += s.sale

        profit = harvest_sale - expected_sale

        final_balance = round (
            float(incomes) + float(harvest_sale) - float(plant_price) - float(fuel) - float(expenses), 2)

        context = {"final_balance": final_balance, "expected_sale": expected_sale, "harvest_sale": harvest_sale,
                   "expenses": expenses, "incomes": incomes, "fuel": fuel, "plant_price": plant_price,
                   "fuel_price": fuel_price, "sale": sale, "profit": profit, "form": form}

        return render (request, "balance.html", context=context)



    # def __init__(self):
    #     self.final_balance = final_balance
    #     self.expected_sale = expected_sale
    #     self.harvest_sale = harvest_sale
    #     self.expenses = expenses
    #     self.incomes = incomes
    #     self.fuel = fuel
    #     self.plant_price = plant_price
    #     self.fuel_price = fuel_price
    #     self.sale = sale
    #     self.profit = profit




# class GeneratePDF(View):
#     def get(self, request, *args, **kwargs):
#         template = get_template('balance.html')
#         balance = BalanceView
#
#         context = {"final_balance": balance.final_balance, "expected_sale": balance.expected_sale, "harvest_sale": balance.harvest_sale, "expenses": balance.expenses, "incomes": balance.incomes, "fuel": balance.fuel, "plant_price": balance.plant_price, "fuel_price": balance.fuel_price, "sale": balance.sale, "profit": balance.profit}
#
#         html = template.render(context)
#         pdf = render_to_pdf('invoice.html', context)
#         if pdf:
#             response = HttpResponse(pdf, content_type='templates')
#             filename = "Invoice_%s.pdf" %("12341231")
#             content = "inline; filename='%s'" %(filename)
#             download = request.GET.get("download")
#             if download:
#                 content = "attachment; filename='%s'" %(filename)
#             response['Content-Disposition'] = content
#             return response
#         return HttpResponse("Not found")


class IncomesView (View):
    def get (self, request):
        income = AdditionalIncome.objects.filter (user_log=request.user).order_by ("cost")
        return render (request, "incomes.html", context={"income": income})

    def post (self, request):
        btn_del = request.POST.get ("delete")
        income = AdditionalIncome.objects.get (id=btn_del)
        if btn_del:
            income.delete ()
            return redirect ("incomes")


class ExpensesView (View):
    def get (self, request):
        expenses = ExtraExpenses.objects.filter (user_log=request.user).order_by ("cost")
        return render (request, "expenses.html", context={"expenses": expenses})

    def post (self, request):
        btn_del = request.POST.get ("delete")
        expenses = ExtraExpenses.objects.get (id=btn_del)
        if btn_del:
            expenses.delete ()
            return redirect ("expenses")


class AddExpensesView (View):
    def get (self, request):
        form = ExpensesForm ()
        return render (request, "expenses_add.html", context={"form": form})

    def post (self, request):
        expenses = ExtraExpenses.objects.filter (user_log=request.user)
        form = ExpensesForm (request.POST)
        if form.is_valid ():
            expenses_name = form.cleaned_data["expenses_name"]
            cost = form.cleaned_data["cost"]
            time_add = form.cleaned_data["time_add"]
            ExtraExpenses.objects.create (user_log=request.user, expenses_name=expenses_name, cost=cost,
                                          time_add=time_add)
            return render (request, "expenses.html", context={"expenses": expenses, "form": form})


class AddIncomesView (View):
    def get (self, request):
        form = IncomeForm ()
        return render (request, "incomes_add.html", context={"form": form})

    def post (self, request):
        income = AdditionalIncome.objects.filter (user_log=request.user)
        form = IncomeForm (request.POST)
        if form.is_valid ():
            income_name = form.cleaned_data["income_name"]
            cost = form.cleaned_data["cost"]
            time_add = form.cleaned_data["time_add"]
            AdditionalIncome.objects.create (user_log=request.user, income_name=income_name, cost=cost,
                                             time_add=time_add)
            return render (request, "incomes.html", context={"income": income, "form": form})


class EditUser (View):
    def get (self, request, user_id):
        message = "Zmień hasło"
        user = User.objects.get (id=user_id)
        form = EditUserForm ()
        return render (request, "create_user.html", context={"form": form, "message": message})

    def post (self, request, user_id):
        message = "Zmień hasło"
        user = User.objects.get (id=user_id)
        form = EditUserForm (request.POST)
        if form.is_valid ():
            password = form.cleaned_data["password"]
            user.set_password (password)
            user.save ()
            return redirect ("landing")
        else:
            return render (request, "create_user.html", context={"form": form, "message": message})
