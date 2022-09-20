import base64
from io import BufferedReader
from django.core.files.base import ContentFile


def decode_base64_to_image(base64_string: str):
    format, imgstr = base64_string.split(';base64,')
    ext = format.split('/')[-1]

    return ContentFile(base64.b64decode(imgstr), name=f'image.{ext}')


def encode_image_file_to_base64(image_file: BufferedReader):
    return base64.b64encode(image_file.read()).decode('utf-8')
