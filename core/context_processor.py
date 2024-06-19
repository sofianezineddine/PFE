
from core.models import Product , Category ,CartOrder,CartOrderProducts,Wishlist,ProductImages,ProductReview,Coupon
from django.db.models import Count, Min, Max
from django.contrib import messages

def default(request):
    categories = Category.objects.all()
    min_max_price= Product.objects.aggregate(Min("price"), Max("price"))
    
    if request.user.is_authenticated:
        try:
            wishlist = Wishlist.objects.filter(user=request.user)
        except:
            messages.warning(request, "You need to login before accessing your wishlist.")
            wishlist = 0
    else:
        wishlist = 0





    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None


    return {
        'categories':categories,
        'wishlist': wishlist,
        'address': address,
        'min_max_price': min_max_price
    }