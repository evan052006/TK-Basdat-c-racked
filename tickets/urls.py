from django.urls import path
from . import views

app_name = "tickets"

urlpatterns = [
    path("", views.tickets_list, name="tickets_list"),
    path("create/", views.create_ticket, name="create_ticket"),
    path("delete/", views.delete_ticket, name="delete_ticket"),
]
