from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render,get_object_or_404
from taggit.models import Tag
from core.models import Product , Category ,CartOrder,CartOrderProducts,Wishlist,Subscriber   ,ProductImages,ProductReview,Address,Coupon
from django.db.models import Count,Avg
from core.forms import ProductReviewForm
import datetime
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import login , authenticate,logout
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from paypal.standard.forms import PayPalPaymentsForm
from django.core import serializers
import calendar
from django.db.models.functions import ExtractMonth
from userauth.models import *
import stripe
from django.utils.translation import gettext as _
from django.utils.translation import get_language,activate,gettext


# Shop -----------------------------------------------------------------------------------------
def index(request):
    products = Product.objects.filter(product_status="published")
    categories = Category.objects.all()

    page_name = translate("Home",language=get_language())
    context = {
        "products": products,
        "categories":categories,
        'page_name': page_name,
    }
    return render(request,'core/index.html',context)


def translate(string,language):

    activate(language)
    return gettext(string)


def product_list_view(request):
    products = Product.objects.filter(product_status="published")
    colors = []
    origins = []
    for p in products:
        if p.color not in colors :
            colors.append(p.color)
        if p.origin not in origins :
            origins.append(p.origin)


    context = {
        "products": products,
        'page_name': "Products",
        "origins":origins,
        "colors":colors,
    }
    return render(request,'core/product-list.html',context)



def deals_view(request):
    deals = Product.objects.filter(deals=True,product_status="published")
    context= {
        "deals":deals,
        "page_name":"Super Deals",
    }
    return render(request,"core/deals.html",context)




def category_list_view(request):
    categories = Category.objects.all()
    context = {
        "categories" : categories,
        "page_name": "Categories"
    }

    return render(request,'core/category-list.html',context)


def category_product_list_view(request,cid):

    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status="published",category=category)

    context = {
     "category": category,
     "products"  :products,
     "page_name": f"Categories | {category.title}"
    }
    return render(request,"core/category-product-list.html",context)




def product_detail_view(request,pid):
    product = Product.objects.get(pid=pid)
    try:
        address = Address.objects.filter(user=request.user)
    except :
        address = None
    p_image = product.p_images.all()
    categories = Category.objects.all()


    products = Product.objects.filter(category=product.category).exclude(pid=pid)

    # Getting all reviews
    reviews = ProductReview.objects.filter(product=product).order_by("-date")

    #Average reviews
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    # Product Review Form
    review_form = ProductReviewForm()


    make_review = True

    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()

        if user_review_count > 0:
            make_review = False



    context = {
        "p" : product,
        "page_name": f"Products | {product.title}",
        "p_image": p_image,
        "categories":categories,
        "products":products,
        "reviews":reviews,
        "average_rating":average_rating,
        "review_form":review_form,
        "make_review":make_review,
        "address":address,
    }

    return render(request,"core/product-detail.html",context)

# Tag List ---------------------------------------------------------------------------------

def tag_list(request,tag_slug=None):
    products = Product.objects.filter(product_status="published").order_by("-id")
    tag = None

    if tag_slug :
        tag = get_object_or_404(Tag,slug=tag_slug)
        products = products.filter(tags__in=[tag])


    context = {
        "products" : products,
        "page_name": f"Tags | {tag.name}",
        "tag":tag,
    }

    return render(request,"core/tag.html",context)


# Review ------------------------------------------------------------------------------

def ajax_add_review(request,pid):
    product = Product.objects.get(pid=pid)

    user = request.user
    current_date = datetime.datetime.now().date()

    review = ProductReview.objects.create(
        user = user,
        product=product,
        review= request.POST['review'],
        rating = request.POST['rating'],
        review_date = current_date,
    )


    context = {
        "user" : user.username,
        "review":request.POST['review'],
        "rating": request.POST['rating'],
        "review_date" : current_date,

    }


    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg("rating"))

    return JsonResponse(
       {
        'bool':True,
        'context' : context,
        'average_reviews' : average_reviews
       }
    )

# Search -------------------------------------------------------------------------------------

