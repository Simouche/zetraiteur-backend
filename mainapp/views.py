from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView, TemplateView, FormView
from django_filters.views import FilterView
from django_tables2 import SingleTableMixin

from mainapp.filters import ClientFilter, MenuFilter, FoodFilter, ExtraFilter, OrderFilter
from mainapp.forms import LoginForm, DeleteForm, MenuForm, MenuWithSectionsFormSet, SectionsFormsetHelper, FoodForm, \
    ExtraForm
from mainapp.models import Client, Menu, Food, Extra, Order
from mainapp.tables import ClientTable, MenuTable, FoodTable, ExtraTable, OrderTable


class LoginView(FormView):
    form_class = LoginForm
    template_name = "dashboard/login.html"
    success_url = reverse_lazy("mainapp:dashboard")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('mainapp:dashboard')
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form: LoginForm):
        user = authenticate(self.request, username=form.get_username, password=form.get_password)
        if user:
            login(self.request, user)
            return super(LoginView, self).form_valid(form)
        else:
            form.add_error("", _('Invalid Username or Password'))
            return self.form_invalid(form=form)


@login_required
def logout_view(request):
    logout(request)
    return redirect(reverse("mainapp:login"))


@method_decorator(login_required, name="dispatch")
class Dashboard(TemplateView):
    template_name = "dashboard/index.html"


@method_decorator(login_required, name="dispatch")
class UsersListView(ListView):
    pass


@method_decorator(login_required, name="dispatch")
class UserCreateView(CreateView):
    pass


@method_decorator(login_required, name="dispatch")
class UserUpdateView(UpdateView):
    pass


@method_decorator(login_required, name="dispatch")
class UserDeleteView(DeleteView):
    pass


@method_decorator(login_required, name="dispatch")
class UserDetailView(DetailView):
    pass


@method_decorator(login_required, name="dispatch")
class ClientListView(SingleTableMixin, FilterView):
    model = Client
    table_class = ClientTable
    template_name = "dashboard/client_list.html"
    paginate_by = 25
    paginate_orphans = True
    allow_empty = True
    filterset_class = ClientFilter


@method_decorator(login_required, name="dispatch")
class ClientUpdateView(ListView):
    pass


@method_decorator(login_required, name="dispatch")
class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy("mainapp:clients-list")
    template_name = "dashboard/fragments/delete_form.html"
    form_class = DeleteForm

    def get_form(self):
        return self.form_class()

    def get_delete_url(self):
        return reverse("mainapp:client-delete", kwargs={"pk": self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        return super(ClientDeleteView, self).get_context_data(form=self.get_form(), delete_url=self.get_delete_url(),
                                                              **kwargs)

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            html = render_to_string(self.template_name, context, self.request)
            return JsonResponse(html, safe=False)
        return super(ClientDeleteView, self).render_to_response(context, **response_kwargs)


@method_decorator(login_required, name="dispatch")
class ClientDetailView(DetailView):
    template_name = "dashboard/fragments/client_profile.html"
    ajax_template_name = "dashboard/fragments/client_profile.html"
    context_object_name = "client"
    model = Client

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            html = render_to_string(self.ajax_template_name, context, self.request)
            return JsonResponse(html, safe=False)
        return super(ClientDetailView, self).render_to_response(context, **response_kwargs)


@method_decorator(login_required, name="dispatch")
class MenuListView(SingleTableMixin, FilterView):
    model = Menu
    table_class = MenuTable
    template_name = "dashboard/menu_list.html"
    paginate_by = 25
    paginate_orphans = True
    allow_empty = True
    filterset_class = MenuFilter


@method_decorator(login_required, name="dispatch")
class MenuCreateView(CreateView):
    model = Menu
    form_class = MenuForm
    formset_class = MenuWithSectionsFormSet
    template_name = "dashboard/fragments/create_menu_form.html"
    success_url = reverse_lazy("mainapp:menus-list")

    def get_form(self, form_class=None):
        self.formset = self.formset_class(**self.get_form_kwargs())
        return super(MenuCreateView, self).get_form(form_class=form_class)

    def get_context_data(self, **kwargs):
        context = super(MenuCreateView, self).get_context_data(**kwargs)
        context['formset'] = self.formset
        context['helper'] = SectionsFormsetHelper()
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid() and self.formset.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        if form.is_valid():
            with transaction.atomic():
                self.object = form.save()
                self.formset.instance = self.object
                self.formset.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, formset=self.formset))

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            html = render_to_string(self.template_name, context, self.request)
            return JsonResponse(html, safe=False)
        return super(MenuCreateView, self).render_to_response(context, **response_kwargs)


