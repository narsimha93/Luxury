from django.contrib import admin

from .models import Contact, transportation,reviews

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'listing', 'email', 'contact_date')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'email', 'listing')
    list_per_page = 25

class TransportationAdmin(admin.ModelAdmin):
    list_display = ('name','owner_phone_number','onwer_address','owner_pincode','no_of_boxes')

admin.site.register(Contact, ContactAdmin)
admin.site.register(transportation,TransportationAdmin)
admin.site.register(reviews)