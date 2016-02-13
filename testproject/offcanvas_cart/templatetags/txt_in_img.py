import os
import hashlib
from PIL import Image, ImageDraw, ImageFont

from django.conf import settings
from django.template import Library

register = Library()


@register.simple_tag
def txt_in_img(text, image_name, color="#fff", font_size=16, font="lato-heavy.ttf"):
    """
    txt_in_image draw a text in the center of an image.
    It can be used eg. for drawing numbers of items in a cart icon.

    :param text: Text or number to draw. Can be any Python object.
    :type text: object
    :param image_name: The filename of the image. The image must be in the 'img' directory of STATIC
    :type image_name: str
    :param color: Color in which the text will be drawn. Accept all css color values.
    :type color: str
    :param font_size: The used font-size. Default to 16.
    :type font_size: int
    :param font: Font to use. Can be either a TrueType or OpenType font file in the 'fonts' directory of STATIC.
    :type font: str
    :returns: A string with the source location of the created image.
            If a image was created before with the same parameters it will be cached and reused.

    Usage:
    {% load txt_in_img %}
    <img src="{% txt_in_img request.cart.total_quantity "cart.png" "#fdf6e3" 18 %}" alt="{{ request.cart.total_quantity }} item(s)">
    """

    image_dir = settings.STATIC_ROOT + "/img/"
    font_dir = settings.STATIC_ROOT + "/fonts/"
    cache_dir = settings.STATIC_ROOT + "/CACHE/img/"
    cache_url = settings.STATIC_URL + "CACHE/img/"

    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)  # Create cache directory if not exists

    text = str(text)
    img_name_temp = image_name + "-" + text + "-" + color.strip("#") + "-" + str(font_size)  # Remove hashes
    img_name = "%s.png" % (hashlib.md5(img_name_temp).hexdigest())
    if os.path.exists(cache_dir + img_name):  # Make sure img doesn't exist already
        pass
    else:
        icon = Image.open(image_dir + image_name).convert('RGBA')
        fnt = ImageFont.truetype(font_dir + font, font_size)  # encoding='utf-8'
        draw = ImageDraw.Draw(icon)
        x = (icon.size[0] - draw.textsize(text, fnt)[0]) / 2
        y = (icon.size[1] - draw.textsize(text, fnt)[1]) / 2
        draw.text((x, y), text, font=fnt, fill=color)
        icon.save(cache_dir + img_name, "PNG", optimize=True)

    img_src = cache_url + img_name
    return img_src