@method_decorator(login_required, name="dispatch")
class MenuUpdateView(UpdateView):
    model = Menu
    form_class = MenuForm
    formset_class = MenuWithSectionsFormSet
    template_name = "dashboard/fragments/create_menu_form.html"
    success_url = reverse_lazy("mainapp:menus-list")

    def get_form(self, form_class=None):
        self.formset = self.formset_class(**self.get_form_kwargs())
        return super(MenuUpdateView, self).get_form(form_class=form_class)

    def get_context_data(self, **kwargs):
        context = super(MenuUpdateView, self).get_context_data(**kwargs)
        context['formset'] = self.formset
        context['helper'] = SectionsFormsetHelper()
        context['url'] = reverse_lazy("mainapp:menu-update", kwargs={"pk": self.kwargs.get('pk')})
        return context

    def form_valid(self, form):
        if form.is_valid():
            with transaction.atomic():
                self.object = form.save()
                self.formset.instance = self.object
                self.formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid() and self.formset.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, formset=self.formset))

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            html = render_to_string(self.template_name, context, self.request)
            return JsonResponse(html, safe=False)
        return super(MenuUpdateView, self).render_to_response(context, **response_kwargs)


@method_decorator(login_required, name="dispatch")
class MenuDeleteView(DeleteView):
    model = Menu
    success_url = reverse_lazy("mainapp:menus-list")
    template_name = "dashboard/fragments/delete_form.html"
    form_class = DeleteForm

    def get_form(self):
        return self.form_class()

    def get_delete_url(self):
        return reverse("mainapp:menu-delete", kwargs={"pk": self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        return super(MenuDeleteView, self).get_context_data(form=self.get_form(), delete_url=self.get_delete_url(),
                                                            **kwargs)

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            html = render_to_string(self.template_name, context, self.request)
            return JsonResponse(html, safe=False)
        return super(MenuDeleteView, self).render_to_response(context, **response_kwargs)


@method_decorator(login_required, name="dispatch")
class MenuDetailView(DetailView):
    pass


@method_decorator(login_required, name="dispatch")
class FoodListView(SingleTableMixin, FilterView):
    model = Food
    table_class = FoodTable
    template_name = "dashboard/food_list.html"
    paginate_by = 25
    paginate_orphans = True
    allow_empty = True
    filterset_class = FoodFilter


@method_decorator(login_required, name="dispatch")
class FoodCreateView(CreateView):
    model = Food
    form_class = FoodForm
    template_name = "dashboard/fragments/create_food_form.html"
    success_url = reverse_lazy("mainapp:foods-list")

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            html = render_to_string(self.template_name, context, self.request)
            return JsonResponse(html, safe=False)
        return super(FoodCreateView, self).render_to_response(context, **response_kwargs)


@method_decorator(login_required, name="dispatch")
class FoodUpdateView(UpdateView):
    model = Food
    form_class = FoodForm
    template_name = "dashboard/fragments/create_food_form.html"
    success_url = reverse_lazy("mainapp:foods-list")

    def get_context_data(self, **kwargs):
        return super(FoodUpdateView, self).get_context_data(
            url=reverse("mainapp:food-update", kwargs={"pk": self.kwargs.get('pk')}), **kwargs)

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            html = render_to_string(self.template_name, context, self.request)
            return JsonResponse(html, safe=False)
        return super(FoodUpdateView, self).render_to_response(context, **response_kwargs)


@method_decorator(login_required, name="dispatch")
class FoodDeleteView(DeleteView):
    model = Food
    success_url = reverse_lazy("mainapp:foods-list")
    template_name = "dashboard/fragments/delete_form.html"
    form_class = DeleteForm

    def get_form(self):
        return self.form_class()

    def get_delete_url(self):
        return reverse("mainapp:food-delete", kwargs={"pk": self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        return super(FoodDeleteView, self).get_context_data(form=self.get_form(), delete_url=self.get_delete_url(),
                                                            **kwargs)

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            html = render_to_string(self.template_name, context, self.request)
            return JsonResponse(html, safe=False)
        return super(FoodDeleteView, self).render_to_response(context, **response_kwargs)


@method_decorator(login_required, name="dispatch")
class FoodDetailView(DetailView):
    pass


@method_decorator(login_required, name="dispatch")
class ExtraListView(SingleTableMixin, FilterView):
    model = Extra
    table_class = ExtraTable
    template_name = "dashboard/extra_list.html"
    paginate_by = 25
    paginate_orphans = True
    allow_empty = True
    filterset_class = ExtraFilter


@method_decorator(login_required, name="dispatch")
class ExtraCreateView(CreateView):
    model = Extra
    form_class = ExtraForm
    template_name = "dashboard/fragments/create_extra_form.html"
    success_url = reverse_lazy("mainapp:extras-list")

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            html = render_to_string(self.template_name, context, self.request)
            return JsonResponse(html, safe=False)
        return super(ExtraCreateView, self).render_to_response(context, **response_kwargs)


@method_decorator(login_required, name="dispatch")
class ExtraUpdateView(UpdateView):
    model = Extra
    form_class = ExtraForm
    template_name = "dashboard/fragments/create_extra_form.html"
    success_url = reverse_lazy("mainapp:foods-list")

    def get_context_data(self, **kwargs):
        return super(ExtraUpdateView, self).get_context_data(
            url=reverse("mainapp:extra-update", kwargs={"pk": self.kwargs.get('pk')}), **kwargs)

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            html = render_to_string(self.template_name, context, self.request)
            return JsonResponse(html, safe=False)
        return super(ExtraUpdateView, self).render_to_response(context, **response_kwargs)


@method_decorator(login_required, name="dispatch")
class ExtraDeleteView(DeleteView):
    model = Extra
    success_url = reverse_lazy("mainapp:extras-list")
    template_name = "dashboard/fragments/delete_form.html"
    form_class = DeleteForm

    def get_form(self):
        return self.form_class()

    def get_delete_url(self):
        return reverse("mainapp:extra-delete", kwargs={"pk": self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        return super(ExtraDeleteView, self).get_context_data(form=self.get_form(), delete_url=self.get_delete_url(),
                                                             **kwargs)

    def render_to_response(self, context, **response_kwargs):
        if self.request.is_ajax():
            html = render_to_string(self.template_name, context, self.request)
            return JsonResponse(html, safe=False)
        return super(ExtraDeleteView, self).render_to_response(context, **response_kwargs)


@method_decorator(login_required, name="dispatch")
class ExtraDetailView(DetailView):
    pass


@method_decorator(login_required, name="dispatch")
class OrderListView(SingleTableMixin, FilterView):
    model = Order
    table_class = OrderTable
    template_name = "dashboard/order_list.html"
    paginate_by = 25
    paginate_orphans = True
    allow_empty = True
    filterset_class = OrderFilter


@method_decorator(login_required, name="dispatch")
class OrderCreateView(CreateView):
    pass


@method_decorator(login_required, name="dispatch")
class OrderUpdateView(UpdateView):
    pass


@method_decorator(login_required, name="dispatch")
class OrderDeleteView(DeleteView):
    pass


@method_decorator(login_required, name="dispatch")
class OrderDetailView(DetailView):
    model = Order
    template_name = "dashboard/order_details.html"


@method_decorator(login_required, name="dispatch")
class OrderLineListView(ListView):
    pass


@method_decorator(login_required, name="dispatch")
class OrderLineCreateView(CreateView):
    pass


@method_decorator(login_required, name="dispatch")
class OrderLineUpdateView(UpdateView):
    pass


@method_decorator(login_required, name="dispatch")
class OrderLineDeleteView(DeleteView):
    pass


@method_decorator(login_required, name="dispatch")
class OrderLineDetailView(DetailView):
    pass
