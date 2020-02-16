from os import path
from urllib.request import urlretrieve
from PIL import Image
from pillow_affine import Shear, Rotate, Scale, Translate, ComposedTransform

WIDTH = 280


def download_and_resize_raw_image(url, root):
    def download(file):
        urlretrieve(url, file)
        return Image.open(file)

    def resize(image):
        raw_width, raw_height = image.size
        aspect_ratio = raw_width / raw_height
        height = round(WIDTH / aspect_ratio)
        return image.resize((WIDTH, height), Image.BILINEAR)

    file = path.join(root, "raw.png")
    image = resize(download(file))
    image.save(file)
    return image


def create_shear_images(image):
    angle = 30.0

    file = "shear.png"
    transform = Shear(angle)
    transform_params = transform.extract_transform_params(image.size)
    image.transform(*transform_params).save(file)

    file = "shear_clockwise.png"
    transform = Shear(angle, clockwise=True)
    transform_params = transform.extract_transform_params(image.size)
    image.transform(*transform_params).save(file)

    file = "shear_off_center.png"
    transform = Shear(angle, center=(0.0, 0.0))
    transform_params = transform.extract_transform_params(image.size)
    image.transform(*transform_params).save(file)


def create_rotate_images(image):
    angle = 30.0

    file = "rotate.png"
    transform = Rotate(angle)
    transform_params = transform.extract_transform_params(image.size)
    image.transform(*transform_params).save(file)

    file = "rotate_clockwise.png"
    transform = Rotate(angle, clockwise=True)
    transform_params = transform.extract_transform_params(image.size)
    image.transform(*transform_params).save(file)

    file = "rotate_off_center.png"
    transform = Rotate(angle, center=(0.0, 0.0))
    transform_params = transform.extract_transform_params(image.size)
    image.transform(*transform_params).save(file)


def create_scale_images(image):
    file = "scale.png"
    transform = Scale(2.0)
    transform_params = transform.extract_transform_params(image.size)
    image.transform(*transform_params).save(file)

    file = "scale_async.png"
    transform = Scale((0.3, 1.0))
    transform_params = transform.extract_transform_params(image.size)
    image.transform(*transform_params).save(file)

    file = "scale_off_center.png"
    transform = Scale(0.5, center=(0.0, 0.0))
    transform_params = transform.extract_transform_params(image.size)
    image.transform(*transform_params).save(file)


def create_translate_images(image):
    file = "translate.png"
    transform = Translate((50.0, 20.0))
    transform_params = transform.extract_transform_params(image.size)
    image.transform(*transform_params).save(file)

    file = "translate_inverse.png"
    transform = Translate((50.0, 20.0), inverse=True)
    transform_params = transform.extract_transform_params(image.size)
    image.transform(*transform_params).save(file)


def create_composed_transform_images(image):
    file = "composed_1.png"
    transform = ComposedTransform(Shear(45.0), Rotate(30.0), Scale(0.7),)
    transform_params = transform.extract_transform_params(image.size)
    image.transform(*transform_params).save(file)

    file = "composed_2.png"
    transform = ComposedTransform(
        Scale((0.3, 0.7)), Rotate(70.0, clockwise=True), Translate((50.0, 20.0))
    )
    transform_params = transform.extract_transform_params(image.size)
    image.transform(*transform_params).save(file)


def main(url, root):
    image = download_and_resize_raw_image(url, root)

    create_shear_images(image)
    create_rotate_images(image)
    create_scale_images(image)
    create_translate_images(image)
    create_composed_transform_images(image)


if __name__ == "__main__":
    # The image from the URL below is cleared for unrestricted usage
    # http://www.r0k.us/graphics/kodak/kodim15.html
    url = "http://www.r0k.us/graphics/kodak/kodak/kodim15.png"

    here = path.abspath(path.dirname(__file__))
    main(url, here)
