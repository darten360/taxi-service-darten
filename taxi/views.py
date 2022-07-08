from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic

from .forms import DriverCreationForm, DriverForm, DriverUpdateForm, CarForm, CarSearchForm
from .models import Driver, Car, Manufacturer


@login_required
def index(request):
    """View function for the home page of the site."""

    num_drivers = Driver.objects.count()
    num_cars = Car.objects.count()
    num_manufacturers = Manufacturer.objects.count()
    num_visits = request.session.get("num_visits", 1)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_drivers": num_drivers,
        "num_cars": num_cars,
        "num_manufacturers": num_manufacturers,
        "num_visits": num_visits
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(LoginRequiredMixin, generic.ListView):
    model = Manufacturer
    context_object_name = "manufacturers"
    paginate_by = 2


class ManufacturerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Manufacturer


class ManufacturerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Manufacturer
    fields = "__all__"

    def get_success_url(self):
        return reverse('taxi:manufacturer-detail', kwargs={'pk': self.object.pk})


class ManufacturerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Manufacturer
    fields = "__all__"

    def get_success_url(self):
        return reverse('taxi:manufacturer-detail', kwargs={'pk': self.object.pk})


class ManufacturerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Manufacturer
    success_url = reverse_lazy("taxi:manufacturers")
    template_name = "taxi/manufacturer_delete_form.html"


class CarListView(LoginRequiredMixin, generic.ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.all().select_related("manufacturer")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CarListView, self).get_context_data(**kwargs)

        model = self.request.GET.get("model", "")

        context["search_form"] = CarSearchForm(initial={
            "model": model
        })

        return context

    def get_queryset(self):
        form = CarSearchForm(self.request.GET)

        if form.is_valid():
            return self.queryset.filter(
                model__icontains=form.cleaned_data["model"]
            )

        return self.queryset


class CarDetailView(LoginRequiredMixin, generic.DetailView):
    model = Car


class CarCreateView(LoginRequiredMixin, generic.CreateView):
    model = Car
    form_class = CarForm

    def get_success_url(self):
        return reverse('taxi:car-detail', kwargs={'pk': self.object.pk})


class CarUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Car
    form_class = CarForm

    def get_success_url(self):
        return reverse('taxi:car-detail', kwargs={'pk': self.object.pk})


class CarDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Car
    success_url = reverse_lazy("taxi:cars")
    template_name = "taxi/car_delete_form.html"


class DriverListView(LoginRequiredMixin, generic.ListView):
    model = Driver
    paginate_by = 2


class DriverDetailView(LoginRequiredMixin, generic.DetailView):
    model = Driver
    queryset = Driver.objects.all().prefetch_related("cars__manufacturer")


class DriverCreateView(LoginRequiredMixin, generic.CreateView):
    model = Driver
    form_class = DriverCreationForm

    def get_success_url(self):
        return reverse('taxi:driver-detail', kwargs={'pk': self.object.pk})


class DriverUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Driver
    form_class = DriverUpdateForm

    def get_success_url(self):
        return reverse('taxi:driver-detail', kwargs={'pk': self.object.pk})


class LicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Driver
    form_class = DriverForm
    template_name = "taxi/license_form.html"

    def get_success_url(self):
        return reverse('taxi:driver-detail', kwargs={'pk': self.object.pk})


class DriverDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Driver
    success_url = reverse_lazy("taxi:drivers")
    template_name = "taxi/driver_delete_form.html"


def assign_or_delete(request, pk):
    driver = Driver.objects.get(id=request.user.id)
    if Car.objects.get(id=pk) in driver.cars.all():
        driver.cars.remove(pk)
    else:
        driver.cars.add(pk)
    return HttpResponseRedirect(reverse_lazy("taxi:car-detail", args=[pk]))