def search_view(request):
    query = request.GET.get("q")
    cat = request.GET.get("cat")

    productss= Product.objects.all()
    products = Product.objects.filter(title__icontains=query).order_by("-date")
    
    if cat != "all":
        products = products.filter(category = cat)

    colors = []
    origins = []
    for p in productss:
        if p.color not in colors :
            colors.append(p.color)
        if p.origin not in origins :
            origins.append(p.origin)

    context = {
        "products": products,
        "query": query,
        "page_name":"Search",
        "origins":origins,
        "colors":colors,
    }
    return render(request, "core/search.html", context)

# Filter---------------------------------------------------------------------------------------

def filter_product(request):
    categories = request.GET.getlist("category[]")
    colors = request.GET.getlist("color[]")
    origins = request.GET.getlist("origin[]")

    min_price = request.GET['min_price']
    max_price = request.GET['max_price']


    products = Product.objects.filter(product_status="published").order_by("-id").distinct()

    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)

    if len(categories) > 0:
        products= products.filter(category__id__in=categories).distinct()

    if len(colors) > 0:
        products= products.filter(color__in=colors).distinct()

    if len(origins) > 0:
        products= products.filter(origin__in=origins).distinct()

    # context = {
    #     "products" : products,

    # }

    data = render_to_string("core/async/product-list.html",{"products":products})

    return JsonResponse({"data":data})

# Cart -----------------------------------------------------------------------------------------------------------

def add_to_cart(request):
    cart_product = {}

    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],
        'max_weight': request.GET['max_weight']
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:

            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data

    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({"data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})




def cart_view(request):
    cart_total_amount = 0

    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

      
        return render(request, "core/cart.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount , "page_name": "Cart"})
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("core:index")



def delete_item_from_cart(request):

    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data


    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount,'page_name':'Cart'})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})





def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {"cart_data":request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount':cart_total_amount,'page_name':"Cart"})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})



#Payement-----------------------------------------------------------------------------------------------------

@login_required
def save_checkout_info(request):
    cart_total_amount = 0
    total_amount = 0
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        address = request.POST.get("address")
        city = request.POST.get("city")
        country = request.POST.get("country")
        cp = request.POST.get("cp")

      

        request.session['full_name'] = full_name
        request.session['email'] = email
        request.session['mobile'] = mobile
        request.session['address'] = address
        request.session['city'] = city
        request.session['country'] = country
        request.session['cp'] = cp


        if 'cart_data_obj' in request.session:

            # Getting total amount for Paypal Amount
            for p_id, item in request.session['cart_data_obj'].items():
                total_amount += int(item['qty']) * float(item['price'])


            full_name = request.session['full_name']
            email = request.session['email']
            phone = request.session['mobile']
            address = request.session['address']
            city = request.session['city']
            country = request.session['country']
            cp = request.session['cp']

            # Create ORder Object
            order = CartOrder.objects.create(
                user=request.user,
                total_price=total_amount,
                full_name=full_name,
                email=email,
                phone=phone,
                address=address,
                city=city,
                country=country,
                cp=cp
            )

            del request.session['full_name']
            del request.session['email']
            del request.session['mobile']
            del request.session['address']
            del request.session['city']
            del request.session['country']
            del request.session['cp']

            # Getting total amount for The Cart
            for p_id, item in request.session['cart_data_obj'].items():
                cart_total_amount += int(item['qty']) * float(item['price'])

                cart_order_products = CartOrderProducts.objects.create(
                    order=order,
                    invoice_no="INVOICE_NO-" + str(order.id), # INVOICE_NO-5,
                    item=item['title'],
                    image=item['image'],
                    qty=item['qty'],
                    price=item['price'],
                    total=float(item['qty']) * float(item['price'])
                )



        return redirect("core:checkout", order.oid)
    try :
        address = Address.objects.get(user=request.user,status=True)
    except :
        address = None
    context = {
        "page_name":"Save Checkout Info",
        "address":address,
    }
    return render(request,"core/save_checkout_info.html",context)




@login_required
def checkout(request, oid):
    order = CartOrder.objects.get(oid=oid)
    order_items = CartOrderProducts.objects.filter(order=order)


    if request.method == "POST":
        code = request.POST.get("code")
        print("code ========", code)
        coupon = Coupon.objects.filter(code=code, active=True).first()
        if coupon:
            if coupon in order.coupons.all():
                messages.warning(request, "Coupon already activated")
                return redirect("core:checkout", order.oid)
            else:
                discount = order.total_price * coupon.discount / 100
                order.coupons.add(coupon)
                order.total_price -= discount
                order.saved += discount
                order.save()

                messages.success(request, "Coupon Activated")
                return redirect("core:checkout", order.oid)
        else:
            messages.warning(request, "Coupon Does Not Exists")
            return redirect("core:checkout", order.oid)

    host = request.get_host()
    paypal_dict = {
             'business': settings.PAYPAL_RECEIVER_EMAIL,
             'amount': order.total_price,
             'item_name': 'Order-Item-No-'+str(order.oid),
             'invoice': 'INVOICE_NO-'+str(order.oid),
             'currency_code': 'USD',
             'notify_url': 'http://{}{}'.format(host,reverse('core:paypal-ipn')),
             'return_url': 'http://{}{}'.format(host,reverse('core:payment-completed')),
             'cancel_return': 'http://{}{}'.format(host,reverse('core:payement-failed')),
    }

    # Form to render the paypal button
    payment_button_form = PayPalPaymentsForm(initial=paypal_dict)
    cart_data = request.session['cart_data_obj']

    context = {
        "order": order,
        "order_items": order_items,
        "stripe_publishable_key": settings.STRIPE_PUBLIC_KEY,
        "page_name":"Checkout",
        'payment_button_form':payment_button_form,
        "cart_data":cart_data,

    }
    return render(request, "core/checkout.html", context)


@csrf_exempt
def create_checkout_session(request, oid):
    order = CartOrder.objects.get(oid=oid)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        customer_email = order.email,
        payment_method_types=['card'],
        line_items = [
            {
                'price_data': {
                    'currency': 'USD',
                    'product_data': {
                        'name': order.full_name
                    },
                    'unit_amount': int(order.total_price * 100)
                },
                'quantity': 1
            }
        ],
        mode = 'payment',
        success_url = request.build_absolute_uri(reverse("core:payment-completed", args=[order.oid])) + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url = request.build_absolute_uri(reverse("core:payement-failed")
    ))

    order.paid_status = False
    order.stripe_payment_intent = checkout_session['id']
    order.save()

    print("checkkout session", checkout_session)
    return JsonResponse({"sessionId": checkout_session.id})


