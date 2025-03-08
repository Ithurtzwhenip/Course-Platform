import uuid
from enum import unique

from django.db import models
import helpers
from django.utils.text import slugify
from cloudinary.models import CloudinaryField

helpers.cloudinary_init()


class AccessRequirement(models.TextChoices):
    PUBLISHED = "any", "Anyone"
    EMAIL_REQUIRED = "email", "Email Required"


class PublishStatus(models.TextChoices):
    PUBLISHED = "pub", "Published"
    COMING_SOON = "soon", "Coming Soon"
    DRAFT = "draft", "Draft"


def handle_upload(instance, filename):
    return f"{filename}"


def generate_public_id(instance, *args, **kwargs):
    title = instance.title
    unique_id = str(uuid.uuid4()).replace("-", "")[:5]
    if not title:
        return unique_id
    slug = slugify(title)
    unique_id_short = unique_id[:5]
    return f"course/{slug}-{unique_id}"


def get_public_id_prefix(instance, *args, **kwargs):
    public_id = instance.public_id
    if not public_id:
        return "courses"
    return f"courses/{public_id}"


def get_display_name(instance, *args, **kwargs):
    title = instance.title
    if title:
        return title
    return 'Course Upload'


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    public_id = models.CharField(max_length=130, blank=True, null=True)
    # image = models.ImageField(upload_to=handle_upload, blank=True, null=True)
    image = CloudinaryField("image", blank=True, null=True, public_id_prefix=get_public_id_prefix,
                            display_name=get_display_name,
                            tags=["course", "thumbnail"]
                            )
    access = models.CharField(max_length=5,
                              choices=AccessRequirement.choices,
                              default=AccessRequirement.EMAIL_REQUIRED

                              )

    status = models.CharField(max_length=10,
                              choices=PublishStatus.choices,
                              default=PublishStatus.DRAFT

                              )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.public_id:  # Fix: Properly checks for None or empty string
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED

    @property
    def image_admin_url(self):
        if not self.image:
            return None
        image_options = {
            "width": 200,
        }
        url = self.image.build_url(**image_options)
        return url


    def get_image_detail(self, as_html=False, width=750):
        if not self.image:
            return None
        image_options = {
            "width": width,
        }
        if as_html:
            # CloudinaryImage(str(self.image)).image(**image_options)
            return self.image.build_url(**image_options)
        # CloudinaryImagestr(str(self.image)).build_url(**image_options)
        url = self.image.build_url(**image_options)
        return url


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    public_id = models.CharField(max_length=130, blank=True, null=True)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    thumbnail = CloudinaryField("image", blank=True, null=True)
    video = CloudinaryField("video", blank=True, null=True, resource_type="video")
    order = models.IntegerField(default=0)
    can_preview = models.BooleanField(default=False,
                                      help_text="If user does not have access to course, can they see this? ")
    status = models.CharField(max_length=10,
                              choices=PublishStatus.choices,
                              default=PublishStatus.PUBLISHED
                              )
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-updated']

    def save(self, *args, **kwargs):
        if not self.public_id:  # Fix: Properly checks for None or empty string
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)

