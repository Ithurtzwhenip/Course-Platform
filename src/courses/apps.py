from django.apps import AppConfig
from helpers._cloudinary.config import cloudinary_init


class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses'

    def ready(self):
        cloudinary_init()