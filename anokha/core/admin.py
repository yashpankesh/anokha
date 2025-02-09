from django.contrib import admin
from .models import Category, Item,Blog
from ckeditor.widgets import CKEditorWidget
from django import forms


# Register your models here.

admin.site.register(Category)
admin.site.register(Item)

class BlogAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Blog
        fields = '__all__'

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    list_display = ('title', 'published_date', 'publisher')
