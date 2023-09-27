from django.contrib import admin

# Register your models here.
from .models import PhotoSet, Photo_pair
from .forms import PhotoForm, SetForm

class PhotoPairInline(admin.TabularInline):
    model = Photo_pair

class PhotoSetAdmin(admin.ModelAdmin):
    form = SetForm
    inlines = [
        PhotoPairInline
    ]
class PhotoAdmin(admin.ModelAdmin):
    form = PhotoForm

admin.site.register(PhotoSet, PhotoSetAdmin)


