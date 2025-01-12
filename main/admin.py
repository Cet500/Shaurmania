from django.contrib import admin
from.models import Review, Shaurma

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display=( 'id', 'name', 'text', 'stars','date' )


@admin.register(Shaurma)
class ShaurmaAdmin(admin.ModelAdmin):
    list_display=('id', 'name','compound', 'description', 'picture', 'price', 'weight')