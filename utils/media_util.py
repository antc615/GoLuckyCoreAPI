from django.conf import settings

def build_absolute_image_url(request, image_field):
    if image_field and hasattr(image_field, 'url'):
        return request.build_absolute_uri(settings.MEDIA_URL + image_field.url)
    return None