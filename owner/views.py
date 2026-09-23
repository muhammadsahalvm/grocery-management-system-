from django.http import request
from django.shortcuts import render, redirect, get_object_or_404

from common.decorators import owner_required
from .models import customer, delivery_area, feedback, order, order_item, owner, category, section, product , staff
from django.contrib import messages


import os
from django.core.files.storage import FileSystemStorage
from django.shortcuts import get_object_or_404

from .helpers import generate_staff_username

from .utils import normalize_image_path

from django.db.models import Avg, Count, Sum, Q
from django.utils import timezone

from decimal import Decimal, InvalidOperation
# ---------------- Owner Registration ----------------
def owner_register(request):

    if request.method == "POST":

        name = request.POST.get("name")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Check if username already exists
        if owner.objects.filter(Username=username).exists():

            return render(request, "owner_registration.html", {
                "error": "Username already exists"
            })

        # Check if passwords match
        if password != confirm_password:

            return render(request, "owner_registration.html", {
                "error": "Password and Confirm Password do not match"
            })

        # Save owner
        owner.objects.create(
            Name=name,
            Username=username,
            Password=password
        )

        return redirect("owner_login")

    return render(request, "owner_registration.html")

# ---------------- Owner Login ----------------

def owner_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        owner_data = owner.objects.filter(
            Username=username,
            Password=password
        ).first()

        if owner_data:
            request.session["owner_id"] = owner_data.id
            request.session["owner_name"] = owner_data.Name

            return redirect("owner_dashboard")

        return render(request, "owner_login.html", {
            "error": "Invalid Username or Password"
        })

    return render(request, "owner_login.html")


# ---------------- Owner Dashboard ----------------

@owner_required
def owner_dashboard(request):

    today = timezone.localdate()
    today_orders = order.objects.filter(created_at__date=today)
    visible_feedback = feedback.objects.filter(
        is_visible=True,
    ).select_related("customer").order_by("-created_at")

    dashboard_stats = {
        "today_orders": today_orders.count(),
        "pending_orders": order.objects.filter(status="pending").count(),
        "revenue_today": today_orders.aggregate(
            total=Sum("total_amount")
        )["total"] or 0,
        "products_available": product.objects.filter(
            is_active=True,
            quantity__gt=0,
        ).count(),
        "customers_count": customer.objects.count(),
        "feedback_count": visible_feedback.count(),
        "feedback_rating": visible_feedback.aggregate(
            average=Avg("rating")
        )["average"],
        "latest_feedback": visible_feedback.first(),
        "recent_orders": order.objects.select_related(
            "customer",
        ).order_by("-created_at")[:5],
        "low_stock_products": product.objects.filter(
            is_active=True,
            quantity__lte=10,
        ).order_by("quantity", "product_name")[:3],
    }

    return render(request, "dashboard_home.html", dashboard_stats)

# ---------------- Category Management ----------------

@owner_required
def owner_category(request):


    # Add Category
    if request.method == "POST":

        category_name = request.POST.get("category_name")
        category_image = request.FILES.get("category_image")

        # Check duplicate category
        if category.objects.filter(category_name__iexact=category_name).exists():
            messages.error(request, "Category already exists.")
            return redirect("owner_category")

        image_path = ""

        # Save Image
        if category_image:

            fs = FileSystemStorage(location="media/category_images")

            filename = fs.save(category_image.name, category_image)

            image_path = os.path.join("category_images", filename)

        # Save Category
        category.objects.create(
            category_name=category_name,
            category_image=image_path
        )

        messages.success(request, "Category added successfully.")

        return redirect("owner_category")

    # Display Categories
    categories = category.objects.all().order_by("category_name")

    context = {
        "categories": categories
    }

    return render(request, "owner_category.html", context)

