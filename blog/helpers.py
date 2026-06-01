from PIL import Image


def resize(image, width=250):

    if image:
        img = Image.open(image.path)
        if img.width > width:
            ratio = width / img.width
            new_height = int(img.height * ratio)
            resized_img = img.resize((width, new_height))
            resized_img.save(image.path)
