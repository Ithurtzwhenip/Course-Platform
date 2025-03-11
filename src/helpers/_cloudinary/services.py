from cloudinary import CloudinaryImage, CloudinaryVideo
from django.template.loader import get_template
from django.conf import settings

def get_cloudinary_image_object(instance, field_name="image", as_html=False, width=500):
    if not hasattr(instance, field_name):
        return None

    image_field = getattr(instance, field_name)
    if not image_field:
        return None

    return CloudinaryImage(str(image_field)).build_url(width=width)


def get_cloudinary_video_object(instance,
                                field_name="video",
                                height=None,
                                as_html=False,
                                width=None,
                                sign_url=False,
                                fetch_format= "auto",
                                quality = "auto",
                                controls=True,
                                autoplay=True,
                                ):
    if not hasattr(instance, field_name):
        return None

    video_field = getattr(instance, field_name)
    if not video_field:
        return None

    # Video options dictionary
    video_options = {
        "sign_url": sign_url,
        "fetch_format": fetch_format,
        "quality": quality,
        "controls": controls,
        "autoplay": autoplay,
    }
    if width is not None:
        video_options["width"] = width
    if height is not None:
        video_options["height"] = height
    if height and width:
        video_options["crop"] = "limit"


    video_url = CloudinaryVideo(str(video_field)).build_url(**video_options)

    if as_html:
        template_name = "videos/snippets/embed.html"
        tmpl = get_template(template_name)
        cloud_name = settings.CLOUDINARY_CLOUD_NAME
        _html = tmpl.render({'video_url': video_url,
                             'cloud_name': cloud_name})
        return _html

    return video_url
