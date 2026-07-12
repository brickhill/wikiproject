from PIL import Image


def resize(image, width=250):
    if image:
        img = Image.open(image.path)
        if img.width > width:
            ratio = width / img.width
            new_height = int(img.height * ratio)
            img.thumbnail((width, new_height))
            img.save(image.path)
            check = Image.open(image.path)
        