# ---------------- Category delete ----------------
@owner_required
def delete_category(request, id):

    cat = get_object_or_404(
        category,
        id=id
    )

    product_count = product.objects.filter(
        category=cat
    ).count()

    if product_count > 0:

        messages.error(
            request,
            f"Cannot delete this category because "
            f"{product_count} product(s) are assigned to it."
        )

        return redirect("owner_category")

    if cat.category_image:

        image_path = os.path.join(
            "media",
            cat.category_image
        )

        if os.path.exists(image_path):

            os.remove(image_path)

    cat.delete()

    messages.success(
        request,
        "Category deleted successfully."
    )

    return redirect("owner_category")

# ---------------- Category edit ----------------

@owner_required
def edit_category(request, id):

    cat = category.objects.get(id=id)

    if request.method == "POST":

        cat.category_name = request.POST.get("category_name")

        new_image = request.FILES.get("category_image")

        if new_image:

            # Delete old image
            if cat.category_image:

                old_image = os.path.join("media", cat.category_image)

                if os.path.exists(old_image):
                    os.remove(old_image)

            fs = FileSystemStorage(location="media/category_images")

            filename = fs.save(new_image.name, new_image)

            cat.category_image = os.path.join("category_images", filename)

        cat.save()

        messages.success(request, "Category updated successfully.")

        return redirect("owner_category")

    return render(request, "edit_category.html", {"cat": cat})

# ---------------- Logout ----------------

def owner_logout(request):

    request.session.flush()

    return redirect("owner_login")

# ---------------- owner section ----------------

@owner_required
def owner_section(request):

    sections = section.objects.all().order_by("section_name")

    return render(
        request,
        "owner_section.html",
        {
            "sections": sections
        }
    )
# ---------------- add section ----------------

@owner_required
def add_section(request):

    if request.method == "POST":

        section_name = request.POST.get("section_name", "").strip()
        rack_number = request.POST.get("rack_number", "").strip()

        if not section_name or not rack_number:
            messages.error(request, "All fields are required.")
            return redirect("owner_section")

        if section.objects.filter(section_name__iexact=section_name).exists():
            messages.error(request, "Section name already exists.")
            return redirect("owner_section")

        if section.objects.filter(rack_number__iexact=rack_number).exists():
            messages.error(request, "Rack number already exists.")
            return redirect("owner_section")

        section.objects.create(
            section_name=section_name,
            rack_number=rack_number
        )

        messages.success(request, "Section added successfully.")

    return redirect("owner_section")

# ---------------- delete section ----------------

@owner_required
def delete_section(request, id):

    selected_section = get_object_or_404(
        section,
        id=id
    )

    product_count = product.objects.filter(
        section=selected_section
    ).count()

    if product_count > 0:

        messages.error(
            request,
            f"Cannot delete this section because "
            f"{product_count} product(s) are assigned to it."
        )

        return redirect("owner_section")

    selected_section.delete()

    messages.success(
        request,
        "Section deleted successfully."
    )

    return redirect("owner_section")

# ---------------- edit section ----------------
@owner_required
def edit_section(request, id):

    section_item = get_object_or_404(
        section,
        id=id
    )


    if request.method == "POST":

        section_name = request.POST.get(
            "section_name",
            ""
        ).strip()

        rack_number = request.POST.get(
            "rack_number",
            ""
        ).strip()


        # ==========================================
        # VALIDATE SECTION NAME
        # ==========================================

        if section.objects.exclude(
            id=id
        ).filter(
            section_name__iexact=section_name
        ).exists():

            messages.error(
                request,
                "Section name already exists."
            )

            return redirect(
                "owner_section"
            )


        # ==========================================
        # VALIDATE RACK NUMBER
        # ==========================================

        if section.objects.exclude(
            id=id
        ).filter(
            rack_number__iexact=rack_number
        ).exists():

            messages.error(
                request,
                "Rack number already exists."
            )

            return redirect(
                "owner_section"
            )


        # ==========================================
        # UPDATE SECTION
        # ==========================================

        section_item.section_name = section_name

        section_item.rack_number = rack_number

        section_item.save()


        messages.success(
            request,
            "Section updated successfully."
        )


    return redirect(
        "owner_section"
    )
# ---------------- display product ----------------

