from django.shortcuts import render, redirect
from django.contrib import messages
from common.decorators import staff_required
from owner.models import staff, product, category, section
from django.conf import settings
from owner.utils import normalize_image_path
from django.db.models import Count, Q

def staff_login(request):

    if request.method == "POST":

        username = request.POST.get("username", "").strip()

        password = request.POST.get("password", "").strip()

        try:

            staff_obj = staff.objects.get(
                username=username,
                password=password
            )

        except staff.DoesNotExist:

            messages.error(
                request,
                "Invalid Username or Password."
            )

            return redirect("staff_login")

        if not staff_obj.is_active:

            messages.error(
                request,
                "Your account is inactive."
            )

            return redirect("staff_login")

        request.session["staff_id"] = staff_obj.id

        request.session["staff_name"] = staff_obj.staff_name

        request.session["staff_username"] = staff_obj.username

        return redirect("staff_dashboard")

    return render(
        request,
        "staff_login.html"
    )

@staff_required
def staff_dashboard(request):

    total_products = product.objects.count()

    active_products = product.objects.filter(
        is_active=True
    ).count()

    low_stock_products = product.objects.filter(
        quantity__lte=10,
        is_active=True
    ).count()

    total_sections = section.objects.count()

    context = {

        "staff_name": request.session.get("staff_name"),

        "total_products": total_products,

        "active_products": active_products,

        "low_stock_products": low_stock_products,

        "total_sections": total_sections,

    }

    return render(
        request,
        "staff_dashboard.html",
        context
    )

# ---------------- view product in staff dashboard ----------------

@staff_required
def staff_product(request):

    products = (
        product.objects
        .select_related("category", "section")
        .order_by("product_name")
    )
    for p in products:
        p.product_image = normalize_image_path(
        p.product_image
    )

    search = request.GET.get("search", "").strip()
    category_id = request.GET.get("category")
    section_id = request.GET.get("section")

    if search:
        products = products.filter(
            product_name__icontains=search
        )

    if category_id:
        products = products.filter(
            category_id=category_id
        )

    if section_id:
        products = products.filter(
            section_id=section_id
        )

    context = {
        "products": products,
        "categories": category.objects.all(),
        "sections": section.objects.all(),
        "search": search,
        "selected_category": category_id,
        "selected_section": section_id,
    }

    return render(
        request,
        "staff_product.html",
        context
    )

# ---------------- stock update in dashboard ----------------

@staff_required
def update_stock(request,id):

    p = product.objects.get(id=id)

    if request.method=="POST":

        quantity=request.POST.get("quantity")

        p.quantity=quantity

        p.save()

        messages.success(

            request,

            "Stock Updated Successfully."

        )

    return redirect("staff_product")

# ---------------- staff category ----------------

@staff_required
def staff_category(request):

    categories = (
        category.objects
        .annotate(
            total_products=Count("product")
        )
        .order_by("category_name")
    )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    if search:

        categories = categories.filter(
            category_name__icontains=search
        )

    total_categories = categories.count()

    context = {

        "categories": categories,

        "search": search,

        "total_categories": total_categories,

    }

    return render(
        request,
        "staff_category.html",
        context
    )


# ---------------- staff section ----------------

@staff_required
def staff_section(request):

    sections = (
        section.objects
        .annotate(
            total_products=Count("product")
        )
        .order_by("section_name")
    )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    if search:

        sections = sections.filter(
            Q(section_name__icontains=search) |
            Q(rack_number__icontains=search)
        )

    total_sections = sections.count()

    context = {

        "sections": sections,

        "search": search,

        "total_sections": total_sections,

    }

    return render(

        request,

        "staff_section.html",

        context

    )
    
@staff_required
def staff_logout(request):

    request.session.flush()

    return redirect("staff_login")