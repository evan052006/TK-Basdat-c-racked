from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from accounts.decorators import require_roles
from .queries import orders_db


def _get_user_role(request):
    """Extract role from request or return GUEST"""
    return getattr(request, "user_role", "GUEST")


def _get_context_with_role(request, extra_context=None):
    """Helper to add role to context"""
    context = {"role": _get_user_role(request)}
    if extra_context:
        context.update(extra_context)
    return context


@require_roles("GUEST", "CUSTOMER", "ORGANIZER", "ADMIN")
def orders_list(request):
    """Display orders list with stats and search"""
    try:
        orders = list(orders_db.get_orders())
    except Exception as exc:
        orders = []
        orders_error = str(exc)
    else:
        orders_error = None

    try:
        promotions = list(orders_db.get_promotions())
    except Exception as exc:
        promotions = []
        promotions_error = str(exc)
    else:
        promotions_error = None

    # Calculate stats
    total_order = len(orders)
    total_paid = sum(1 for o in orders if o.get("payment_status") == "PAID")
    total_pending = sum(1 for o in orders if o.get("payment_status") == "PENDING")
    total_revenue = sum(
        float(o.get("total_amount", 0)) for o in orders if o.get("payment_status") == "PAID"
    )

    context = _get_context_with_role(request, {
        "orders": orders,
        "promotions": promotions,
        "orders_error": orders_error,
        "promotions_error": promotions_error,
        "total_order": total_order,
        "total_paid": total_paid,
        "total_pending": total_pending,
        "total_revenue": total_revenue,
    })
    return render(request, "orders/orders_list.html", context)


@require_roles("GUEST", "CUSTOMER", "ORGANIZER", "ADMIN")
def promotions_list(request):
    """Display promotions list with search"""
    try:
        promotions = list(orders_db.get_promotions())
    except Exception as exc:
        promotions = []
        promotions_error = str(exc)
    else:
        promotions_error = None

    # Calculate stats
    total_promo = len(promotions)
    total_usage = sum(int(p.get("usage_count", 0)) for p in promotions)
    total_percentage = sum(1 for p in promotions if p.get("discount_type") == "PERCENTAGE")

    context = _get_context_with_role(request, {
        "promotions": promotions,
        "promotions_error": promotions_error,
        "total_promo": total_promo,
        "total_usage": total_usage,
        "total_percentage": total_percentage,
    })
    return render(request, "orders/promotions_list.html", context)


@require_POST
@require_roles("ADMIN")
def create_order(request):
    """Create new order"""
    try:
        order_date = (request.POST.get("order_date") or "").replace("T", " ")
        payment_status = request.POST.get("payment_status")
        total_amount = request.POST.get("total_amount")
        customer_id = request.POST.get("customer_id")

        orders_db.create_order(
            order_date=order_date,
            payment_status=payment_status,
            total_amount=float(total_amount),
            customer_id=customer_id,
        )

        return redirect("orders:orders_list")
    except Exception:
        return redirect("orders:orders_list")


@require_POST
@require_roles("ADMIN")
def update_order(request):
    """Update existing order"""
    try:
        order_id = request.POST.get("order_id")
        payment_status = request.POST.get("payment_status")

        existing_order = orders_db.get_order(order_id=order_id)
        if not existing_order:
            return redirect("orders:orders_list")

        orders_db.update_order(
            order_id=order_id,
            order_date=existing_order.get("order_date"),
            payment_status=payment_status,
            total_amount=existing_order.get("total_amount"),
            customer_id=existing_order.get("customer_id"),
        )

        return redirect("orders:orders_list")
    except Exception:
        return redirect("orders:orders_list")


@require_POST
@require_roles("ADMIN")
def delete_order(request):
    """Delete existing order"""
    try:
        order_id = request.POST.get("order_id")
        orders_db.delete_order(order_id=order_id)

        return redirect("orders:orders_list")
    except Exception:
        return redirect("orders:orders_list")


@require_POST
@require_roles("ADMIN")
def create_promotion(request):
    """Create new promotion"""
    try:
        promo_code = request.POST.get("promo_code")
        discount_type = request.POST.get("discount_type")
        discount_value = request.POST.get("discount_value")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        usage_limit = request.POST.get("usage_limit", 1)

        orders_db.create_promotion(
            promo_code=promo_code,
            discount_type=discount_type,
            discount_value=float(discount_value),
            start_date=start_date,
            end_date=end_date,
            usage_limit=int(usage_limit),
        )

        return redirect("orders:promotions_list")
    except Exception:
        return redirect("orders:promotions_list")


@require_POST
@require_roles("ADMIN")
def update_promotion(request):
    """Update existing promotion"""
    try:
        promotion_id = request.POST.get("promotion_id")
        promo_code = request.POST.get("promo_code")
        discount_type = request.POST.get("discount_type")
        discount_value = request.POST.get("discount_value")
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date")
        usage_limit = request.POST.get("usage_limit", 1)

        orders_db.update_promotion(
            promotion_id=promotion_id,
            promo_code=promo_code,
            discount_type=discount_type,
            discount_value=float(discount_value),
            start_date=start_date,
            end_date=end_date,
            usage_limit=int(usage_limit),
        )

        return redirect("orders:promotions_list")
    except Exception:
        return redirect("orders:promotions_list")


@require_POST
@require_roles("ADMIN")
def delete_promotion(request):
    """Delete existing promotion"""
    try:
        promotion_id = request.POST.get("promotion_id")
        orders_db.delete_promotion(promotion_id=promotion_id)

        return redirect("orders:promotions_list")
    except Exception:
        return redirect("orders:promotions_list")

def checkout_dummy(request):
    """
    Dummy view for checkout screenshot (Customer role).
    """
    context = {"user_role": "CUSTOMER", "role": "CUSTOMER"}
    return render(request, "orders/checkout.html", context)