@owner_required 
def owner_product(request):

    # Add Product
    if request.method == "POST":

        product_name = request.POST.get("product_name").strip()

        category_id = request.POST.get("category")

        section_id = request.POST.get("section")

        description = request.POST.get("description")

        actual_price = request.POST.get("actual_price")

        offer_price = request.POST.get("offer_price")

        quantity = request.POST.get("quantity")

        product_image = request.FILES.get("product_image")


        # Duplicate Product Check
        if product.objects.filter(product_name__iexact=product_name).exists():

            messages.error(request, "Product already exists.")

            return redirect("owner_product")


        # Price Validation
        if offer_price:

            if float(offer_price) > float(actual_price):

                messages.error(
                    request,
                    "Offer price cannot be greater than Actual Price."
                )

                return redirect("owner_product")


        image_path = ""

        # Save Image
        if product_image:

            fs = FileSystemStorage(
                location="media/product_images"
            )

            filename = fs.save(
                product_image.name,
                product_image
            )

            image_path = f"product_images/{filename}"


        product.objects.create(

            product_name=product_name,

            category=category.objects.get(id=category_id),

            section=section.objects.get(id=section_id),

            product_image=image_path,

            description=description,

            actual_price=actual_price,

            offer_price=offer_price if offer_price else None,

            quantity=quantity

        )

        messages.success(
            request,
            "Product Added Successfully."
        )

        return redirect("owner_product")

    # Fetch data
    categories = category.objects.all().order_by("category_name")

    sections = section.objects.all().order_by("section_name")

    products = product.objects.select_related(
        "category",
        "section"
    ).order_by("product_name")
    for p in products:
        p.product_image = normalize_image_path(
        p.product_image
    )

    # Statistics
    total_products = products.count()

    active_products = products.filter(
        is_active=True
    ).count()

    inactive_products = products.filter(
        is_active=False
    ).count()

    low_stock_products = products.filter(
        quantity__lte=10
    ).count()

    # Context
    context = {

        "categories": categories,

        "sections": sections,

        "products": products,

        "total_products": total_products,

        "active_products": active_products,

        "inactive_products": inactive_products,

        "low_stock_products": low_stock_products,

    }

    return render(
        request,
        "owner_product.html",
        context
    )

# ---------------- Delete Product ----------------
@owner_required
def delete_product(request, id):

    pro = product.objects.get(id=id)

    # Delete image from media folder
    if pro.product_image:

        image_path = os.path.join("media", pro.product_image)

        if os.path.exists(image_path):
            os.remove(image_path)

    pro.delete()

    messages.success(request, "Product deleted successfully.")

    return redirect("owner_product")

# ---------------- Edit Product ----------------
@owner_required
def edit_product(request, id):

    pro = get_object_or_404(product, id=id)

    if request.method == "POST":

        product_name = request.POST.get("product_name").strip()

        category_id = request.POST.get("category")

        section_id = request.POST.get("section")

        description = request.POST.get("description")

        actual_price = request.POST.get("actual_price")

        offer_price = request.POST.get("offer_price")

        quantity = request.POST.get("quantity")

        new_image = request.FILES.get("product_image")

        # Duplicate product check
        if product.objects.exclude(id=id).filter(
            product_name__iexact=product_name
        ).exists():

            messages.error(request, "Product already exists.")

            return redirect("owner_product")

        # Price validation
        if offer_price:

            if float(offer_price) > float(actual_price):

                messages.error(
                    request,
                    "Offer price cannot be greater than Actual Price."
                )

                return redirect("owner_product")

        pro.product_name = product_name

        pro.category = category.objects.get(id=category_id)

        pro.section = section.objects.get(id=section_id)

        pro.description = description

        pro.actual_price = actual_price

        pro.offer_price = offer_price if offer_price else None

        pro.quantity = quantity

        # Replace image
        if new_image:

            if pro.product_image:

                old_image = os.path.join("media", pro.product_image)

                if os.path.exists(old_image):
                    os.remove(old_image)

            fs = FileSystemStorage(location="media/product_images")

            filename = fs.save(new_image.name, new_image)

            pro.product_image = os.path.join(
                "product_images",
                filename
            )

        pro.save()

        messages.success(request, "Product updated successfully.")

        return redirect("owner_product")

        categories = category.objects.all().order_by(
        "category_name"
    )

    sections = section.objects.all().order_by(
        "section_name"
    )

    return render(
        request,
        "edit_product.html",
        {
            "product": pro,
            "categories": category,
            "sections": sections,
        }
    )

