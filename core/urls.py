from django.urls import path,include
from core.views import *


app_name = "core"


urlpatterns = [
    path("", index,name="index"),

    path("products/", product_list_view,name="product-list"),
    path("products/<pid>/", product_detail_view,name="product-detail"),

    path("category/", category_list_view,name="category-list"),
    path("category/<cid>/", category_product_list_view,name="category-product-list"),
    path("deals/", deals_view,name="deals"),
   

    #Tags
    path("products/tag/<tag_slug>/",tag_list,name="tags"),

    # Add Review
    path("ajax-add-review/<pid>/",ajax_add_review,name="ajax-add-review"),

    #Search

    path("search/",search_view,name="search"),

    # Filter Products
    path("filter-products/",filter_product,name="filter-product"),

    #Add To Cart
    path("add-to-cart/", add_to_cart, name="add-to-cart"),
   
    #Cart
    path("cart/", cart_view, name="cart"),


    #Delete From Cart

    path("delete-from-cart/", delete_item_from_cart ,name="delete-from-cart"),


    #update cart
    path("update-cart/", update_cart, name="update-cart"),


    #Paypal Integration
    path('paypal/', include('paypal.standard.ipn.urls')),

    #Payement completed
    path("payment-completed/", payment_completed_view1, name="payment-completed"),
    path("payment-completed/<oid>/", payment_completed_view2, name="payment-completed"),

    #Cheackout
    path("checkout/<oid>/", checkout, name="checkout"),

    path("save_checkout_info/", save_checkout_info, name="save_checkout_info"),

    path("api/create_checkout_session/<oid>/", create_checkout_session, name="api_checkout_session"),

    #Payement failed
    path('payement-failed/', payment_failed_view,name="payement-failed"),

    #Customer Dashborad
    path('dashboard/', customer_dashboard,name="dashboard"),

    #Order Detail
    path('dashboard/order/<id>/', order_detail,name="order-detail"),

   
    #Make Default Address
    path("make-default-address/", make_address_default, name="make-default-address"),

    #Wishlist page
    path('wishlist/',wishlist_view, name='wishlist'),


    # add to Wishlist
    path("add-to-wishlist/", add_to_wishlist, name="add-to-wishlist"),



    #Remove From Wishlist
    path("remove-from-wishlist/", remove_wishlist, name="remove-from-wishlist"),










    #Contact
    path("contact/", contact, name="contact"),
    path("ajax-contact-form/", ajax_contact_form, name="ajax-contact-form"),

    #Privacy
    path("privacy_policy/", privacy_policy, name="privacy_policy"),
    
    #Terms Of Use
    path("terms_of_service/", terms_of_service, name="terms_of_service"),

    #About Us
    path('about-us/', about_us_view,name="about"),

    #purchase_guide
    path('purchase-guide/', purchase_guide_view,name="purchase-guide"),
    path("subscribe/", subscribe_view, name="subscribe"),
    path("reset_pass/", reset_pass_view, name="reset_pass"),
    path("forgout_pass/", forgout_pass_view, name="forgout_pass"),


]


