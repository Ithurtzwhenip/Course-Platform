from cloudinary import CloudinaryImage
from django.contrib import admin
from django.utils.html import format_html
# Register your models here.

from .models import Course, Lesson


class LessonInLine(admin.StackedInline):
    model = Lesson
    extra = 0

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInLine]
    list_display = ('title', 'description', 'access')
    list_filter = ('status', 'access')
    fields = ['public_id','title', 'description', 'status', 'image', 'access', 'display_image']
    readonly_fields = ['public_id','display_image']

    def display_image(self, obj, *args, **kwargs):
        url = obj.image_admin_url
        return format_html(f"<img src='{url}'>")

    display_image.short_description = "Current Image"
# admin.site.register(Course)