# # ---------- Product Statistics ----------

# total_products = product.objects.count()

# active_products = product.objects.filter(
#     is_active=True
# ).count()

# inactive_products = product.objects.filter(
#     is_active=False
# ).count()

# low_stock_products = product.objects.filter(
#     quantity__lte=10
# ).count()

# ---------- Product isactive button ----------
@owner_required
def toggle_product_status(request,id):
    pro = product.objects.get(id=id)
    pro.is_active = not pro.is_active
    pro.save()
    return redirect("owner_product")

# ---------- staff section ----------
    
@owner_required
def owner_staff(request):
    if request.method == "POST":
        staff_name = request.POST.get(
            "staff_name",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        ).strip()

        salary = request.POST.get("salary")

        if not staff_name or not password or not salary:

            messages.error(
                request,
                "Please fill in all staff fields."
            )

            return redirect("owner_staff")

        if float(salary) <= 0:

            messages.error(
                request,
                "Salary must be greater than zero."
            )

            return redirect("owner_staff")

        if staff.objects.filter(
            staff_name__iexact=staff_name
        ).exists():

            messages.error(
                request,
                "Staff already exists."
            )

            return redirect("owner_staff")

        username = generate_staff_username()

        staff.objects.create(

            staff_name=staff_name,

            username=username,

            password=password,

            salary=salary

        )

        messages.success(
            request,
            "Staff added successfully."
        )

        return redirect("owner_staff")

    staffs = staff.objects.all().order_by("staff_name")

    total_staff = staffs.count()

    active_staff = staffs.filter(
        is_active=True
    ).count()

    inactive_staff = staffs.filter(
        is_active=False
    ).count()

    context = {
        "staffs": staffs,
        "total_staff": total_staff,
        "active_staff": active_staff,
        "inactive_staff": inactive_staff,
    }

    return render(
        request,
        "owner_staff.html",
        context
    )

@owner_required
def edit_staff(request, id):

    s = staff.objects.get(id=id)

    if request.method == "POST":

        staff_name = request.POST.get("staff_name").strip()

        password = request.POST.get("password").strip()

        salary = request.POST.get("salary")

        is_active = request.POST.get("is_active") == "True"

        if not staff_name or not password or not salary:

            messages.error(
                request,
                "Please fill all fields."
            )

            return redirect("owner_staff")

        if float(salary) <= 0:

            messages.error(
                request,
                "Salary must be greater than zero."
            )

            return redirect("owner_staff")

        if staff.objects.exclude(id=id).filter(
            staff_name__iexact=staff_name
        ).exists():

            messages.error(
                request,
                "Staff already exists."
            )

            return redirect("owner_staff")

        s.staff_name = staff_name

        s.password = password

        s.salary = salary

        s.is_active = is_active

        s.save()

        messages.success(
            request,
            "Staff updated successfully."
        )

        return redirect("owner_staff")

    
@owner_required
def delete_staff(request, id):

    s = staff.objects.get(id=id)

    s.delete()

    messages.success(
        request,
        "Staff deleted successfully."
    )

    return redirect("owner_staff")

# ---------- is active toggle btn ----------

@owner_required
def toggle_staff_status(request, id):

    s = staff.objects.get(id=id)

    s.is_active = not s.is_active

    s.save()

    return redirect("owner_staff")

    # ==========================================
# CUSTOMER MANAGEMENT
# ==========================================