@login_required
def payment_completed_view1(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
    return render(request, 'core/payment-completed2.html',  {'cart_data':request.session['cart_data_obj'],'totalcartitems':len(request.session['cart_data_obj']),'cart_total_amount':cart_total_amount})


@login_required
def payment_completed_view2(request,oid):
    order = CartOrder.objects.get(oid=oid)
    order_items = CartOrderProducts.objects.filter(order=order)

    if order.paid_status == False:
        order.paid_status = True
        order.save()
        del request.session['cart_data_obj']

    total =0
    for p in order_items :
        total += p.total

    context = {
        "order": order,
        "stripe_publishable_key": settings.STRIPE_PUBLIC_KEY,
        "page_name" :"Payement Completed",
        "order_items":order_items,
        "total" : total
     }

    return render(request, 'core/payment-completed.html',  context)


@login_required
def payment_failed_view(request):
    context = {
        "page_name": "Payement Failed!"
    }
    return render(request, 'core/payment-failed.html',context)


# Customer Dashboard---------------------------------------------------------------------------------------


@login_required
def customer_dashboard(request):
    orders_list = CartOrder.objects.filter(user=request.user).order_by("-id")
    address = Address.objects.filter(user=request.user)
    user_profile = Profile.objects.get(user=request.user)

    orders = CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month", "count")

    month_order= []
    total_orders= []

    for o in orders:
        month_order.append( calendar.month_name[o['month']] )
        total_orders.append(o['count'])

    if request.method == "POST":
        address = request.POST.get("address")
        country = request.POST.get("country")
        state = request.POST.get("state")
        cp = request.POST.get("cp")


        new_address = Address.objects.create(
            user=request.user,
            address=address,
            country=country,
            state=state,
            cp=cp
        )
        messages.success(request, "Address Added Successfully.")
        return redirect("core:dashboard")
    else:
        print("Error")



    context={
         "address": address,
         "page_name":"Dashboard",
          "user_profile": user_profile,
         "orders_list":orders_list,
         "orders":orders,
         "month_order":month_order,
         "total_orders":total_orders,
    }

    return render(request, 'core/dashboard.html',context)



def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({"boolean": True})



def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    order_items = CartOrderProducts.objects.filter(order=order)


    context = {
        "order_items": order_items,
        "page_name":"Order Detail",
    }
    return render(request, 'core/order-detail.html', context)


# Wishlist---------------------------------------------------------------------------------------

@login_required
def wishlist_view(request):
    try:
         wishlist = Wishlist.objects.filter(user=request.user)
    except:
         wishlist = None

    context = {
    "w": wishlist,
    "page_name": "Wishlist"
    }
    return render(request, 'core/wishlist.html', context)



def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)
    print("product id isssssssssssss:" + product_id)

    context = {}

    wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()
    print(wishlist_count)

    if wishlist_count > 0:
        context = {
            "bool": True
        }
    else:
        new_wishlist = Wishlist.objects.create(
            user=request.user,
            product=product,
        )
        context = {
            "bool": True
        }

    return JsonResponse(context)


