from django.contrib import admin

from userauth.models import User,ContactUs,Profile,Admin

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','email']


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'subject','message']

class ListAdmin(admin.ModelAdmin):
    list_display = ['title', 'admin_image']

class ProfileAdmin(admin.ModelAdmin):
     list_display = ['user_image','user', 'full_name', 'phone','email']


admin.site.register(User,UserAdmin)
admin.site.register(Admin, ListAdmin)
admin.site.register(ContactUs, ContactUsAdmin)
admin.site.register(Profile,ProfileAdmin)