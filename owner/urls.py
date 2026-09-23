from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    path("owner_register",views.owner_register,name="owner_registration"),
    path("owner_login",views.owner_login,name="owner_login"),
    path("owner_dashboard",views.owner_dashboard,name="owner_dashboard"),
    path("owner_logout",views.owner_logout,name="owner_logout"),
    path("owner_category", views.owner_category, name="owner_category"),
    path("edit_category/<int:id>/", views.edit_category, name="edit_category"),
    path("delete_category/<int:id>/", views.delete_category, name="delete_category"),

    path("section/", views.owner_section, name="owner_section"),
    path("add_section/", views.add_section, name="add_section"),
    path("edit_section/<int:id>/", views.edit_section, name="edit_section"),
    path("delete_section/<int:id>/", views.delete_section, name="delete_section"),

    path("owner_product",views.owner_product,name="owner_product"),
    path("edit_product/<int:id>/", views.edit_product, name="edit_product"),
    path("delete_product/<int:id>/", views.delete_product, name="delete_product"),
    path("toggle_product_status/<int:id>/",views.toggle_product_status,name="toggle_product_status"),

    path("owner_staff",views.owner_staff,name="owner_staff"),
    path("edit_staff/<int:id>/",views.edit_staff,name="edit_staff"),
    path("delete_staff/<int:id>/",views.delete_staff,name="delete_staff"),
    path("toggle_staff_status/<int:id>/",views.toggle_staff_status,name="toggle_staff_status"),

    path("owner_customer",views.owner_customer,name="owner_customer"),
    path("toggle_customer_status/<int:id>/",views.toggle_customer_status,name="toggle_customer_status"),
    path("customer_details/<int:id>/",views.customer_details,name="customer_details"),

    path("owner_order",views.owner_order,name="owner_order"),
    path("order_details/<int:id>/", views.order_details, name="order_details"),
    path("update_order_status/<int:id>/", views.update_order_status, name="update_order_status"),

    path("owner_feedback",views.owner_feedback,name="owner_feedback"),
    path("toggle_feedback_visibility/<int:id>/", views.toggle_feedback_visibility, name="toggle_feedback_visibility"),

    path("owner_delivery_area", views.owner_delivery_area, name="owner_delivery_area"),
    path("add_delivery_area/", views.add_delivery_area, name="add_delivery_area"),
    path("edit_delivery_area/<int:id>/", views.edit_delivery_area, name="edit_delivery_area"),
    path("toggle_delivery_area/<int:id>/", views.toggle_delivery_area, name="toggle_delivery_area"),

]