def remove_wishlist(request):
    pid = request.GET['id']
    wishlist = Wishlist.objects.filter(user=request.user)
    wishlist_d = Wishlist.objects.get(id=pid)
    delete_product = wishlist_d.delete()

    context = {
        "bool":True,
        "w":wishlist
    }
    wishlist_json = serializers.serialize('json', wishlist)
    t = render_to_string('core/async/wishlist-list.html', context)
    return JsonResponse({'data':t,'w':wishlist_json})










# Other Pages---------------------------------------------------------------------------------------

def contact(request):
    return render(request, "core/contact.html",context={"page_name":"Contact Us"})


def ajax_contact_form(request):
    full_name = request.GET['full_name']
    email = request.GET['email']
    phone = request.GET['phone']
    subject = request.GET['subject']
    message = request.GET['message']

    contact = ContactUs.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message,
    )

    data = {
        "bool": True,
        "message": "Message Sent Successfully"
    }

    return JsonResponse({"data":data})





def about_us_view(request):

    return render(request,"core/about-us.html",context={"page_name":"About Us"})

def purchase_guide_view(request):

    return render(request,"core/purchase_guide.html",context={"page_name":"Purchase Guide"})


def privacy_policy(request):
    return render(request, "core/privacy_policy.html",context={"page_name":"Privacy Policy"})

def terms_of_service(request):
    return render(request, "core/terms_of_service.html",context={"page_name":"Terms Of Service"})



def subscribe_view(request):
    if request.method == "POST" :
        email = request.POST.get("email")

        subscriber = Subscriber.objects.create(
            email= email
        )
        messages.success(request,"Thanks for subscribing")
        return redirect("core:index")



def forgout_pass_view(request):

    context={
        "page_name":"Forgout Password",
    }
    if request.method == "POST":
        email = request.POST.get("email")
        try :
            user = User.objects.get(email=email)
        except :
            user = None   

        if user != None:
            request.session['email_reset'] = email
            return redirect("core:reset_pass")
        else :
            messages.warning(request,"Email Does Not Exist, create an account.")
            return render(request,"core/forgout_pass.html",context)
                            
    return render(request,"core/forgout_pass.html",context)



def reset_pass_view(request):
    if  request.method == "POST":
            email = request.POST.get("email")
            new_pass = request.POST.get("pass")
            conf_pass = request.POST.get("confirm_pass")

            if new_pass != conf_pass:
                 messages.warning(request, "Confirm Password and New Password Does Not Match")
                 return redirect("core:reset_pass")
            else :
                request.user = User.objects.get(email=email)
                request.user.set_password(new_pass)
                request.user.save()
                messages.success(request,"Your password has been successfully reset. You can now log in with your new password.")
                return redirect("userauth:sign-in")

    context = {
        "page_name":"Reset Password",
        "email":request.session['email_reset'],
    }

    return render(request,"core/reset_pass.html",context)