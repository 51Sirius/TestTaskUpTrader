from django.contrib import admin

from . models import Menu, MenuItem


@admin.register(Menu)
class Menu(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(MenuItem)
class Item(admin.ModelAdmin):
    list_display = ('id', 'title', 'parent', 'menu')
    list_filter = ('menu', )
    fieldsets = (
        (None, {
            'fields': (('menu', 'parent'), 'title')
        }),
    )
