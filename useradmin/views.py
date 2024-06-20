from django.shortcuts import render, redirect
from django.db.models import Sum
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.hashers import check_password
import datetime
from django.contrib.auth import login , authenticate,logout
from core.models import *
from userauth.models import Profile, User
from useradmin.forms import AddProductForm
from useradmin.decorators import admin_required
import calendar
from django.db.models.functions import ExtractMonth
from django.db.models import Count,Avg

# @admin_required
def dashboard(request):
    revenue = CartOrder.objects.aggregate(total_price=Sum("total_price"))
    total_orders_count = CartOrder.objects.all()
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    new_customers = User.objects.all().order_by("-id")[:6]
    latest_orders = CartOrder.objects.all()

    this_month = datetime.datetime.now().month
    monthly_revenue = CartOrder.objects.filter(order_date__month=this_month).aggregate(total_price=Sum("total_price"))


    orders = CartOrder.objects.annotate(month=ExtractMonth("order_date")).values("month").annotate(count=Count("id")).values("month", "count")
    cust_orders= orders.filter(user=request.user)
    month = []
    total_orders = []

    for i in cust_orders:
        month.append(calendar.month_name[i["month"]])
        total_orders.append(i["count"])

    # total_orders = [count - 1 for count in total_orders]
    
    context = {
        "monthly_revenue": monthly_revenue,
        "revenue": revenue,
        "all_products": all_products,
        "all_categories": all_categories,
        "new_customers": new_customers,
        "latest_orders": latest_orders,
        "total_orders_count": total_orders_count,
        "page_name":"Admin Dashboard",
        "orders":cust_orders,
        "month_order":month,
        "total_orders": total_orders ,
    }
    return render(request, "useradmin/dashboard.html", context)




# @admin_required
def products(request):
    all_products = Product.objects.all().order_by("-id")
    all_categories = Category.objects.all()
    
    context = {
        "all_products": all_products,
        "all_categories": all_categories,
        "page_name":"Admin Products",
    }
    return render(request, "useradmin/products.html", context)




# @admin_required
def add_product(request):
    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            form.save_m2m()
            return redirect("useradmin:dashboard-products")
    else:
        form = AddProductForm()
    context = {
        'form':form,
        "page_name":"Admin Add Product"
    }
    return render(request, "useradmin/add-products.html", context)


# @admin_required
def edit_product(request, pid):
    product = Product.objects.get(pid=pid)

    if request.method == "POST":
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.save()
            form.save_m2m()
            return redirect("useradmin:dashboard-products")
    else:
        form = AddProductForm(instance=product)
    context = {
        'form':form,
        'product':product,
        "page_name":"Admin Edit Product"
    }
    return render(request, "useradmin/edit-products.html", context)


# @admin_required
def delete_product(request, pid):
    product = Product.objects.get(pid=pid)
    product.delete()
    return redirect("useradmin:dashboard-products")


# @admin_required
def orders(request):
    orders = CartOrder.objects.filter(user=request.user).order_by("-id")
    context = {
        'orders':orders,
        "page_name":"Orders"
    }
    return render(request, "useradmin/orders.html", context)

# @admin_required
def order_detail(request, id):
    order = CartOrder.objects.get(id=id,user=request.user)
    order_items = CartOrderProducts.objects.filter(order=order)
    context = {
        'order':order,
        'order_items':order_items,
        "page_name":"Order Detail",
    }
    return render(request, "useradmin/order_detail.html", context)



# @admin_required
def profile(request):
    products = Product.objects.filter()
    revenue = CartOrder.objects.filter(paid_status=True).aggregate(total_price=Sum("total_price"))
    total_sales = CartOrderProducts.objects.filter(order__paid_status=True).aggregate(qty=Sum("qty"))
    try :
        address = Address.objects.get(user=request.user,status=True)
    except:
        address = None
    context = {
        "address":address,
        'products':products,
        'revenue':revenue,
        'total_sales':total_sales,
        "page_name":"Profile",
    }
    return render(request, "useradmin/profile.html", context)


# @admin_required
def reviews(request):
    reviews = ProductReview.objects.all()
    context = {
        'reviews':reviews,
        "page_name":"Reviews",
    }
    return render(request, "useradmin/reviews.html", context)

# @admin_required
@csrf_exempt
def change_order_status(request, oid):
    order = CartOrder.objects.get(oid=oid)
    if request.method == "POST":
        status = request.POST.get("status")
        print("status =======", status)
        messages.success(request, f"Order status changed to {status}")
        order.order_status = status
        order.save()
    
    return redirect("useradmin:order_detail", order.id)

# @admin_required
def settings_update_profile(request):
    profile = None
    if request.method == "POST":
        image = request.FILES.get("image")
        full_name = request.POST.get("full_name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        try :
            profile = Profile.objects.get(user=request.user)
            if image != None:
                profile.image=image
            profile.full_name=full_name
            profile.phone=phone
            profile.full_name=full_name
            profile.email=email
            profile.save()
        except :
            profile = None
        

        messages.success(request, "Profile Updated Successfully")
        return redirect("useradmin:settings_update")
    
    context = {
        'profile':profile,
        "page_name":"Settings"
    }
    return render(request, "useradmin/setting.html", context)


# @admin_required
def change_password(request):
    profile = None
    try :
        profile = Profile.objects.get(user=request.user)
    except:
        profile = None    

    context = {
        "page_name":"Change Password",
        "profile":profile,
    }

    if request.method == "POST":
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        confirm_new_password = request.POST.get("confirm_new_password")

        if confirm_new_password != new_password:
            messages.warning(request, "Confirm Password and New Password Does Not Match")
        else :
            if check_password(old_password, request.user.password):
                request.user.set_password(new_password)
                request.user.save()
                actual_user = authenticate(username=request.user.username,password= request.user.password)
                login(request,actual_user)
                messages.success(request, "Password Changed Successfully")
            else:
                messages.warning(request, "Old password is not correct")
        
        return render(request, "useradmin/change_password.html",context)

   
    return render(request, "useradmin/change_password.html",context)



def my_address(request):
  
    address = Address.objects.filter(user=request.user)
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
        return redirect("useradmin:my_address")
    else:
        print("Error")
    
    context={
         "address": address,
         "page_name":"My Address",
    }
    return render(request, 'useradmin/my_address.html',context)



def order_tracking(request):
  
    context= {
        "page_name":"Order Tracking",
    }
    return render(request, 'useradmin/order_tracking.html',context)



