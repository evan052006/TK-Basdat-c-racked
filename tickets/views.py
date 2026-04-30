import uuid
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from accounts.decorators import require_roles
from .queries import tickets_db


def _get_user_role(request):
    """Extract role from request or return GUEST"""
    return getattr(request, "user_role", "GUEST")


@require_roles("GUEST", "CUSTOMER", "ORGANIZER", "ADMIN")
def tickets_list(request):
    """Display tickets list with stats and search"""
    role = _get_user_role(request)

    try:
        tickets = list(tickets_db.get_tickets())
    except Exception as exc:
        tickets = []
        print(f"tickets error: {exc}")

    # Stats
    total_ticket = len(tickets)
    total_valid = sum(1 for t in tickets if t.get("payment_status") == "PAID")
    total_used = 0
    try:
        total_used = tickets_db.get_used_ticket_count()
    except Exception:
        pass

    # For create modal dropdowns (Admin/Organizer only)
    orders = []
    categories = []
    if role in ("ADMIN", "ORGANIZER"):
        try:
            orders = list(tickets_db.get_all_orders())
        except Exception:
            pass
        try:
            categories = list(tickets_db.get_ticket_categories())
        except Exception:
            pass

    context = {
        "role": role,
        "tickets": tickets,
        "total_ticket": total_ticket,
        "total_valid": total_valid,
        "total_used": total_used,
        "orders": orders,
        "categories": categories,
    }
    return render(request, "tickets/tickets_list.html", context)


@require_POST
@require_roles("ADMIN", "ORGANIZER")
def create_ticket(request):
    """Create a new ticket"""
    try:
        torder_id = request.POST.get("torder_id")
        tcategory_id = request.POST.get("tcategory_id")

        # Auto-generate code
        code = f"TTK-{uuid.uuid4().hex[:8].upper()}"

        tickets_db.create_ticket(
            code=code,
            tcategory_id=tcategory_id,
            torder_id=torder_id,
        )
        return redirect("tickets:tickets_list")
    except Exception as e:
        print(f"create_ticket error: {e}")
        return redirect("tickets:tickets_list")


@require_POST
@require_roles("ADMIN")
def delete_ticket(request):
    """Delete a ticket (removes seat relationship first)"""
    try:
        ticket_id = request.POST.get("ticket_id")

        # Remove seat relationship first
        try:
            tickets_db.delete_ticket(ticket_id=ticket_id)
        except Exception:
            pass

        # Delete the ticket record
        tickets_db.delete_ticket_record(ticket_id=ticket_id)

        return redirect("tickets:tickets_list")
    except Exception as e:
        print(f"delete_ticket error: {e}")
        return redirect("tickets:tickets_list")
