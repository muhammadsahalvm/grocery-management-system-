from django.urls import path
from . import views

urlpatterns = [

    path("login/",views.staff_login,name="staff_login"),

    path("dashboard/",views.staff_dashboard,name="staff_dashboard"),

    path("logout/",views.staff_logout,name="staff_logout"),

    path("products/",views.staff_product,name="staff_product"),
    
    path("update-stock/<int:id>/",views.update_stock,name="update_stock"),

    path("categories/",views.staff_category,name="staff_category"),

    path("sections/",views.staff_section,name="staff_section"),

]