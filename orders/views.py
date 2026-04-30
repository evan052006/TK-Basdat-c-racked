from django.shortcuts import render
from .queries import orders_db


def orders_list(request):
    try:
        orders = orders_db.get_orders()
    except Exception as exc:
        orders = []
        orders_error = str(exc)
    else:
        orders_error = None

    try:
        promotions = orders_db.get_promotions()
    except Exception as exc:
        promotions = []
        promotions_error = str(exc)
    else:
        promotions_error = None

    context = {
        "orders": orders,
        "promotions": promotions,
        "orders_error": orders_error,
        "promotions_error": promotions_error,
    }
    return render(request, "orders/orders_list.html", context)
