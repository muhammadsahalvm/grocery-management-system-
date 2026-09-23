from django.urls import path, include 

from . import views


urlpatterns = [
    path("", views.user_home, name="user_home"),
    path("info/", views.user_info, name="user_info"),
    path("register/", views.user_register, name="user_register"),
    path("login/", views.user_login, name="user_login"),
    path("logout/", views.user_logout, name="user_logout"),
    path("profile/", views.user_profile, name="user_profile"),
    path("product/<int:id>/", views.user_product_detail, name="user_product_detail"),

    path("wishlist/", views.user_wishlist, name="user_wishlist"),
    path("add_to_wishlist/<int:id>/", views.add_to_wishlist, name="add_to_wishlist"),
    path("remove_from_wishlist/<int:id>/", views.remove_from_wishlist, name="remove_from_wishlist"),
    path("delivery-check/", views.check_delivery_availability, name="check_delivery_availability"),

    path("cart/", views.user_cart, name="user_cart"),
    path("cart/add/<int:id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:id>/", views.remove_from_cart, name="remove_from_cart"),
    path("cart/update/<int:id>/", views.update_cart, name="update_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("check-delivery/", views.check_delivery, name="check_delivery"),

    path("orders/", views.user_orders, name="user_orders"),
    path("order/<int:order_id>/", views.user_order_detail, name="user_order_detail"),
    path("order/<int:order_id>/cancel/", views.cancel_order, name="cancel_order"),

    path("profile/change-password/", views.change_password, name="change_password"),

    path("product/<int:product_id>/feedback/", views.add_feedback, name="add_feedback"),
    path("feedback/<int:feedback_id>/edit/", views.edit_feedback, name="edit_feedback"),
    path("feedback/<int:feedback_id>/delete/", views.delete_feedback, name="delete_feedback"),
]
