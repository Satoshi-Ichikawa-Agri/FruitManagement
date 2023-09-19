from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from fruit_management.models.fruit import Fruit
from fruit_management.forms import FruitForm


class FruitListView(LoginRequiredMixin, ListView):
    """Fruit List View"""

    model = Fruit
    template_name = "fruit_management/index.html"

    def get_queryset(self, **kwargs):
        queryset = Fruit.objects.all().order_by("-updated_at")

        return queryset


class FruitRegisterView(LoginRequiredMixin, CreateView):
    """Fruit Register View"""

    model = Fruit
    form_class = FruitForm
    template_name = "fruit_management/register.html"
    success_url = "/index/"


class FruitEditView(LoginRequiredMixin, UpdateView):
    """Fruit Edit View"""

    model = Fruit
    form_class = FruitForm
    template_name = "fruit_management/edit.html"
    success_url = "/index/"


@login_required
def fruit_delete(request, pk):
    """Fruit Delete"""

    model = Fruit
    template_name = "fruit_management/delete.html"
    fruit = get_object_or_404(model, pk=pk)

    if request.method == "POST":
        fruit.delete()

        return redirect("index")

    return render(request, template_name, {"object": fruit})
