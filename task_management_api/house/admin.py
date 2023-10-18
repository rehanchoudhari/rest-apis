from django.contrib import admin
from .models import House

# Register your models here.


class HouseAdmin(admin.ModelAdmin):

    readonly_fields=('id',)

admin.site.register(House, HouseAdmin)