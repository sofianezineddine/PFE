from django.urls import path
from useradmin import views

app_name = "useradmin"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("products/", views.products, name="dashboard-products"),
    path("add-products/", views.add_product, name="dashboard-add-products"),
    path("edit-products/<pid>/", views.edit_product, name="dashboard-edit-products"),
    path("delete-products/<pid>/", views.delete_product, name="dashboard-delete-products"),
    path("orders/", views.orders, name="orders"),
    path("order_detail/<id>/", views.order_detail, name="order_detail"),
    path("change_order_status/<oid>/", views.change_order_status, name="change_order_status"),
    path("profile/", views.profile, name="profile"),
    path("reviews/", views.reviews, name="reviews"),
    path("settings_update_profile/", views.settings_update_profile, name="settings_update"),
    path("change_password/", views.change_password, name="change_password"),
    path("my_address/", views.my_address, name="my_address"),
    path("order_tracking/", views.order_tracking, name="order_tracking"),
]
