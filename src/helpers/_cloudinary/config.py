import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from django.conf import settings

CLOUDINARY_CLOUD_NAME = settings.CLOUDINARY_CLOUD_NAME
CLOUDINARY_API_KEY = settings.CLOUDINARY_API_KEY
CLOUDINARY_SECRET_API_KEY = settings.CLOUDINARY_SECRET_API_KEY

def cloudinary_init():
    cloudinary.config(
    cloud_name = CLOUDINARY_CLOUD_NAME,
    api_key =CLOUDINARY_API_KEY ,
    api_secret = CLOUDINARY_SECRET_API_KEY,
    secure=True
)
