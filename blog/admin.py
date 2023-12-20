from django.contrib import admin
from . import models


# Register your models here.
# ===== actions ====================================================================


def make_publshed(modeladmin, request, queryset):
    rows_update = queryset.update(status='p')
    if rows_update == 1:
        massage_bit = "منتشر شد."
    else:
        massage_bit = "منتشر شدند."
    modeladmin.message_user(request, "{} مقاله {}".format(rows_update, massage_bit))


def make_draft(modeladmin, request, queryset):
    rows_update = queryset.update(status='d')
    if rows_update == 1:
        massage_bit = "پیش نویس شد."
    else:
        massage_bit = "پیش نویس شدند."
    modeladmin.message_user(request, "{} مقاله {}".format(rows_update, massage_bit))


make_draft.short_description = "پیش نویس کزدن مقالات انتخاب شده"
make_publshed.short_description = "انتشار مقالات انتخاب شده"


# ===== end actions ================================================================

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'parent', 'status')
    list_filter = (['status'])
    search_fields = ("title", "slug")
    prepopulated_fields = {"slug": ("title",)}


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbnail_tag', 'slug', 'author', 'jpublish', 'is_special', 'status', 'category_to_str')
    list_filter = ('publish', 'status')
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ('-publish', 'status')
    actions = [make_publshed, make_draft]


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.IPAddress)
admin.site.register(models.ArticleHit)
