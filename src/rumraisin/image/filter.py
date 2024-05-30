from PIL.Image import Image
from pillow_lut import amplify_lut
from rumraisin.lut import get_lut


def antique_filter(image: Image, intensity: float) -> Image:
    """
    The image filtering for the "Antique" look
    """
    lut = get_lut("Faded")
    amplified = amplify_lut(lut, intensity)
    image = image.filter(amplified)
    return image
