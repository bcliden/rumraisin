from random import choice
from typing import Callable, Optional

from PIL import ImageFont as imf
from PIL.Image import Image
from PIL.ImageDraw import ImageDraw
from PIL.ImageFilter import Color3DLUT
from pillow_lut import amplify_lut
from rumraisin.lut import get_lut

picks: dict[str, Optional[Color3DLUT]] = {
    "Old": get_lut("Faded"),  # or Tweed or Pasadena?
    "Vibrant": get_lut("Teigen"),  # or Magic Hour?
    "B&W": get_lut("SoftBlackAndWhite"),  # or Zeke?
}

font = imf.load_default(60)


def antique_filter(image: Image, intensity: float) -> Image:
    """
    The image filtering for the "Antique" look
    """
    lut = get_lut("Faded")
    amplified = amplify_lut(lut, intensity)
    image = image.filter(amplified)
    return image


def process_lut(name: str) -> Callable[[Image, float], Image]:
    if name not in picks:
        raise SystemError(f"Invalid LUT: '{name}'")

    lut = picks[name]

    def process_image(image: Image, intensity: float) -> Image:
        amplified = amplify_lut(lut, intensity)
        image = image.filter(amplified)
        draw = ImageDraw(image)
        draw.text(
            xy=(10, 10),
            text=name,
            font=font,
            fill="white",
            stroke_width=5,
            stroke_fill="black",
        )
        return image

    return process_image


antique = process_lut("Old")


def random_filter(image: Image, intensity: float) -> Image:
    name = choice(list(picks.keys()))
    return process_lut(name)(image, intensity)