@owner_required
def owner_customer(request):

    customers = (
        customer.objects
        .annotate(
            total_orders=Count("orders", distinct=True),
            total_spending=Sum("orders__total_amount")
        )
        .order_by("-created_at")
    )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    status = request.GET.get(
        "status",
        ""
    ).strip()


    # Search

    if search:

        customers = customers.filter(
            Q(name__icontains=search) |
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )


    # Status filter

    if status == "active":

        customers = customers.filter(
            is_active=True
        )

    elif status == "inactive":

        customers = customers.filter(
            is_active=False
        )


    # Statistics

    total_customers = customer.objects.count()

    active_customers = customer.objects.filter(
        is_active=True
    ).count()

    inactive_customers = customer.objects.filter(
        is_active=False
    ).count()


    context = {

        "customers": customers,

        "search": search,

        "selected_status": status,

        "total_customers": total_customers,

        "active_customers": active_customers,

        "inactive_customers": inactive_customers,

    }

    return render(
        request,
        "owner_customer.html",
        context
    )

# ==========================================
# TOGGLE CUSTOMER STATUS
# ==========================================

@owner_required
def toggle_customer_status(request, id):

    selected_customer = get_object_or_404(
        customer,
        id=id
    )

    selected_customer.is_active = not selected_customer.is_active

    selected_customer.save()

    if selected_customer.is_active:

        messages.success(
            request,
            f"{selected_customer.name} has been activated."
        )

    else:

        messages.success(
            request,
            f"{selected_customer.name} has been deactivated."
        )

    return redirect("owner_customer")

# ==========================================
# CUSTOMER DETAILS
# ==========================================

@owner_required
def customer_details(request, id):

    selected_customer = get_object_or_404(
        customer,
        id=id
    )

    orders = (
        order.objects
        .filter(customer=selected_customer)
        .order_by("-created_at")
    )

    total_orders = orders.count()

    total_spending = (
        orders
        .exclude(status="cancelled")
        .aggregate(
            total=Sum("total_amount")
        )["total"]
        or 0
    )

    context = {

        "customer": selected_customer,

        "orders": orders,

        "total_orders": total_orders,

        "total_spending": total_spending,

    }

    return render(
        request,
        "customer_details.html",
        context
    ) 

# ==========================================
# ORDER MANAGEMENT
# ==========================================

@owner_required
def owner_order(request):

    orders = (
        order.objects
        .select_related("customer","delivery_area")
        .prefetch_related("items")
        .order_by("-created_at")
    )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    status = request.GET.get(
        "status",
        ""
    ).strip()

    payment_status = request.GET.get(
        "payment_status",
        ""
    ).strip()


    # Search

    if search:

        orders = orders.filter(
            Q(order_number__icontains=search) |
            Q(customer__name__icontains=search) |
            Q(customer__username__icontains=search) |
            Q(customer__phone__icontains=search)
        )


    # Order status

    if status:

        orders = orders.filter(
            status=status
        )


    # Payment status

    if payment_status:

        orders = orders.filter(
            payment_status=payment_status
        )


    # Statistics

    total_orders = order.objects.count()

    pending_orders = order.objects.filter(
        status="pending"
    ).count()

    delivered_orders = order.objects.filter(
        status="delivered"
    ).count()

    cancelled_orders = order.objects.filter(
        status="cancelled"
    ).count()


    context = {

        "orders": orders,

        "search": search,

        "selected_status": status,

        "selected_payment_status": payment_status,

        "total_orders": total_orders,

        "pending_orders": pending_orders,

        "delivered_orders": delivered_orders,

        "cancelled_orders": cancelled_orders,

        "status_choices": order.STATUS_CHOICES,

        "payment_status_choices":
            order.PAYMENT_STATUS_CHOICES,

    }


    return render(
        request,
        "owner_order.html",
        context
    )

# ==========================================
# ORDER DETAILS
# ==========================================

@owner_required
def order_details(request, id):

    selected_order = get_object_or_404(
        order.objects.select_related("customer","delivery_area"),
        id=id
    )

    items = (
        order_item.objects
        .filter(order=selected_order)
        .select_related("product")
    )

    context = {

        "order": selected_order,

        "items": items,

        "status_choices": order.STATUS_CHOICES,

    }

    return render(
        request,
        "order_details.html",
        context
    )

# ==========================================
# UPDATE ORDER STATUS
# ==========================================

