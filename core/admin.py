from django.contrib import admin
from core.models import Product , Category ,CartOrder,CartOrderProducts,Wishlist,ProductImages,ProductReview,Address,Coupon,Subscriber





class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['title','product_image','price','category','color','origin','deals','product_status']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','category_image']

class CartOrderAdmin(admin.ModelAdmin):
    list_editable = ['order_status']
    list_display = ['user','total_price','paid_status','order_date','order_status']


class CartOrderProductsAdmin(admin.ModelAdmin):
    list_display = ['order','invoice_no','item','image','qty','price','total']




class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ['user','product','review','rating','review_date']

class CouponAdmin(admin.ModelAdmin):
    list_display = ['code','discount','active']

class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user','product','date']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user','address','country','state','cp','status']

class SubscriberAdmin(admin.ModelAdmin):
    list_display= ["id","email"]

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderProducts, CartOrderProductsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Coupon,CouponAdmin)
admin.site.register(Subscriber,SubscriberAdmin)