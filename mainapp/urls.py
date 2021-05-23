from django.urls import path, include
from rest_framework.routers import SimpleRouter

from mainapp import apis

router = SimpleRouter()
router.register("clients", apis.ClientViewSet, "clients")
router.register("clients/phones", apis.PhoneNumberViewSet, "clients-phones")
router.register("clients/addresses", apis.AddressViewSet, "clients-addresses")
router.register("menus", apis.MenuViewSet, "menus")
router.register("foods", apis.FoodViewSet, "foods")
router.register("extras", apis.ExtraViewSet, "extras")
router.register("compositions", apis.CompositionViewSet, "compositions")
router.register("orders", apis.OrderViewSet, "orders")
router.register("orders/lines", apis.OrderLineViewSet, "orders-lines")

urlpatterns = [
    path("apis/", include(router.urls))
]
