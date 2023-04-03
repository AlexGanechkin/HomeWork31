from django.contrib import admin

from ads.models import Publication, Category, Location, User

admin.site.register(Publication)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(Location)
