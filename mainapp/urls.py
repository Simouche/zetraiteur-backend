from django.urls import path, include
from rest_framework.routers import SimpleRouter

from mainapp import apis, views

app_name = "mainapp"

router = SimpleRouter()
router.register("clients", apis.ClientViewSet, "apis-clients")
router.register("clients/phones", apis.PhoneNumberViewSet, "apis-clients-phones")
router.register("clients/addresses", apis.AddressViewSet, "apis-clients-addresses")
# router.register("menus", apis.MenuViewSet, "apis-menus")
# router.register("foods", apis.FoodViewSet, "apis-foods")
# router.register("extras", apis.ExtraViewSet, "apis-extras")
router.register("compositions", apis.CompositionViewSet, "apis-compositions")
router.register("orders", apis.OrderViewSet, "apis-orders")
router.register("orders/lines", apis.OrderLineViewSet, "apis-orders-lines")

urlpatterns = [
    path("", views.Dashboard.as_view(), name="dashboard"),

    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),

    path("clients/list/", views.ClientListView.as_view(), name="clients-list"),
    path("clients/<int:pk>/delete/", views.ClientDeleteView.as_view(), name="client-delete"),
    path("clients/<int:pk>/details/", views.ClientDetailView.as_view(), name="client-details"),

    path("menus/create/", views.MenuCreateView.as_view(), name="menu-create"),
    path("menus/list/", views.MenuListView.as_view(), name="menus-list"),
    path("menus/<int:pk>/delete/", views.MenuDeleteView.as_view(), name="menu-delete"),
    path("menus/<int:pk>/details/", views.MenuDetailView.as_view(), name="menu-details"),
    path("menus/<int:pk>/update/", views.MenuUpdateView.as_view(), name="menu-update"),

    path("foods/create/", views.FoodCreateView.as_view(), name="food-create"),
    path("foods/list/", views.FoodListView.as_view(), name="foods-list"),
    path("foods/<int:pk>/delete/", views.FoodDeleteView.as_view(), name="food-delete"),
    path("foods/<int:pk>/details/", views.FoodDetailView.as_view(), name="food-details"),
    path("foods/<int:pk>/update/", views.FoodUpdateView.as_view(), name="food-update"),

    path("extras/create/", views.ExtraCreateView.as_view(), name="extra-create"),
    path("extras/list/", views.ExtraListView.as_view(), name="extras-list"),
    path("extras/<int:pk>/delete/", views.ExtraDeleteView.as_view(), name="extra-delete"),
    path("extras/<int:pk>/details/", views.ExtraDetailView.as_view(), name="extra-details"),
    path("extras/<int:pk>/update/", views.ExtraUpdateView.as_view(), name="extra-update"),

    path("orders/list/", views.OrderListView.as_view(), name="orders-list"),
    path("orders/<int:pk>/delete/", views.OrderDeleteView.as_view(), name="order-delete"),
    path("orders/<int:pk>/details/", views.OrderDetailView.as_view(), name="order-details"),
    path("orders/<int:pk>/update/", views.OrderUpdateView.as_view(), name="order-update"),

    path("apis/login/", apis.LoginApi.as_view()),
    path("apis/extras/", apis.ExtrasListView.as_view()),
    path("apis/menus/", apis.MenuListView.as_view()),
    path("apis/foods/", apis.FoodListView.as_view()),
    path("apis/", include(router.urls))
]
