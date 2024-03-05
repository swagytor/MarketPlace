import os

from PIL import Image

from MarketPlace.settings import BASE_DIR


def resize_images(instance):
    model_name = instance._meta.model_name
    img_name = instance.img.name.split('/')[-1]
    img_path = f'{BASE_DIR}/media/{model_name}/big/{img_name}'

    img = Image.open(img_path)
    medium_size = (img.width // 4, img.height // 4)
    small_size = (img.width // 10, img.height // 10)

    medium_img = img.resize(medium_size)
    os.makedirs(f'{BASE_DIR}/media/{model_name}/medium/', exist_ok=True)
    medium_img_path = f'{BASE_DIR}/media/{model_name}/medium/{img_name}'
    medium_img.save(medium_img_path)
    instance.medium_img = f'{model_name}/medium/{img_name}'

    small_img = img.resize(small_size)
    os.makedirs(f'{BASE_DIR}/media/{model_name}/small/', exist_ok=True)
    small_img_path = f'{BASE_DIR}/media/{model_name}/small/{img_name}'
    small_img.save(small_img_path)
    instance.small_img = f'{model_name}/small/{img_name}'
