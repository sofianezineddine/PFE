from django.db import models
from django.utils.html import mark_safe
from shortuuid.django_fields import ShortUUIDField
from taggit.managers import TaggableManager
from userauth.models import User
from django_ckeditor_5.fields import CKEditor5Field



# def make_serial(prefix,count):

#     all_chars = string.ascii_letters + string.digits
#     chars_count = len(all_chars)

#     serial_list =[]

#     while count > 0:

#         random_number = random.randint(0,chars_count - 1)

#         random_character = all_chars[random_number]

#         serial_list.append(random_character)

#         count -= 1

#     return  f"{prefix}"+f"{string.ascii_letters[random.randint(0,len(string.ascii_letters))]}".join(serial_list)  




STATUS_CHOICE = (
    ("processing", "Processing"),
    ("shipped", "Shipped"),
    ("delivered", "Delivered"),
)


STATUS = (
    ("draft", "Draft"),
    ("in_review", "In Review"),
    ("published", "Published"),
)


RATING = (
    (1,  "★☆☆☆☆"),
    (2,  "★★☆☆☆"),
    (3,  "★★★☆☆"),
    (4,  "★★★★☆"),
    (5,  "★★★★★"),
)







def admin_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)



def products_directory_path(instance,filename):
    return f"prods/{filename}"




class Category(models.Model):
    cid = ShortUUIDField(unique=True, length=10, max_length=20,prefix="cat", alphabet="abcdefgh12345")
    title = models.CharField(max_length=100, default="Cooking")
    image = models.ImageField(upload_to="category", default="category.jpg")

    class Meta:
        verbose_name_plural = "Categories"

    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title






class Product(models.Model):
    pid =ShortUUIDField(unique=True, length=10,max_length=20,prefix="prod", alphabet="abcdefgh12345")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="category")
    title = models.CharField(max_length=100, default="Raw Black Beach Honey Dew")
    image = models.ImageField(upload_to=products_directory_path, default="product.jpg")
    specifications = models.TextField(null=True, blank=True, default="This is the product")
    description = CKEditor5Field(config_name='extends', null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    total_weight = models.FloatField(max_length=3,default=8)

    price = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")
    old_price = models.DecimalField(max_digits=12, decimal_places=2, default="2.99")
    tags = TaggableManager(blank=True)
    color = models.CharField(max_length=50,default="Black")
    origin = models.CharField(max_length=50,default="India")

    product_status = models.CharField(
        choices=STATUS, max_length=10, default="in_review")

    in_stock = models.BooleanField(default=True)
    deals = models.BooleanField(default=False)

    sku = ShortUUIDField(unique=True, length=4, max_length=10,prefix="sku", alphabet="1234567890")

    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True, blank=True)


    class Meta:
        verbose_name_plural = "Products"

    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title

    def get_precentage(self):
        new_price = (1 -self.price / self.old_price) * 100
        return new_price
    



class ProductImages(models.Model):
    images = models.ImageField(
        upload_to="product-images", default="product.jpg")
    product = models.ForeignKey(
        Product, related_name="p_images", on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Product Images"


############################################## Cart, Order, OrderITems and Address ##################################
############################################## Cart, Order, OrderITems and Address ##################################
############################################## Cart, Order, OrderITems and Address ##################################
############################################## Cart, Order, OrderITems and Address ##################################




class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)

    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)
    cp = models.CharField(max_length=5, null=True, blank=True)

    total_price = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")
    saved = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")
    coupons = models.ManyToManyField("core.Coupon", blank=True)
    
    shipping_method = models.CharField(max_length=100, null=True, blank=True)
    tracking_id = models.CharField(max_length=100, null=True, blank=True)
    tracking_website_address = models.CharField(max_length=100, null=True, blank=True)


    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    order_status = models.CharField(choices=STATUS_CHOICE, max_length=30, default="processing")
    sku = ShortUUIDField(null=True, blank=True, length=5,prefix="SKU", max_length=20, alphabet="1234567890")


    # oid =models.UUIDField(unique=True,max_length=20,primary_key=True)
    oid = ShortUUIDField(null=True, blank=True, length=5, max_length=20, alphabet="1234567890")
    stripe_payment_intent = models.CharField(max_length=1000, null=True, blank=True)
    # date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "Cart Order"


class CartOrderProducts(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")
    total = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")

    class Meta:
        verbose_name_plural = "Cart Order Items"

    def order_img(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))




############################################## Product Revew, wishlists, Address ##################################
############################################## Product Revew, wishlists, Address ##################################
############################################## Product Revew, wishlists, Address ##################################
############################################## Product Revew, wishlists, Address ##################################

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name="reviews")
    review = models.TextField()
    rating = models.IntegerField(choices=RATING, default=None)

    date =  models.DateTimeField(auto_now_add=True)
    review_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Product Reviews"

    def __str__(self):
        if self.product:
            return self.product.title
        else:
            return f"review - {self.pk}"

    def get_rating(self):
        return self.rating
    



class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "wishlists"

    def __str__(self):
        return self.product.title


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    cp = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True) 
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Address"


class Coupon(models.Model):
    code = models.CharField(max_length=1000)
    discount = models.IntegerField(default=1)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code}"    
    

class Subscriber(models.Model):
    email = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Subscribers"

    def __str__(self):
        return self.email