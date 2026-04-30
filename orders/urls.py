from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("", views.orders_list, name="orders_list"),
    path("promotions/", views.promotions_list, name="promotions_list"),
    
    # Orders CRUD
    path("checkout/", views.checkout_dummy, name="checkout_dummy"),
    path("create/", views.create_order, name="create_order"),
    path("update/", views.update_order, name="update_order"),
    path("delete/", views.delete_order, name="delete_order"),
    
    # Promotions CRUD
    path("promo/create/", views.create_promotion, name="create_promotion"),
    path("promo/update/", views.update_promotion, name="update_promotion"),
    path("promo/delete/", views.delete_promotion, name="delete_promotion"),
]
