import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from decouple import config

CLOUDINARY_CLOUD_NAME = config('CLOUDINARY_CLOUD_NAME', default=None)
CLOUDINARY_API_KEY = config('CLOUDINARY_API_KEY', default=None)
CLOUDINARY_SECRET_API_KEY = config('CLOUDINARY_SECRET_API_KEY', default=None)

def cloudinary_init():
    cloudinary.config(
    cloud_name = CLOUDINARY_CLOUD_NAME,
    api_key =CLOUDINARY_API_KEY ,
    api_secret = CLOUDINARY_SECRET_API_KEY,
    secure=True
)