@owner_required
def update_order_status(request, id):

    selected_order = get_object_or_404(
        order,
        id=id
    )

    if request.method != "POST":

        return redirect(
            "order_details",
            id=id
        )

    new_status = request.POST.get(
        "status",
        ""
    ).strip()


    valid_statuses = dict(
        order.STATUS_CHOICES
    )


    if new_status not in valid_statuses:

        messages.error(
            request,
            "Invalid order status."
        )

        return redirect(
            "order_details",
            id=id
        )


    current_status = selected_order.status


    # Prevent changing completed/cancelled orders

    if current_status in [
        "delivered",
        "cancelled"
    ]:

        messages.error(
            request,
            "This order can no longer be updated."
        )

        return redirect(
            "order_details",
            id=id
        )


    selected_order.status = new_status

    selected_order.save(
        update_fields=[
            "status",
            "updated_at"
        ]
    )


    messages.success(
        request,
        f"Order {selected_order.order_number} "
        f"status updated to "
        f"{valid_statuses[new_status]}."
    )


    return redirect(
        "order_details",
        id=id
    )

# ==========================================
# FEEDBACK MANAGEMENT
# ==========================================

@owner_required
def owner_feedback(request):

    feedbacks = (
        feedback.objects
        .select_related(
            "customer",
            "product"
        )
        .order_by("-created_at")
    )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    rating = request.GET.get(
        "rating",
        ""
    ).strip()

    visibility = request.GET.get(
        "visibility",
        ""
    ).strip()


    # Search

    if search:

        feedbacks = feedbacks.filter(

            Q(customer__name__icontains=search) |

            Q(customer__username__icontains=search) |

            Q(product__product_name__icontains=search) |

            Q(feedback__icontains=search)

        )


    # Rating filter

    if rating:

        try:

            rating_value = int(rating)

            if 1 <= rating_value <= 5:

                feedbacks = feedbacks.filter(
                    rating=rating_value
                )

        except ValueError:

            pass


    # Visibility filter

    if visibility == "visible":

        feedbacks = feedbacks.filter(
            is_visible=True
        )

    elif visibility == "hidden":

        feedbacks = feedbacks.filter(
            is_visible=False
        )


    # Statistics

    total_feedback = feedback.objects.count()

    visible_feedback = feedback.objects.filter(
        is_visible=True
    ).count()

    hidden_feedback = feedback.objects.filter(
        is_visible=False
    ).count()


    context = {

        "feedbacks": feedbacks,

        "search": search,

        "selected_rating": rating,

        "selected_visibility": visibility,

        "total_feedback": total_feedback,

        "visible_feedback": visible_feedback,

        "hidden_feedback": hidden_feedback,

    }


    return render(
        request,
        "owner_feedback.html",
        context
    )

# ==========================================
# TOGGLE FEEDBACK VISIBILITY
# ==========================================

@owner_required
def toggle_feedback_visibility(request, id):

    selected_feedback = get_object_or_404(
        feedback,
        id=id
    )

    selected_feedback.is_visible = (
        not selected_feedback.is_visible
    )

    selected_feedback.save(
        update_fields=[
            "is_visible"
        ]
    )


    if selected_feedback.is_visible:

        messages.success(
            request,
            "Feedback is now visible."
        )

    else:

        messages.success(
            request,
            "Feedback has been hidden."
        )


    return redirect(
        "owner_feedback"
    )

# ==========================================
# DELIVERY AREA MANAGEMENT
# ==========================================

@owner_required
def owner_delivery_area(request):

    areas = (
        delivery_area.objects
        .order_by("locality")
    )

    search = request.GET.get(
        "search",
        ""
    ).strip()

    if search:

        areas = areas.filter(
            Q(locality__icontains=search) |
            Q(pincode__icontains=search)
        )

    total_areas = delivery_area.objects.count()

    available_areas = delivery_area.objects.filter(
        is_available=True
    ).count()

    unavailable_areas = delivery_area.objects.filter(
        is_available=False
    ).count()

    context = {

        "areas": areas,

        "search": search,

        "total_areas": total_areas,

        "available_areas": available_areas,

        "unavailable_areas": unavailable_areas,

    }

    return render(
        request,
        "owner_delivery_area.html",
        context
    )

