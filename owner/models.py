from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class owner(models.Model):
    Name = models.CharField(max_length=200,null= False)
    Username = models.CharField(max_length=100 ,null=False , unique=True)
    Password = models.CharField(max_length=100 ,null=False) 

class category(models.Model):
    category_name =models.CharField(max_length=100, unique=True)
    category_image = models.CharField(max_length=200,blank=True ,null=True)
    def __str__(self):
        return self.category_name

class section(models.Model):
    section_name = models.CharField(max_length=200, unique=True , null=False)
    rack_number = models.CharField( max_length=20,unique=True , null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.section_name} ({self.rack_number})"


class product(models.Model):

    product_name = models.CharField(max_length=200,unique=True,null = False)
    category = models.ForeignKey(category,on_delete=models.CASCADE)
    section = models.ForeignKey(section,on_delete=models.CASCADE)
    product_image = models.CharField(max_length=200,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    actual_price = models.DecimalField( max_digits=10,decimal_places=2)
    offer_price = models.DecimalField( max_digits=10,decimal_places=2, blank=True, null=True)
    quantity = models.PositiveIntegerField(null=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product_name
    
class staff(models.Model):

    staff_name = models.CharField(max_length=200 , null=False)
    username = models.CharField(max_length=100,unique=True , null=False)
    password = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10,decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField( auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return self.staff_name

# ==========================================
# CUSTOMER
# ==========================================

class customer(models.Model):

    name = models.CharField(max_length=200, null=False)
    username = models.CharField(max_length=100, unique=True, null=False)
    email = models.EmailField(unique=True, null=False)
    gender = models.CharField(max_length=20,blank=True,null=True)
    password = models.CharField(max_length=255, null=False)
    image = models.CharField(max_length=255,blank=True,null=True)

    phone = models.CharField(
        max_length=15,
        unique=True,
        null=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.name


# ==========================================
# DELIVERY AREA
# ==========================================

class delivery_area(models.Model):

    locality = models.CharField(
        max_length=200
    )

    pincode = models.CharField(
        max_length=10,
        unique=True
    )

    is_available = models.BooleanField(
        default=True
    )

    delivery_charge = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return f"{self.locality} - {self.pincode}"


# ==========================================
# ORDER
# ==========================================

class order(models.Model):

    STATUS_CHOICES = [

        ("pending", "Pending"),

        ("confirmed", "Confirmed"),

        ("preparing", "Preparing"),

        ("out_for_delivery", "Out for Delivery"),

        ("delivered", "Delivered"),

        ("cancelled", "Cancelled"),

    ]

    PAYMENT_METHOD_CHOICES = [

        ("cod", "Cash on Delivery"),

        ("online", "Online Payment"),

    ]

    PAYMENT_STATUS_CHOICES = [

        ("pending", "Pending"),

        ("paid", "Paid"),

        ("failed", "Failed"),

        ("refunded", "Refunded"),

    ]

    DELIVERY_TYPE_CHOICES = [

    ("asap", "As Soon As Possible"),

    ("scheduled", "Scheduled"),

    ]

    customer = models.ForeignKey(
        customer,
        on_delete=models.PROTECT,
        related_name="orders"
    )

    delivery_area = models.ForeignKey(
    delivery_area,
    on_delete=models.PROTECT,
    related_name="orders",
    null=True,
    blank=True
    )

    order_number = models.CharField(
        max_length=30,
        unique=True
    )

    address = models.TextField()

    delivery_type = models.CharField(
    max_length=20,
    choices=DELIVERY_TYPE_CHOICES,
    default="asap"
    )

    scheduled_date = models.DateField(
    null=True,
    blank=True
    )

    scheduled_slot = models.CharField(
    max_length=50,
    null=True,
    blank=True
    )

    delivery_charge = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    default=0
    )

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="pending"
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default="cod"
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return self.order_number


# ==========================================
# ORDER ITEM
# ==========================================

class order_item(models.Model):

    order = models.ForeignKey(
        order,
        on_delete=models.CASCADE,
        related_name="items"
    )

    product = models.ForeignKey(
        product,
        on_delete=models.PROTECT,
        related_name="order_items"
    )

    quantity = models.PositiveIntegerField()

    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    def __str__(self):

        return (
            f"{self.order.order_number} - "
            f"{self.product.product_name}"
        )


# ==========================================
# FEEDBACK
# ==========================================

class feedback(models.Model):

    customer = models.ForeignKey(
        customer,
        on_delete=models.CASCADE,
        related_name="feedbacks"
    )

    product = models.ForeignKey(
        product,
        on_delete=models.PROTECT,
        related_name="feedbacks"
    )

    feedback = models.TextField()

    rating = models.PositiveSmallIntegerField(
    validators=[
        MinValueValidator(1),
        MaxValueValidator(5)
    ]
    )

    is_visible = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):

        return (
            f"{self.customer.name} - "
            f"{self.product.product_name}"
        )




# ==========================================
# WISHLIST
# ==========================================

class wishlist(models.Model):

    customer = models.ForeignKey(
        customer,
        on_delete=models.CASCADE,
        related_name="wishlist_items"
    )

    product = models.ForeignKey(
        product,
        on_delete=models.PROTECT,
        related_name="wishlist_items"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "customer",
                    "product"
                ],
                name="unique_customer_product_wishlist"
            )

        ]

    def __str__(self):

        return (
            f"{self.customer.name} - "
            f"{self.product.product_name}"
        )