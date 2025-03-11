import helpers
from cloudinary import CloudinaryImage
from django.contrib import admin
from django.utils.html import format_html
# Register your models here.

from .models import Course, Lesson


class LessonInLine(admin.StackedInline):
    model = Lesson
    readonly_fields = ['public_id', 'updated', 'display_image', 'display_video']
    extra = 0

    def display_image(self, obj):

        if obj.thumbnail and hasattr(obj.thumbnail, 'url'):
            url = obj.thumbnail.url
            return format_html(f"<img src='{url}' width='300'>")
        return "No Image Available"

    display_image.short_description = "Current Image"

    def display_video(self, obj):

        if obj.video and hasattr(obj.video, 'url'):
            url = obj.video.url
            return format_html(f"""
                <video width="300" controls>
                    <source src="{url}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            """)
        return "No Video Available"

    display_video.short_description = "Current Video"


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [LessonInLine]
    list_display = ('title', 'description', 'access')
    list_filter = ('status', 'access')
    fields = ['public_id', 'title', 'description', 'status', 'image', 'access', 'display_image']
    readonly_fields = ['public_id', 'display_image']

    def display_image(self, obj, *args, **kwargs):
        if hasattr(obj, 'image_admin_url') and obj.image_admin_url:
            return format_html(f"<img src='{obj.image_admin_url}' width='300'>")
        return "No Image Available"

    display_image.short_description = "Current Image"

# admin.site.register(Course)
