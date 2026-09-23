from django.db import models

from owner.models import customer, product


class cart(models.Model):

    customer = models.ForeignKey(
        customer,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )   

    product = models.ForeignKey(
        product,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:

        constraints = [

            models.UniqueConstraint(
                fields=[
                    "customer",
                    "product"
                ],
                name="unique_customer_product_cart"
            )

        ]

    def __str__(self):

        return (
            f"{self.customer.username} - "
            f"{self.product.product_name}"
        )   