from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.utils.html import mark_safe
from shortuuid.django_fields import ShortUUIDField
from django_ckeditor_5.fields import CKEditor5Field



class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS =['username']

    def __str__(self):
        return self.username

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to="image", null=True,blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True) 
    def __str__(self):
      
        return f"{self.user.username} - {self.full_name}"

    def user_image(self):
        try :
            image = self.image.url
        except :
            image = "https://www.shutterstock.com/image-vector/vector-flat-illustration-grayscale-avatar-600nw-2281862025.jpg"    
        return mark_safe('<img src="%s" width="50" height="50" />' % (image))
       


def admin_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Admin(models.Model):
    aid =  ShortUUIDField(unique=True, length=10, max_length=20,
                         prefix="adm", alphabet="abcdefgh12345")
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100, default="Nestify")
    image = models.ImageField(
        upload_to=admin_directory_path, default="vendor.jpg")
    # description = models.TextField(null=True, blank=True, default="Store Admin")
    description = CKEditor5Field(config_name='extends', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Admins"

    def admin_image(self):
        return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))

    def __str__(self):
        return self.title


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
 
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)



class ContactUs(models.Model):
    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=200) 
    subject = models.CharField(max_length=200) 
    message = models.TextField()

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"

    def __str__(self):
        return self.full_name