##add delivary area

@owner_required
def add_delivery_area(request):

    if request.method == "POST":

        locality = request.POST.get(
            "locality",
            ""
        ).strip()

        pincode = request.POST.get(
            "pincode",
            ""
        ).strip()

        delivery_charge = request.POST.get(
            "delivery_charge",
            "0"
        ).strip()

        is_available = (
            request.POST.get("is_available")
            == "on"
        )


        if not locality:

            messages.error(
                request,
                "Locality is required."
            )

            return redirect(
                "owner_delivery_area"
            )


        if not pincode:

            messages.error(
                request,
                "Pincode is required."
            )

            return redirect(
                "owner_delivery_area"
            )


        if not pincode.isdigit():

            messages.error(
                request,
                "Pincode must contain only numbers."
            )

            return redirect(
                "owner_delivery_area"
            )


        if delivery_area.objects.filter(
            pincode=pincode
        ).exists():

            messages.error(
                request,
                "This pincode already exists."
            )

            return redirect(
                "owner_delivery_area"
            )


        try:

            delivery_charge = float(
                delivery_charge
            )

            if delivery_charge < 0:

                raise ValueError

        except (ValueError, TypeError):

            messages.error(
                request,
                "Enter a valid delivery charge."
            )

            return redirect(
                "owner_delivery_area"
            )


        delivery_area.objects.create(

            locality=locality,

            pincode=pincode,

            delivery_charge=delivery_charge,

            is_available=is_available

        )


        messages.success(
            request,
            "Delivery area added successfully."
        )


        return redirect(
            "owner_delivery_area"
        )


    return redirect(
        "owner_delivery_area"
    )

##edit delivary area
@owner_required
def edit_delivery_area(request, id):

    area = get_object_or_404(
        delivery_area,
        id=id
    )

    if request.method == "POST":

        locality = request.POST.get(
            "locality",
            ""
        ).strip()

        pincode = request.POST.get(
            "pincode",
            ""
        ).strip()

        delivery_charge = request.POST.get(
            "delivery_charge",
            "0"
        ).strip()

        is_available = (
            request.POST.get("is_available")
            == "on"
        )


        if not locality or not pincode:

            messages.error(
                request,
                "Locality and pincode are required."
            )

            return redirect(
                "owner_delivery_area"
            )


        if not pincode.isdigit():

            messages.error(
                request,
                "Pincode must contain only numbers."
            )

            return redirect(
                "owner_delivery_area"
            )


        if delivery_area.objects.filter(
            pincode=pincode
        ).exclude(
            id=id
        ).exists():

            messages.error(
                request,
                "Another delivery area already uses this pincode."
            )

            return redirect(
                "owner_delivery_area"
            )


        try:
            delivery_charge = Decimal(
                delivery_charge
            )

            if delivery_charge < 0:
                raise ValueError

        except (
                InvalidOperation,
                ValueError,
                TypeError
            ):

                messages.error(
                    request,
                    "Enter a valid delivery charge."
                )

                return redirect(
                    "owner_delivery_area"
                )

        area.locality = locality

        area.pincode = pincode

        area.delivery_charge = delivery_charge

        area.is_available = is_available

        area.save()


        messages.success(
            request,
            "Delivery area updated successfully."
        )


        return redirect(
            "owner_delivery_area"
        )


    context = {

        "area": area

    }


    return render(
        request,
        "edit_delivery_area.html",
        context
    )

##toogle delivary area
@owner_required
def toggle_delivery_area(request, id):

    area = get_object_or_404(
        delivery_area,
        id=id
    )

    area.is_available = not area.is_available

    area.save(
        update_fields=[
            "is_available",
            "updated_at"
        ]
    )

    if area.is_available:

        messages.success(
            request,
            f"{area.locality} is now available for delivery."
        )

    else:

        messages.success(
            request,
            f"{area.locality} is no longer available for delivery."
        )

    return redirect(
        "owner_delivery_area"
    )