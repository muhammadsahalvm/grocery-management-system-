from django.http import request , JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import cart
from owner.models import customer, order_item ,product, category, section, staff, order, feedback, delivery_area, wishlist

import os
from django.core.files.storage import FileSystemStorage

from django.db.models import Avg


def user_required(view_func):

    def wrapper(request, *args, **kwargs):

        customer_id = request.session.get(
            "customer_id"
        )

        if not customer_id:

            messages.error(
                request,
                "Please login to continue."
            )

            return redirect(
                "user_login"
            )

        try:

            user = customer.objects.get(
                id=customer_id,
                is_active=True
            )

        except customer.DoesNotExist:

            request.session.flush()

            messages.error(
                request,
                "Please login again."
            )

            return redirect(
                "user_login"
            )

        request.current_customer = user

        if "customer_image" not in request.session or request.session.get("customer_image") != str(user.image or ""):
            request.session["customer_image"] = str(user.image) if user.image else ""

        return view_func(
            request,
            *args,
            **kwargs
        )

    return wrapper

# ==========================================
# CUSTOMER REGISTRATION
# ==========================================

def user_register(request):

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        username = request.POST.get(
            "username",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        gender = request.POST.get(
            "gender",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )

        phone = request.POST.get(
            "phone",
            ""
        ).strip()


        # ==========================================
        # REQUIRED FIELD VALIDATION
        # ==========================================

        if not all([
            name,
            username,
            email,
            password,
            phone
        ]):

            messages.error(
                request,
                "Please fill all required fields."
            )

            return redirect(
                "user_register"
            )


        # ==========================================
        # USERNAME CHECK
        # ==========================================

        if customer.objects.filter(
            username__iexact=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect(
                "user_register"
            )


        # ==========================================
        # EMAIL CHECK
        # ==========================================

        if customer.objects.filter(
            email__iexact=email
        ).exists():

            messages.error(
                request,
                "Email already exists."
            )

            return redirect(
                "user_register"
            )


        # ==========================================
        # PHONE CHECK
        # ==========================================

        if customer.objects.filter(
            phone=phone
        ).exists():

            messages.error(
                request,
                "Phone number already exists."
            )

            return redirect(
                "user_register"
            )


        # ==========================================
        # CREATE CUSTOMER
        # ==========================================

        customer.objects.create(

            name=name,

            username=username,

            email=email,

            gender=gender or None,

            password=password,

            phone=phone,

            is_active=True

        )


        messages.success(
            request,
            "Registration successful. Please login."
        )


        return redirect(
            "user_login"
        )


    return render(
        request,
        "user/user_register.html"
    )


# ==========================================
# CUSTOMER LOGIN
# ==========================================

def user_login(request):

    if request.method == "POST":

        username = request.POST.get(
            "username",
            ""
        ).strip()

        password = request.POST.get(
            "password",
            ""
        )


        # ==========================================
        # REQUIRED FIELD VALIDATION
        # ==========================================

        if not username or not password:

            messages.error(
                request,
                "Username and password are required."
            )

            return redirect(
                "user_login"
            )


        # ==========================================
        # FIND CUSTOMER
        # ==========================================

        try:

            user = customer.objects.get(
                username__iexact=username
            )

        except customer.DoesNotExist:

            messages.error(
                request,
                "Invalid username or password."
            )

            return redirect(
                "user_login"
            )


        # ==========================================
        # ACCOUNT STATUS
        # ==========================================

        if not user.is_active:

            messages.error(
                request,
                "Your account is currently inactive."
            )

            return redirect(
                "user_login"
            )


        # ==========================================
        # PASSWORD CHECK
        # ==========================================

        if user.password != password:

            messages.error(
                request,
                "Invalid username or password."
            )

            return redirect(
                "user_login"
            )


        # ==========================================
        # CREATE SESSION
        # ==========================================

        request.session["customer_id"] = user.id

        request.session["customer_username"] = (
            user.username
        )

        request.session["customer_name"] = (
            user.name
        )

        request.session["customer_image"] = (
            str(user.image) if user.image else ""
        )


        request.session.save()


        messages.success(
            request,
            f"Welcome, {user.name}!"
        )


        return redirect(
            "user_home"
        )


    return render(
        request,
        "user/user_login.html"
    )

# ==========================================
# CUSTOMER LOGOUT
# ==========================================

def user_logout(request):

    request.session.flush()

    messages.success(
        request,
        "You have been logged out successfully."
    )

    return redirect(
        "user_login"
    )

# ==========================================
# CUSTOMER PROFILE
# ==========================================

@user_required
def user_profile(request):

    user = request.current_customer


    # ==========================================
    # UPDATE PROFILE
    # ==========================================

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        gender = request.POST.get(
            "gender",
            ""
        ).strip()

        profile_image = request.FILES.get(
            "profile_image"
        )


        # ==========================================
        # REQUIRED FIELDS
        # ==========================================

        if not name or not email or not phone:

            messages.error(
                request,
                "Name, email and phone are required."
            )

            return redirect(
                "user_profile"
            )


        # ==========================================
        # EMAIL DUPLICATE CHECK
        # ==========================================

        if customer.objects.filter(
            email__iexact=email
        ).exclude(
            id=user.id
        ).exists():

            messages.error(
                request,
                "This email is already in use."
            )

            return redirect(
                "user_profile"
            )


        # ==========================================
        # PHONE DUPLICATE CHECK
        # ==========================================

        if customer.objects.filter(
            phone=phone
        ).exclude(
            id=user.id
        ).exists():

            messages.error(
                request,
                "This phone number is already in use."
            )

            return redirect(
                "user_profile"
            )


        # ==========================================
        # UPDATE BASIC INFORMATION
        # ==========================================

        user.name = name

        user.email = email

        user.phone = phone

        user.gender = gender or None


        # ==========================================
        # PROFILE IMAGE
        # ==========================================

        if profile_image:

            fs = FileSystemStorage(
                location="media/customer_images"
            )

            filename = fs.save(
                profile_image.name,
                profile_image
            )

            image_path = os.path.join(
                "customer_images",
                filename
            )

            user.image = image_path


        # ==========================================
        # SAVE USER
        # ==========================================

        user.save()


        # ==========================================
        # UPDATE SESSION
        # ==========================================

        request.session["customer_name"] = user.name
        request.session["customer_image"] = str(user.image) if user.image else ""


        messages.success(
            request,
            "Profile updated successfully."
        )


        return redirect(
            "user_profile"
        )


    # ==========================================
    # DISPLAY PROFILE
    # ==========================================

    context = {

        "customer": user

    }


    return render(
        request,
        "user/user_profile.html",
        context
    )

# ==========================================
# MAIN USER STOREFRONT
# ==========================================

def user_home(request):

    if request.session.get("customer_id") and "customer_image" not in request.session:
        try:
            home_user = customer.objects.get(id=request.session["customer_id"])
            request.session["customer_image"] = str(home_user.image) if home_user.image else ""
        except customer.DoesNotExist:
            pass

    products = (
        product.objects
        .filter(
            is_active=True
        )
        .select_related(
            "category",
            "section"
        )
        .order_by(
            "product_name"
        )
    )


    search = request.GET.get(
        "search",
        ""
    ).strip()

    category_id = request.GET.get(
        "category",
        ""
    ).strip()

    section_id = request.GET.get(
        "section",
        ""
    ).strip()


    # ==========================================
    # SEARCH
    # ==========================================

    if search:

        products = products.filter(

            Q(
                product_name__icontains=search
            )

            |

            Q(
                description__icontains=search
            )

            |

            Q(
                category__category_name__icontains=search
            )

            |

            Q(
                section__section_name__icontains=search
            )

        )


    # ==========================================
    # CATEGORY FILTER
    # ==========================================

    if category_id:

        products = products.filter(
            category_id=category_id
        )


    # ==========================================
    # SECTION FILTER
    # ==========================================

    if section_id:

        products = products.filter(
            section_id=section_id
        )


    # ==========================================
    # ACTIVE CATEGORIES
    # ==========================================

    categories = (
        category.objects
        .order_by(
            "category_name"
        )
    )


    # ==========================================
    # ACTIVE SECTIONS
    # ==========================================

    sections = (
        section.objects
        .filter(
            is_active=True
        )
        .order_by(
            "section_name"
        )
    )


    # ==========================================
    # LOGGED-IN CUSTOMER
    # ==========================================

    customer_data = None

    customer_id = request.session.get(
        "customer_id"
    )

    if customer_id:

        try:

            customer_data = customer.objects.get(
                id=customer_id,
                is_active=True
            )

        except customer.DoesNotExist:

            request.session.flush()


    context = {

        "products": products,

        "categories": categories,

        "sections": sections,

        "search": search,

        "selected_category": category_id,

        "selected_section": section_id,

        "customer": customer_data,

    }


    return render(
        request,
        "user/user_home.html",
        context
    )
# ==========================================
# PRODUCT DETAIL
# ==========================================

@user_required
def user_product_detail(request, id):

    product_item = get_object_or_404(
        product.objects.select_related(
            "category",
            "section"
        ),
        id=id,
        is_active=True
    )


    current_customer = request.current_customer


    # ==========================================
    # CUSTOMER FEEDBACK
    # ==========================================

    feedbacks = (
        feedback.objects
        .filter(
            product=product_item,
            is_visible=True
        )
        .select_related(
            "customer"
        )
        .order_by(
            "-created_at"
        )
    )


    # ==========================================
    # AVERAGE RATING
    # ==========================================

    rating_data = feedback.objects.filter(
        product=product_item,
        is_visible=True
    ).aggregate(
        average_rating=Avg("rating")
    )


    average_rating = rating_data["average_rating"]


    # ==========================================
    # REVIEW ELIGIBILITY
    # ==========================================

    can_review = (
        order_item.objects
        .filter(
            order__customer=current_customer,
            order__status="delivered",
            product=product_item
        )
        .exists()
    )


    has_reviewed = (
        feedback.objects
        .filter(
            customer=current_customer,
            product=product_item
        )
        .exists()
    )


    # ==========================================
    # RELATED & BEST SELLING & CART STATE
    # ==========================================

    related_products = product.objects.filter(
        category=product_item.category,
        is_active=True
    ).exclude(id=product_item.id).order_by("-id")[:4]

    best_selling_products = product.objects.filter(
        is_active=True
    ).order_by("-id")[:4]
    
    cart_item = cart.objects.filter(
        customer=current_customer,
        product=product_item
    ).first()
    
    cart_quantity = cart_item.quantity if cart_item else 0


    context = {

        "product": product_item,

        "feedbacks": feedbacks,

        "average_rating": average_rating,

        "can_review": can_review,

        "has_reviewed": has_reviewed,
        
        "related_products": related_products,
        
        "best_selling_products": best_selling_products,
        
        "cart_quantity": cart_quantity,

    }


    return render(
        request,
        "user/user_product_detail.html",
        context
    )
# ==========================================
# ADD TO WISHLIST
# ==========================================

@user_required
def add_to_wishlist(request, id):

    product_item = get_object_or_404(
        product,
        id=id,
        is_active=True
    )

    wishlist_item, created = wishlist.objects.get_or_create(

        customer=request.current_customer,

        product=product_item

    )

    if created:

        messages.success(
            request,
            f"{product_item.product_name} added to your wishlist."
        )

    else:

        messages.info(
            request,
            f"{product_item.product_name} is already in your wishlist."
        )


    return redirect(
        "user_product_detail",
        id=id
    )

# ==========================================
# REMOVE FROM WISHLIST
# ==========================================

@user_required
def remove_from_wishlist(request, id):

    product_item = get_object_or_404(
        product,
        id=id
    )

    wishlist.objects.filter(

        customer=request.current_customer,

        product=product_item

    ).delete()


    messages.success(
        request,
        f"{product_item.product_name} removed from your wishlist."
    )


    return redirect(
        "user_wishlist"
    )

# ==========================================
# WISHLIST
# ==========================================

@user_required
def user_wishlist(request):

    wishlist_items = (
        wishlist.objects
        .filter(
            customer=request.current_customer
        )
        .select_related(
            "product",
            "product__category",
            "product__section"
        )
        .order_by(
            "-created_at"
        )
    )


    context = {

        "wishlist_items": wishlist_items,

    }


    return render(
        request,
        "user/user_wishlist.html",
        context
    )

# ==========================================
# DELIVERY AVAILABILITY
# ==========================================

@user_required
def check_delivery_availability(request):

    delivery = None
    checked = False

    if request.method == "POST":

        pincode = request.POST.get(
            "pincode",
            ""
        ).strip()

        checked = True

        if not pincode:

            messages.error(
                request,
                "Please enter your pincode."
            )

        else:

            try:

                delivery = delivery_area.objects.get(
                    pincode=pincode
                )

            except delivery_area.DoesNotExist:

                delivery = None


    context = {

        "delivery": delivery,

        "checked": checked,

    }


    return render(
        request,
        "user/delivery_check.html",
        context
    )

# ==========================================
# ADD TO CART
# ==========================================

@user_required
def add_to_cart(request, id):

    product_item = get_object_or_404(
        product,
        id=id,
        is_active=True
    )


    # ==========================================
    # GET REQUESTED QUANTITY
    # ==========================================

    quantity = request.POST.get(
        "quantity",
        "1"
    ).strip()


    try:

        quantity = int(quantity)

    except (ValueError, TypeError):

        messages.error(
            request,
            "Invalid quantity."
        )

        return redirect(
            "user_product_detail",
            id=id
        )


    # ==========================================
    # QUANTITY VALIDATION
    # ==========================================

    if quantity == 0:

        messages.error(
            request,
            "Quantity cannot be zero."
        )

        return redirect(
            "user_product_detail",
            id=id
        )


    # ==========================================
    # STOCK VALIDATION
    # ==========================================

    if product_item.quantity <= 0:

        messages.error(
            request,
            "This product is currently out of stock."
        )

        return redirect(
            "user_product_detail",
            id=id
        )


    # ==========================================
    # FIND EXISTING CART ITEM
    # ==========================================

    cart_item = cart.objects.filter(

        customer=request.current_customer,

        product=product_item

    ).first()


    if cart_item:

        new_quantity = (
            cart_item.quantity + quantity
        )

        if new_quantity <= 0:
            cart_item.delete()
            
            messages.success(
                request,
                f"{product_item.product_name} removed from your cart."
            )
            
            next_url = request.META.get('HTTP_REFERER')
            if next_url:
                return redirect(next_url)
                
            return redirect(
                "user_product_detail",
                id=id
            )

        if new_quantity > product_item.quantity:

            messages.error(
                request,
                f"Only {product_item.quantity} "
                f"units are available."
            )

            return redirect(
                "user_product_detail",
                id=id
            )


        cart_item.quantity = new_quantity

        cart_item.save()


    else:

        if quantity <= 0:
            messages.error(
                request,
                "Quantity must be at least 1."
            )

            return redirect(
                "user_product_detail",
                id=id
            )

        if quantity > product_item.quantity:

            messages.error(
                request,
                f"Only {product_item.quantity} "
                f"units are available."
            )

            return redirect(
                "user_product_detail",
                id=id
            )


        cart.objects.create(

            customer=request.current_customer,

            product=product_item,

            quantity=quantity

        )


    messages.success(
        request,
        f"{product_item.product_name} added successfully."
    )

    next_url = request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
        
    return redirect(
        "user_product_detail",
        id=id
    )

# ==========================================
# VIEW CART
# ==========================================

@user_required
def user_cart(request):

    cart_items = (
        cart.objects
        .filter(
            customer=request.current_customer
        )
        .select_related(
            "product",
            "product__category",
            "product__section"
        )
        .order_by(
            "-created_at"
        )
    )


    subtotal = 0


    for item in cart_items:

        if item.product.offer_price is not None:

            price = item.product.offer_price

        else:

            price = item.product.actual_price


        item.item_price = price

        item.item_total = (
            price * item.quantity
        )

        subtotal += item.item_total


    context = {

        "cart_items": cart_items,

        "subtotal": subtotal,

    }


    return render(
        request,
        "user/user_cart.html",
        context
    )

# ==========================================
# UPDATE CART
# ==========================================

@user_required
def update_cart(request, id):

    if request.method != "POST":

        return redirect(
            "user_cart"
        )


    cart_item = get_object_or_404(

        cart.objects.select_related(
            "product"
        ),

        id=id,

        customer=request.current_customer

    )


    quantity = request.POST.get(
        "quantity",
        ""
    ).strip()


    try:

        quantity = int(quantity)

    except (ValueError, TypeError):

        messages.error(
            request,
            "Invalid quantity."
        )

        return redirect(
            "user_cart"
        )


    if quantity <= 0:

        messages.error(
            request,
            "Quantity must be at least 1."
        )

        return redirect(
            "user_cart"
        )


    if not cart_item.product.is_active:

        messages.error(
            request,
            f"{cart_item.product.product_name} "
            f"is no longer available."
        )

        return redirect(
            "user_cart"
        )


    if quantity > cart_item.product.quantity:

        messages.error(
            request,
            f"Only {cart_item.product.quantity} "
            f"units are available."
        )

        return redirect(
            "user_cart"
        )


    cart_item.quantity = quantity

    cart_item.save()


    messages.success(
        request,
        "Cart updated successfully."
    )


    return redirect(
        "user_cart"
    )

# ==========================================
# REMOVE FROM CART
# ==========================================

@user_required
def remove_from_cart(request, id):

    if request.method != "POST":

        return redirect(
            "user_cart"
        )


    cart_item = get_object_or_404(

        cart,

        id=id,

        customer=request.current_customer

    )


    product_name = (
        cart_item.product.product_name
    )


    cart_item.delete()


    messages.success(
        request,
        f"{product_name} removed from your cart."
    )


    return redirect(
        "user_cart"
    )

# ==========================================
# CHECKOUT
# ==========================================

@user_required
def checkout(request):

    cart_items = (
        cart.objects
        .filter(
            customer=request.current_customer
        )
        .select_related(
            "product"
        )
    )

    if not cart_items.exists():

        messages.error(
            request,
            "Your cart is empty."
        )

        return redirect(
            "user_cart"
        )


    subtotal = 0


    for item in cart_items:

        # ------------------------------------------
        # PRODUCT AVAILABILITY CHECK
        # ------------------------------------------

        if not item.product.is_active:

            messages.error(
                request,
                f"{item.product.product_name} "
                f"is no longer available."
            )

            return redirect(
                "user_cart"
            )


        # ------------------------------------------
        # STOCK CHECK
        # ------------------------------------------

        if item.product.quantity < item.quantity:

            messages.error(
                request,
                f"Only {item.product.quantity} "
                f"units of {item.product.product_name} "
                f"are currently available."
            )

            return redirect(
                "user_cart"
            )


        # ------------------------------------------
        # CURRENT PRICE
        # ------------------------------------------

        if item.product.offer_price is not None:

            price = item.product.offer_price

        else:

            price = item.product.actual_price


        item.item_price = price

        item.item_total = (
            price * item.quantity
        )

        subtotal += item.item_total




    delivery_charge = 0
    selected_delivery_area = None



    # ==========================================
    # POST
    # ==========================================

    if request.method == "POST":

        street = request.POST.get(
            "street",
            ""
        ).strip()

        city = request.POST.get(
            "city",
            ""
        ).strip()

        pincode = request.POST.get(
            "pincode",
            ""
        ).strip()

        delivery_type = request.POST.get(
            "delivery_type",
            "asap"
        ).strip()

        scheduled_date = request.POST.get(
            "scheduled_date",
            ""
        ).strip()

        scheduled_slot = request.POST.get(
            "scheduled_slot",
            ""
        ).strip()

        payment_method = request.POST.get(
            "payment_method",
            "cod"
        ).strip()


        # ==========================================
        # ADDRESS VALIDATION
        # ==========================================

        if not street:

            messages.error(
                request,
                "Please enter your street name."
            )

            return redirect("checkout")


        if not city:

            messages.error(
                request,
                "Please enter your city."
            )

            return redirect("checkout")


        if not pincode:

            messages.error(
                request,
                "Please enter your pincode."
            )

            return redirect("checkout")


        if not pincode.isdigit():

            messages.error(
                request,
                "Pincode must contain only numbers."
            )

            return redirect("checkout")

        # ==========================================
        # DELIVERY AREA BY PINCODE
        # ==========================================

        try:

            selected_delivery_area = (
                delivery_area.objects.get(
                    pincode=pincode
                )
            )

        except delivery_area.DoesNotExist:

            messages.error(
                request,
                "Delivery is currently unavailable "
                "for this pincode."
            )

            return redirect(
                "checkout"
            )


        if not selected_delivery_area.is_available:

            messages.error(
                request,
                "Delivery is currently unavailable "
                f"for {selected_delivery_area.locality}."
            )

            return redirect(
                "checkout"
            )


        delivery_charge = (
            selected_delivery_area.delivery_charge
        )


        # ==========================================
        # DELIVERY TYPE
        # ==========================================

        if delivery_type not in [
            "asap",
            "scheduled"
        ]:

            messages.error(
                request,
                "Invalid delivery type."
            )

            return redirect(
                "checkout"
            )


        # ==========================================
        # SCHEDULED ORDER VALIDATION
        # ==========================================

        if delivery_type == "scheduled":

            if not scheduled_date:

                messages.error(
                    request,
                    "Please select a delivery date."
                )

                return redirect(
                    "checkout"
                )


            if not scheduled_slot:

                messages.error(
                    request,
                    "Please select a delivery time slot."
                )

                return redirect(
                    "checkout"
                )

        else:

            scheduled_date = None

            scheduled_slot = None


        # ==========================================
        # PAYMENT METHOD
        # ==========================================

        if payment_method not in [
            "cod",
            "online"
        ]:

            messages.error(
                request,
                "Invalid payment method."
            )

            return redirect(
                "checkout"
            )


        # ==========================================
        # FINAL TOTAL
        # ==========================================

        total_amount = (
            subtotal + delivery_charge
        )


        # ==========================================
        # TEMPORARY PAYMENT LOGIC
        # ==========================================

        if payment_method == "cod":

            payment_status = "pending"

        else:

            # Online payment is not implemented yet.
            # Do NOT mark it as paid.

            payment_status = "pending"


        # ==========================================
        # CREATE ORDER NUMBER
        # ==========================================

        import uuid

        order_number = (
            "ORD-"
            + uuid.uuid4().hex[:10].upper()
        )


        # ==========================================
        # CREATE ORDER
        # ==========================================

        new_order = order.objects.create(

            customer=request.current_customer,

            delivery_area=selected_delivery_area,

            order_number=order_number,

            address=(
                    f"{street}, "
                    f"{city}, "
                    f"{pincode}"
             ),

            delivery_type=delivery_type,

            scheduled_date=scheduled_date,

            scheduled_slot=scheduled_slot,

            delivery_charge=delivery_charge,

            total_amount=total_amount,

            status="pending",

            payment_method=payment_method,

            payment_status=payment_status

        )


        # ==========================================
        # CREATE ORDER ITEMS + REDUCE STOCK
        # ==========================================

        for item in cart_items:

            if item.product.offer_price is not None:

                unit_price = (
                    item.product.offer_price
                )

            else:

                unit_price = (
                    item.product.actual_price
                )


            item_total = (
                unit_price * item.quantity
            )


            order_item.objects.create(

                order=new_order,

                product=item.product,

                quantity=item.quantity,

                unit_price=unit_price,

                total_price=item_total

            )


            # Reduce stock

            item.product.quantity -= (
                item.quantity
            )

            item.product.save(
                update_fields=[
                    "quantity"
                ]
            )


        # ==========================================
        # CLEAR CART
        # ==========================================

        cart_items.delete()


        messages.success(
            request,
            "Order placed successfully."
        )


        return redirect(
            "user_order_detail",
            order_id=new_order.id
        )


    context = {

        "cart_items": cart_items,

        "subtotal": subtotal,

        "delivery_charge": 0,

        "total_amount":  subtotal ,
        

    }


    return render(
        request,
        "user/user_checkout.html",
        context
    )

# ==========================================
# ORDER DETAIL
# ==========================================

@user_required
def user_order_detail(request, order_id):

    user_order = get_object_or_404(

        order.objects.prefetch_related(
            "items__product"
        ),

        id=order_id,

        customer=request.current_customer

    )

    product_subtotal = sum(
        item.total_price
        for item in user_order.items.all()
    )

    context = {

        "order": user_order,

        "product_subtotal": product_subtotal,

    }

    return render(
        request,
        "user/user_order_detail.html",
        context
    )

# ==========================================
# CHECK DELIVERY AVAILABILITY
# ==========================================

@user_required
def check_delivery(request):

    pincode = request.GET.get(
        "pincode",
        ""
    ).strip()


    if not pincode:

        return JsonResponse({
            "available": False,
            "message": "Pincode is required."
        })


    if not pincode.isdigit():

        return JsonResponse({
            "available": False,
            "message": "Invalid pincode."
        })


    try:

        area = delivery_area.objects.get(
            pincode=pincode
        )

    except delivery_area.DoesNotExist:

        return JsonResponse({
            "available": False,
            "message": (
                "Delivery is currently unavailable "
                "for this pincode."
            )
        })


    if not area.is_available:

        return JsonResponse({
            "available": False,
            "message": (
                "Delivery is currently unavailable "
                "for this location."
            )
        })


    return JsonResponse({

        "available": True,

        "locality": area.locality,

        "pincode": area.pincode,

        "delivery_charge": str(
            area.delivery_charge
        )

    })

# ==========================================
# ORDER HISTORY
# ==========================================

@user_required
def user_orders(request):

    orders = (
        order.objects
        .filter(
            customer=request.current_customer
        )
        .select_related(
            "delivery_area"
        )
        .prefetch_related(
            "items__product"
        )
        .order_by(
            "-created_at"
        )
    )

    context = {

        "orders": orders,

    }

    return render(
        request,
        "user/user_order.html",
        context
    )


# ==========================================
# CANCEL ORDER
# ==========================================

@user_required
def cancel_order(request, order_id):

    if request.method != "POST":

        return redirect(
            "user_order_detail",
            order_id=order_id
        )


    from django.db import transaction


    with transaction.atomic():

        # ==========================================
        # GET AND LOCK ORDER
        # ==========================================

        user_order = get_object_or_404(

            order.objects.select_for_update(),

            id=order_id,

            customer=request.current_customer

        )


        # ==========================================
        # CHECK STATUS
        # ==========================================

        if user_order.status not in [
            "pending",
            "confirmed"
        ]:

            messages.error(
                request,
                "This order can no longer be cancelled."
            )

            return redirect(
                "user_order_detail",
                order_id=order_id
            )


        # ==========================================
        # GET ORDER ITEMS
        # ==========================================

        order_items = (
            order_item.objects
            .select_related("product")
            .select_for_update()
            .filter(
                order=user_order
            )
        )


        # ==========================================
        # RESTORE STOCK
        # ==========================================

        for item in order_items:

            product_item = (
                product.objects
                .select_for_update()
                .get(
                    id=item.product.id
                )
            )


            product_item.quantity += item.quantity


            product_item.save(
                update_fields=[
                    "quantity"
                ]
            )


        # ==========================================
        # UPDATE ORDER STATUS
        # ==========================================

        user_order.status = "cancelled"

        user_order.save(
            update_fields=[
                "status",
                "updated_at"
            ]
        )


    messages.success(
        request,
        "Order cancelled successfully. "
        "Stock has been restored."
    )


    return redirect(
        "user_order_detail",
        order_id=order_id
    )

@user_required
def change_password(request):

    user = request.current_customer


    if request.method == "POST":

        current_password = request.POST.get(
            "current_password",
            ""
        )

        new_password = request.POST.get(
            "new_password",
            ""
        )

        confirm_password = request.POST.get(
            "confirm_password",
            ""
        )


        # ==========================================
        # CURRENT PASSWORD
        # ==========================================

        if not current_password:

            messages.error(
                request,
                "Please enter your current password."
            )

            return redirect(
                "change_password"
            )


        if current_password != user.password:

            messages.error(
                request,
                "Current password is incorrect."
            )

            return redirect(
                "change_password"
            )


        # ==========================================
        # NEW PASSWORD
        # ==========================================

        if not new_password:

            messages.error(
                request,
                "Please enter a new password."
            )

            return redirect(
                "change_password"
            )


        if len(new_password) < 6:

            messages.error(
                request,
                "New password must contain at least 6 characters."
            )

            return redirect(
                "change_password"
            )


        # ==========================================
        # CONFIRM PASSWORD
        # ==========================================

        if new_password != confirm_password:

            messages.error(
                request,
                "New passwords do not match."
            )

            return redirect(
                "change_password"
            )


        # ==========================================
        # PREVENT SAME PASSWORD
        # ==========================================

        if new_password == user.password:

            messages.error(
                request,
                "New password must be different from your current password."
            )

            return redirect(
                "change_password"
            )


        # ==========================================
        # UPDATE PASSWORD
        # ==========================================

        user.password = new_password

        user.save(
            update_fields=[
                "password",
                "updated_at"
            ]
        )


        messages.success(
            request,
            "Password changed successfully."
        )


        return redirect(
            "user_profile"
        )


    return render(
        request,
        "user/user_change_password.html"
    )

# ==========================================
# ADD FEEDBACK
# ==========================================

@user_required
def add_feedback(request, product_id):

    if request.method != "POST":

        return redirect(
            "user_product_detail",
            id=product_id
        )


    current_customer = request.current_customer


    # ==========================================
    # GET PRODUCT
    # ==========================================

    product_item = get_object_or_404(
        product,
        id=product_id,
        is_active=True
    )


    # ==========================================
    # CHECK PURCHASE
    # ==========================================

    purchased = (
        order_item.objects
        .filter(
            order__customer=current_customer,
            order__status="delivered",
            product=product_item
        )
        .exists()
    )


    if not purchased:

        messages.error(
            request,
            "You can review a product only after purchasing it."
        )

        return redirect(
            "user_product_detail",
            id=product_id
        )


    # ==========================================
    # CHECK EXISTING FEEDBACK
    # ==========================================

    if feedback.objects.filter(
        customer=current_customer,
        product=product_item
    ).exists():

        messages.error(
            request,
            "You have already reviewed this product."
        )

        return redirect(
            "user_product_detail",
            id=product_id
        )


    # ==========================================
    # GET FORM DATA
    # ==========================================

    feedback_text = request.POST.get(
        "feedback",
        ""
    ).strip()

    rating = request.POST.get(
        "rating",
        ""
    ).strip()


    # ==========================================
    # FEEDBACK VALIDATION
    # ==========================================

    if not feedback_text:

        messages.error(
            request,
            "Please enter your feedback."
        )

        return redirect(
            "user_product_detail",
            id=product_id
        )


    # ==========================================
    # RATING VALIDATION
    # ==========================================

    try:

        rating = int(rating)

    except (TypeError, ValueError):

        messages.error(
            request,
            "Please select a valid rating."
        )

        return redirect(
            "user_product_detail",
            id=product_id
        )


    if rating < 1 or rating > 5:

        messages.error(
            request,
            "Rating must be between 1 and 5."
        )

        return redirect(
            "user_product_detail",
            id=product_id
        )


    # ==========================================
    # CREATE FEEDBACK
    # ==========================================

    feedback.objects.create(

        customer=current_customer,

        product=product_item,

        feedback=feedback_text,

        rating=rating

    )


    messages.success(
        request,
        "Feedback submitted successfully."
    )


    return redirect(
        "user_product_detail",
        id=product_id
    )

@user_required
def edit_feedback(request, feedback_id):

    current_customer = request.current_customer


    # ==========================================
    # GET CUSTOMER'S OWN FEEDBACK
    # ==========================================

    review = get_object_or_404(
        feedback,
        id=feedback_id,
        customer=current_customer
    )


    # ==========================================
    # POST
    # ==========================================

    if request.method == "POST":

        feedback_text = request.POST.get(
            "feedback",
            ""
        ).strip()

        rating = request.POST.get(
            "rating",
            ""
        ).strip()


        # ==========================================
        # FEEDBACK VALIDATION
        # ==========================================

        if not feedback_text:

            messages.error(
                request,
                "Please enter your feedback."
            )

            return redirect(
                "edit_feedback",
                feedback_id=feedback_id
            )


        # ==========================================
        # RATING VALIDATION
        # ==========================================

        try:

            rating = int(rating)

        except (TypeError, ValueError):

            messages.error(
                request,
                "Please select a valid rating."
            )

            return redirect(
                "edit_feedback",
                feedback_id=feedback_id
            )


        if rating < 1 or rating > 5:

            messages.error(
                request,
                "Rating must be between 1 and 5."
            )

            return redirect(
                "edit_feedback",
                feedback_id=feedback_id
            )


        # ==========================================
        # UPDATE
        # ==========================================

        review.feedback = feedback_text

        review.rating = rating

        review.save(
            update_fields=[
                "feedback",
                "rating",
                "updated_at"
            ]
        )


        messages.success(
            request,
            "Feedback updated successfully."
        )


        return redirect(
            "user_product_detail",
            id=review.product.id
        )


    # ==========================================
    # DISPLAY EDIT PAGE
    # ==========================================

    context = {

        "review": review

    }


    return render(
        request,
        "user/user_edit_feedback.html",
        context
    )

@user_required
def delete_feedback(request, feedback_id):

    # ==========================================
    # ONLY POST IS ALLOWED
    # ==========================================

    if request.method != "POST":

        return redirect(
            "user_home"
        )


    current_customer = request.current_customer


    # ==========================================
    # GET CUSTOMER'S OWN FEEDBACK
    # ==========================================

    review = get_object_or_404(
        feedback,
        id=feedback_id,
        customer=current_customer
    )


    # ==========================================
    # SAVE PRODUCT ID BEFORE DELETE
    # ==========================================

    product_id = review.product.id


    # ==========================================
    # DELETE FEEDBACK
    # ==========================================

    review.delete()


    messages.success(
        request,
        "Feedback deleted successfully."
    )


    return redirect(
        "user_product_detail",
        id=product_id
    )

def user_info(request):
    return render(request, "user/user_info.html")