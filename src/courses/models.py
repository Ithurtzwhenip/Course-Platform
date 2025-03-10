import uuid
from django.db import models
import helpers
from django.utils.text import slugify
from cloudinary.models import CloudinaryField
from cloudinary import CloudinaryImage  # Fix: Import added

helpers.cloudinary_init()


class AccessRequirement(models.TextChoices):
    PUBLISHED = "any", "Anyone"
    EMAIL_REQUIRED = "email", "Email Required"


class PublishStatus(models.TextChoices):
    PUBLISHED = "pub", "Published"
    COMING_SOON = "soon", "Coming Soon"
    DRAFT = "draft", "Draft"


def handle_upload(instance, filename):
    return f"uploads/{uuid.uuid4().hex[:8]}_{filename}"  # Fix: Unique filename


def generate_public_id(instance, *args, **kwargs):
    title = instance.title
    unique_id = str(uuid.uuid4()).replace("-", "")[:5]  # Fix: Generates unique 5-character ID
    if not title:
        return unique_id
    slug = slugify(title)
    return f"course/{slug}-{unique_id}"


def get_public_id_prefix(instance, *args, **kwargs):
    if hasattr(instance, 'path'):
        path = instance.path.strip("/")
        return path
    public_id = instance.public_id
    model_name_slug = slugify(instance.__class__.__name__)
    return f"{model_name_slug}/{public_id}" if public_id else model_name_slug


def get_display_name(instance, *args, **kwargs):
    if hasattr(instance, "get_display_name"):
        return instance.get_display_name()
    elif hasattr(instance, 'title'):
        return instance.title
    return f'{instance.__class__.__name__} Upload'


class Course(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    public_id = models.CharField(max_length=130, blank=True, null=True)
    image = CloudinaryField("image", blank=True, null=True,
                            public_id_prefix=get_public_id_prefix,
                            display_name=get_display_name,
                            tags=["course", "thumbnail"])
    access = models.CharField(max_length=5, choices=AccessRequirement.choices, default=AccessRequirement.EMAIL_REQUIRED)
    status = models.CharField(max_length=10, choices=PublishStatus.choices, default=PublishStatus.DRAFT)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.public_id:
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return f"/{self.path}/"

    @property
    def path(self):
        return f"courses/{self.public_id}"

    def get_display_name(self):
        return f"{self.title}- Course"

    @property
    def is_published(self):
        return self.status == PublishStatus.PUBLISHED


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    public_id = models.CharField(max_length=130, blank=True, null=True)
    title = models.CharField(max_length=120)
    description = models.TextField(blank=True, null=True)
    thumbnail = CloudinaryField("image",
                                public_id_prefix=get_public_id_prefix,
                                display_name=get_display_name,
                                tags=['thumbnail', 'lesson'],
                                blank=True, null=True)
    video = CloudinaryField("video",
                            public_id_prefix=get_public_id_prefix,
                            display_name=get_display_name,
                            tags=['video', 'lesson'],
                            blank=True,
                            null=True,
                            type="private",
                            resource_type="video")
    order = models.IntegerField(default=0)
    can_preview = models.BooleanField(default=False,
                                      help_text="If user does not have access to course, can they see this?")
    status = models.CharField(max_length=10, choices=PublishStatus.choices, default=PublishStatus.PUBLISHED)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-updated']

    def save(self, *args, **kwargs):
        if not self.public_id:
            self.public_id = generate_public_id(self)
        super().save(*args, **kwargs)

    @property
    def path(self):
        return f"{self.course.path}/lessons/{self.public_id}"

    def get_display_name(self):
        return f"{self.title}- {self.course.get_display_name()}"
